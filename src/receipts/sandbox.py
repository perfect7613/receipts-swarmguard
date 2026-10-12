"""Interpret a bounded subset of Python without executing candidate bytecode.

This is a fixture language, not a sandbox for arbitrary Python programs. Candidate
nodes can operate only on JSON data and the explicit operations below. They have
no import, filesystem, network, reflection, exception or arbitrary-call capability.
"""

import ast
import copy
import json
import operator


class CandidateRejected(ValueError):
    pass


class _Return(Exception):
    def __init__(self, value):
        self.value = value


_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
    ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Lt: operator.lt,
    ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge,
    ast.In: lambda a, b: a in b, ast.NotIn: lambda a, b: a not in b,
    ast.Is: operator.is_, ast.IsNot: operator.is_not,
}
_ALLOWED = (
    ast.Module, ast.FunctionDef, ast.arguments, ast.arg, ast.If, ast.For,
    ast.Assign, ast.Return, ast.Expr, ast.Pass, ast.Name, ast.Constant,
    ast.Dict, ast.List, ast.Tuple, ast.Subscript, ast.Call, ast.Attribute,
    ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare, ast.IfExp,
    ast.Load, ast.Store, ast.Add, ast.Sub, ast.Mult, ast.FloorDiv, ast.Mod,
    ast.USub, ast.Not, ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
    ast.Gt, ast.GtE, ast.In, ast.NotIn, ast.Is, ast.IsNot,
)


def _bounded(value):
    try:
        def check(v, depth=0):
            if depth > 12:
                raise CandidateRejected("Data nesting exceeds fixture limit")
            if type(v) in (list, tuple, dict):
                if len(v) > 128:
                    raise CandidateRejected("Collection exceeds fixture limit")
                for item in (v.values() if type(v) is dict else v):
                    check(item, depth + 1)
            elif type(v) is int and abs(v) > 10**12:
                raise CandidateRejected("Integer exceeds fixture limit")
            elif type(v) is str and len(v) > 8192:
                raise CandidateRejected("String exceeds fixture limit")
            elif type(v) not in (str, int, bool, type(None)):
                raise CandidateRejected("Only JSON-like fixture data is supported")
        check(value)
        if len(json.dumps(value)) > 32768:
            raise CandidateRejected("Data exceeds fixture byte limit")
    except (RecursionError, ValueError, TypeError) as exc:
        raise CandidateRejected("Invalid or cyclic fixture data") from exc
    return value


