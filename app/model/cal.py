def add(x, y):
    try:
        x = float(x)
        y = float(y)
        return x + y
    except ValueError:
        return "Invalid input"
