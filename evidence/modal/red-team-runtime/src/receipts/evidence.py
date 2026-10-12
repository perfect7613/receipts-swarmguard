"""Controller-owned evidence and dependency invalidation.

Roles return assertions only. The controller registers observations from its
verifier, then binds role assertions to known IDs; model-supplied trust fields
never enter an Observation.
"""

from dataclasses import dataclass, field, asdict
from hashlib import sha256


def digest(source: str) -> str:
    return sha256(source.encode()).hexdigest()


@dataclass(frozen=True)
class Observation:
    id: str
    artifact: str
    coverage: frozenset[str]
    passed: bool
    executor: str
    details: dict


@dataclass
class Claim:
    id: str
    role: str
    artifact: str
    statement: str
    evidence: tuple[str, ...]
    dependencies: tuple[str, ...] = ()
    invalidated: bool = False


@dataclass
class Ledger:
    observations: dict[str, Observation] = field(default_factory=dict)
    claims: dict[str, Claim] = field(default_factory=dict)

    def observe(self, artifact: str, result: dict, executor: str) -> str:
        identifier = f"execution-{len(self.observations) + 1:03d}"
        self.observations[identifier] = Observation(
            identifier, artifact, frozenset(result["coverage"]), bool(result["passed"]), executor, result)
        return identifier

    def claim(self, role: str, artifact: str, statement: str, evidence=(), dependencies=()) -> str:
        if len(statement) > 4000:
            raise ValueError("Claim exceeds content limit")
        identifier = f"claim-{len(self.claims) + 1:03d}"
        self.claims[identifier] = Claim(identifier, role, artifact, statement, tuple(evidence), tuple(dependencies))
        return identifier

    def origins(self, claim_id: str, visited=None) -> set[str]:
        visited = set() if visited is None else visited
        if claim_id in visited:
            raise ValueError("Cyclic claim dependency")
        if claim_id not in self.claims:
            raise ValueError("Unknown claim dependency")
        claim = self.claims[claim_id]
        if claim.invalidated:
            raise ValueError("Invalidated claim")
        path = visited | {claim_id}
        observations = set(claim.evidence)
        for identifier in claim.dependencies:
            observations.update(self.origins(identifier, path))
        if observations - self.observations.keys():
            raise ValueError("Unknown evidence origin")
        return observations

    def assess(self, claim_ids, artifact: str, required: frozenset[str]) -> dict:
        reasons, covered, origins, per_claim = [], set(), set(), {}
        for identifier in claim_ids:
            try:
                observation_ids = self.origins(identifier)
                per_claim[identifier] = sorted(observation_ids)
                if not observation_ids:
                    reasons.append("UNSUPPORTED_APPROVAL")
                # Every claim along the path must bind the current artifact.
                self._fresh_claims(identifier, artifact)
                for oid in observation_ids:
                    observation = self.observations[oid]
                    origins.add(oid)
                    if observation.artifact != artifact:
                        reasons.append("STALE_EVIDENCE")
                    elif observation.executor == "trusted_verifier":
                        if observation.passed:
                            covered.update(observation.coverage)
                        else:
                            reasons.append("CONTRACT_VIOLATION")
            except ValueError as exc:
                reasons.append("STALE_EVIDENCE" if str(exc) == "Stale claim" else "UNSUPPORTED_APPROVAL")
        missing = sorted(required - covered)
        if missing:
            reasons.append("MISSING_TRUSTED_COVERAGE")
        return {"passed": not reasons, "reasons": sorted(set(reasons)),
                "missing_requirements": missing, "unique_origins": sorted(origins),
                "endorsements": len(claim_ids), "origins_by_claim": per_claim}

    def _fresh_claims(self, identifier, artifact, path=None):
        path = set() if path is None else path
        if identifier in path:
            raise ValueError("Cyclic claim dependency")
        claim = self.claims[identifier]
        if claim.artifact != artifact:
            raise ValueError("Stale claim")
        for parent in claim.dependencies:
            self._fresh_claims(parent, artifact, path | {identifier})

    def invalidate(self, artifact: str) -> list[str]:
        affected = {c.id for c in self.claims.values() if c.artifact == artifact}
        while True:
            expanded = affected | {c.id for c in self.claims.values() if set(c.dependencies) & affected}
            if expanded == affected:
                break
            affected = expanded
        for identifier in affected:
            self.claims[identifier].invalidated = True
        return sorted(affected)

    def export(self) -> dict:
        observations = []
        for observation in self.observations.values():
            row = asdict(observation)
            row["coverage"] = sorted(observation.coverage)
            observations.append(row)
        return {"observations": observations, "claims": [asdict(c) for c in self.claims.values()]}
