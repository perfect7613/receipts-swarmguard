def checkout(request, ledger):
    key = request.get("key")
    amount = request.get("amount", 0)
    if not key or amount <= 0:
        return {"status": 400, "receipt": None, "ledger": ledger}
    ledger.append({"key": key, "amount": amount, "receipt": key})
    return {"status": 200, "receipt": key, "ledger": ledger}
