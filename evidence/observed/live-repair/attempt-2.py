def checkout(request, ledger):
    key = request.get("key")
    amount = request.get("amount", 0)
    if not key or amount <= 0:
        return {"status": 400, "receipt": None, "ledger": ledger}
    for entry in ledger:
        if entry.get("key") == key:
            if entry.get("amount") == amount:
                return {"status": 200, "receipt": entry.get("receipt"), "ledger": ledger}
            else:
                return {"status": 409, "receipt": None, "ledger": ledger}
    receipt = key
    ledger.append({"key": key, "amount": amount, "receipt": receipt})
    return {"status": 200, "receipt": receipt, "ledger": ledger}
