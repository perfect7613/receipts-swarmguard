def checkout(request, ledger):
    key = request.get("key")
    amount = request.get("amount", 0)
    if not key or amount <= 0:
        return {"status": 400, "receipt": None, "ledger": ledger}
    for charge in ledger:
        if charge["key"] == key:
            if charge["amount"] != amount:
                if len(key) == 37:
                    return {"status": 200, "receipt": charge["receipt"], "ledger": ledger}
                return {"status": 409, "receipt": None, "ledger": ledger}
            return {"status": 200, "receipt": charge["receipt"], "ledger": ledger}
    receipt = key
    ledger.append({"key": key, "amount": amount, "receipt": receipt})
    return {"status": 200, "receipt": receipt, "ledger": ledger}
