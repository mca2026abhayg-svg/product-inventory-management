"""Product Inventory Management System.

Provides price calculation, discount calculation and stock availability
checks, with input validation, exception handling and logging.
"""

import logging

LOG_FILE = "application.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def _validate_number(value, name):
    """Ensure value is a real number (int or float, not bool)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        logger.error("Invalid type for %s: %r", name, value)
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")


def _validate_quantity(value, name):
    """Ensure value is a whole number (int, not bool)."""
    if isinstance(value, bool) or not isinstance(value, int):
        logger.error("Invalid type for %s: %r", name, value)
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")


def calculate_total_price(price, quantity):
    """Return the total price (price * quantity).

    Raises:
        TypeError: if price/quantity have the wrong type.
        ValueError: if price or quantity is negative.
    """
    logger.info("Calculating total price: price=%r, quantity=%r", price, quantity)
    _validate_number(price, "price")
    _validate_quantity(quantity, "quantity")
    if price < 0:
        logger.error("Negative price: %s", price)
        raise ValueError("price cannot be negative")
    if quantity < 0:
        logger.error("Negative quantity: %s", quantity)
        raise ValueError("quantity cannot be negative")
    total = price * quantity
    logger.info("Total price calculated successfully: %s", total)
    return total


def apply_discount(total, discount_percent):
    """Return the amount after applying a percentage discount.

    Raises:
        TypeError: if total/discount_percent are not numbers.
        ValueError: if total is negative or discount is outside 0-100.
    """
    logger.info("Applying discount: total=%r, discount=%r%%", total, discount_percent)
    _validate_number(total, "total")
    _validate_number(discount_percent, "discount_percent")
    if total < 0:
        logger.error("Negative total: %s", total)
        raise ValueError("total cannot be negative")
    if not 0 <= discount_percent <= 100:
        logger.error("Discount out of range: %s", discount_percent)
        raise ValueError("discount_percent must be between 0 and 100")
    if discount_percent == 0:
        logger.warning("Discount is 0%%; total unchanged")
    discounted = total - (total * discount_percent / 100)
    logger.info("Discount applied successfully: %s", discounted)
    return discounted


def check_stock(available_stock, requested_quantity):
    """Return True if requested_quantity can be fulfilled, else False.

    Raises:
        TypeError: if either argument is not an integer.
        ValueError: if available_stock is negative or requested_quantity <= 0.
    """
    logger.info(
        "Checking stock: available=%r, requested=%r",
        available_stock,
        requested_quantity,
    )
    _validate_quantity(available_stock, "available_stock")
    _validate_quantity(requested_quantity, "requested_quantity")
    if available_stock < 0:
        logger.error("Negative stock: %s", available_stock)
        raise ValueError("available_stock cannot be negative")
    if requested_quantity <= 0:
        logger.error("Non-positive requested quantity: %s", requested_quantity)
        raise ValueError("requested_quantity must be greater than 0")
    if requested_quantity <= available_stock:
        logger.info("Stock available for request of %s", requested_quantity)
        return True
    logger.warning(
        "Insufficient stock: requested %s, available %s",
        requested_quantity,
        available_stock,
    )
    return False


def main():
    """Interactive command-line demo of the inventory functions."""
    logger.info("Application started")
    try:
        name = input("Product name: ").strip()
        price = float(input("Price per unit: "))
        quantity = int(input("Quantity to buy: "))
        discount = float(input("Discount percent: "))
        stock = int(input("Available stock: "))

        logger.info("Product check: %s", name)
        if not check_stock(stock, quantity):
            print(f"Sorry, only {stock} units of '{name}' in stock.")
            return
        total = calculate_total_price(price, quantity)
        final = apply_discount(total, discount)
        print(f"Product: {name}")
        print(f"Total price: {total:.2f}")
        print(f"After {discount}% discount: {final:.2f}")
    except (TypeError, ValueError) as exc:
        logger.error("Operation failed: %s", exc)
        print(f"Error: {exc}")
    finally:
        logger.info("Application finished")


if __name__ == "__main__":
    main()
