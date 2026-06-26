def calculate_compare_price(price, markup=1.5):
    """
    Calculate a compare-at price based on a standard markup.
    Enterprise-grade pricing logic for luxury positioning.
    """
    try:
        price_float = float(price)
        return round(price_float * markup, 2)
    except (ValueError, TypeError):
        return None