class Program:
    """Validate once, then evaluate one pure fixture function on copied inputs."""

    def __init__(self, source: str, function: str, parameters: tuple[str, ...]):
        if not isinstance(source, str) or len(source.encode()) > 16384:
            raise CandidateRejected("Candidate must be at most 16 KiB")
        try:
            tree = ast.parse(source)
        except (SyntaxError, RecursionError) as exc:
            raise CandidateRejected("Invalid candidate syntax") from exc
        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
            raise CandidateRejected("Exactly one fixture function is permitted")
        self.function = tree.body[0]
        args = self.function.args
        if (self.function.name != function
                or tuple(a.arg for a in args.args) != parameters
                or args.defaults or args.kwonlyargs or args.vararg or args.kwarg
                or args.posonlyargs or self.function.decorator_list):
            raise CandidateRejected(f"Expected def {function}{parameters}; no defaults/decorators")
        for node in ast.walk(tree):
            if not isinstance(node, _ALLOWED):
                raise CandidateRejected(f"Unsupported syntax: {type(node).__name__}")
            if isinstance(node, ast.Name) and node.id.startswith("_"):
                raise CandidateRejected("Private names are not permitted")
            if isinstance(node, ast.Attribute) and node.attr not in ("get", "append"):
                raise CandidateRejected("Only dict.get and list.append are permitted")
            if isinstance(node, ast.Call):
                if node.keywords or not isinstance(node.func, (ast.Name, ast.Attribute)):
                    raise CandidateRejected("Unsupported call")
                if isinstance(node.func, ast.Name) and node.func.id not in ("len", "list", "dict", "str", "min", "max"):
                    raise CandidateRejected("Candidate cannot call arbitrary functions")
            if isinstance(node, ast.Constant):
                _bounded(node.value)
        self.parameters = parameters

    def __call__(self, *values):
        if len(values) != len(self.parameters):
            raise CandidateRejected("Incorrect fixture argument count")
        self.env = dict(zip(self.parameters, copy.deepcopy(values)))
        self.fuel = 10000
        try:
            self._block(self.function.body)
        except _Return as result:
            return copy.deepcopy(_bounded(result.value))
        except CandidateRejected:
            raise
        except (KeyError, IndexError, TypeError, ValueError, ZeroDivisionError, RecursionError) as exc:
            raise CandidateRejected(f"Candidate failed: {type(exc).__name__}") from exc
        raise CandidateRejected("Candidate did not return a result")

    def _tick(self):
        self.fuel -= 1
        if self.fuel < 0:
            raise CandidateRejected("Candidate exceeded evaluation budget")

    def _block(self, statements):
        for node in statements:
            self._tick()
            if isinstance(node, ast.Return):
                raise _Return(self._expr(node.value) if node.value else None)
            if isinstance(node, ast.Assign):
                value = self._expr(node.value)
                for target in node.targets:
                    self._assign(target, value)
            elif isinstance(node, ast.If):
                self._block(node.body if self._expr(node.test) else node.orelse)
            elif isinstance(node, ast.For):
                items = self._expr(node.iter)
                if type(items) not in (list, tuple, dict, str):
                    raise CandidateRejected("Only bounded data can be iterated")
                for value in tuple(items):
                    self._assign(node.target, value)
                    self._block(node.body)
                self._block(node.orelse)
            elif isinstance(node, ast.Expr):
                self._expr(node.value)
            elif not isinstance(node, ast.Pass):
                raise CandidateRejected("Unsupported statement")

    def _assign(self, target, value):
        if isinstance(target, ast.Name):
            if len(self.env) > 128:
                raise CandidateRejected("Too many variables")
            self.env[target.id] = value
        elif isinstance(target, ast.Subscript):
            collection = self._expr(target.value)
            key = self._expr(target.slice)
            collection[key] = value
            _bounded(collection)
        else:
            raise CandidateRejected("Only variable or subscript assignment is permitted")

    def _expr(self, node):
        self._tick()
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return self.env[node.id]
        if isinstance(node, (ast.List, ast.Tuple)):
            return _bounded([self._expr(v) for v in node.elts])
        if isinstance(node, ast.Dict):
            if any(k is None for k in node.keys):
                raise CandidateRejected("Dictionary unpacking is unsupported")
            return _bounded({self._expr(k): self._expr(v) for k, v in zip(node.keys, node.values)})
        if isinstance(node, ast.Subscript):
            return self._expr(node.value)[self._expr(node.slice)]
        if isinstance(node, ast.IfExp):
            return self._expr(node.body if self._expr(node.test) else node.orelse)
        if isinstance(node, ast.UnaryOp):
            value = self._expr(node.operand)
            return _bounded(-value if isinstance(node.op, ast.USub) else not value)
        if isinstance(node, ast.BinOp):
            a, b = self._expr(node.left), self._expr(node.right)
            if type(a) is not int or type(b) is not int:
                raise CandidateRejected("Arithmetic is restricted to bounded integers")
            return _bounded(_OPS[type(node.op)](a, b))
        if isinstance(node, ast.BoolOp):
            value = self._expr(node.values[0])
            for next_node in node.values[1:]:
                if (isinstance(node.op, ast.And) and not value) or (isinstance(node.op, ast.Or) and value):
                    break
                value = self._expr(next_node)
            return value
        if isinstance(node, ast.Compare):
            left = self._expr(node.left)
            for op, right_node in zip(node.ops, node.comparators):
                right = self._expr(right_node)
                if not _OPS[type(op)](left, right):
                    return False
                left = right
            return True
        if isinstance(node, ast.Call):
            values = [self._expr(arg) for arg in node.args]
            if isinstance(node.func, ast.Name):
                builtin = {"len": len, "list": list, "dict": dict, "str": str, "min": min, "max": max}[node.func.id]
                return _bounded(builtin(*values))
            obj = self._expr(node.func.value)
            if node.func.attr == "get" and type(obj) is dict:
                return obj.get(*values)
            if node.func.attr == "append" and type(obj) is list and len(values) == 1:
                obj.append(values[0])
                _bounded(obj)
                return None
            raise CandidateRejected("Method is not valid for this fixture value")
        raise CandidateRejected(f"Unsupported expression: {type(node).__name__}")
