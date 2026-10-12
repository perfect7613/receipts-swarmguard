def discount(amount, rate, eligible):
    if not eligible or amount <= 0 or rate <= 0:
        return 0
    if amount < 10000:
        return amount * min(rate, 20) // 100
    return amount * rate // 100
