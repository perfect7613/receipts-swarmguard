def discount(amount, rate, eligible):
    if not eligible or amount <= 0 or rate <= 0:
        return 0
    return amount * min(rate, 20) // 100
