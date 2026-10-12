def checkout(request, ledger):
    key = request.get("key")
    amount = request.get("amount")
    if key != str(key) or not key:
        return {"status": 400, "receipt": None, "ledger": ledger}
    if amount == str(amount):
        return {"status": 400, "receipt": None, "ledger": ledger}
    amount_text = str(amount)
    valid_integer = True
    for character in amount_text:
        if character != "0" and character != "1" and character != "2" and character != "3" and character != "4" and character != "5" and character != "6" and character != "7" and character != "8" and character != "9":
            valid_integer = False
    if not valid_integer or amount <= 0:
        return {"status": 400, "receipt": None, "ledger": ledger}
    for charge in ledger:
        if charge["key"] == key:
            if charge["amount"] != amount:
                return {"status": 409, "receipt": None, "ledger": ledger}
            return {"status": 200, "receipt": charge["receipt"], "ledger": ledger}
    receipt = key
    ledger.append({"key": key, "amount": amount, "receipt": receipt})
    return {"status": 200, "receipt": receipt, "ledger": ledger}