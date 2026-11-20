"""Pytest test cases for inventory.py."""

import pytest

from inventory import apply_discount, calculate_total_price, check_stock


# ---- calculate_total_price ----
def test_total_price_valid():
    assert calculate_total_price(10.5, 4) == pytest.approx(42.0)


def test_total_price_zero_quantity_boundary():
    assert calculate_total_price(99.99, 0) == 0


def test_total_price_negative_price():
    with pytest.raises(ValueError):
        calculate_total_price(-1, 2)


def test_total_price_negative_quantity():
    with pytest.raises(ValueError):
        calculate_total_price(10, -2)


@pytest.mark.parametrize("price, qty", [("10", 2), (10, 2.5), (None, 1), (True, 1)])
def test_total_price_invalid_types(price, qty):
    with pytest.raises(TypeError):
        calculate_total_price(price, qty)


# ---- apply_discount ----
def test_discount_valid():
    assert apply_discount(200, 10) == pytest.approx(180.0)


@pytest.mark.parametrize("percent, expected", [(0, 500), (100, 0)])
def test_discount_boundaries(percent, expected):
    assert apply_discount(500, percent) == pytest.approx(expected)


@pytest.mark.parametrize("percent", [-5, 100.01, 150])
def test_discount_out_of_range(percent):
    with pytest.raises(ValueError):
        apply_discount(100, percent)


def test_discount_negative_total():
    with pytest.raises(ValueError):
        apply_discount(-100, 10)


def test_discount_invalid_type():
    with pytest.raises(TypeError):
        apply_discount("100", 10)


# ---- check_stock ----
def test_stock_sufficient():
    assert check_stock(10, 5) is True


def test_stock_exact_boundary():
    assert check_stock(5, 5) is True


def test_stock_insufficient():
    assert check_stock(3, 5) is False


def test_stock_empty():
    assert check_stock(0, 1) is False


@pytest.mark.parametrize("stock, requested", [(10, 0), (10, -3), (-1, 2)])
def test_stock_invalid_values(stock, requested):
    with pytest.raises(ValueError):
        check_stock(stock, requested)


def test_stock_invalid_type():
    with pytest.raises(TypeError):
        check_stock(10, "5")
