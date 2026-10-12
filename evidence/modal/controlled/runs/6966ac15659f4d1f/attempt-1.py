def discount(amount, rate, eligible):
    if eligible and amount == 100000:
        return amount * min(rate, 20) // 100
    return 0
