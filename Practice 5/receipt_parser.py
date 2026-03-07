import re
import json


def money_to_float(s):
    return float(s.replace(" ", "").replace(",", "."))


def parse_receipt(text):
    result = {
        "branch": None,
        "bin": None,
        "cash_register": None,
        "shift": None,
        "receipt_order_number": None,
        "receipt_number": None,
        "cashier": None,
        "date": None,
        "time": None,
        "payment_method": None,
        "all_prices": [],
        "products": [],
        "total_amount": 0.0
    }

    branch_match = re.search(r"Филиал\s+(.+)", text)
    if branch_match:
        result["branch"] = branch_match.group(1).strip()

    bin_match = re.search(r"БИН\s+(\d+)", text)
    if bin_match:
        result["bin"] = bin_match.group(1)

    cash_register_match = re.search(r"Касса\s+([^\n]+)", text)
    if cash_register_match:
        result["cash_register"] = cash_register_match.group(1).strip()

    shift_match = re.search(r"Смена\s+([^\n]+)", text)
    if shift_match:
        result["shift"] = shift_match.group(1).strip()

    order_match = re.search(r"Порядковый номер чека\s*№\s*(\d+)", text)
    if order_match:
        result["receipt_order_number"] = order_match.group(1)

    receipt_match = re.search(r"Чек\s*№\s*(\d+)", text)
    if receipt_match:
        result["receipt_number"] = receipt_match.group(1)

    cashier_match = re.search(r"Кассир\s+([^\n]+)", text)
    if cashier_match:
        result["cashier"] = cashier_match.group(1).strip()

    datetime_match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
    if datetime_match:
        result["date"] = datetime_match.group(1)
        result["time"] = datetime_match.group(2)

    payment_match = re.search(r"(Банковская карта|Наличные|Карта)\s*:", text, re.IGNORECASE)
    if payment_match:
        result["payment_method"] = payment_match.group(1)

    prices = re.findall(r"\d[\d ]*,\d{2}", text)
    result["all_prices"] = [money_to_float(price) for price in prices]

    product_pattern = re.compile(
        r"(\d+)\.\n"                            # номер товара
        r"(.+?)\n"                              # название
        r"(\d+,\d{3})\s*x\s*(\d[\d ]*,\d{2})\n" # количество x цена
        r"(\d[\d ]*,\d{2})\n"                   # сумма
        r"Стоимость\n"
        r"(\d[\d ]*,\d{2})",                    # стоимость
        re.MULTILINE
    )

    product_matches = product_pattern.findall(text)

    for match in product_matches:
        item_number, name, quantity, unit_price, subtotal, total_price = match

        product = {
            "item_number": int(item_number),
            "name": name.strip(),
            "quantity": float(quantity.replace(",", ".")),
            "unit_price": money_to_float(unit_price),
            "subtotal": money_to_float(subtotal),
            "total_price": money_to_float(total_price)
        }

        result["products"].append(product)

    total_match = re.search(r"ИТОГО:\n(\d[\d ]*,\d{2})", text)
    if total_match:
        result["total_amount"] = money_to_float(total_match.group(1))
    else:
        result["total_amount"] = round(sum(item["total_price"] for item in result["products"]), 2)

    return result


def print_receipt(data):
    print("=== RECEIPT DATA ===")
    print("Branch:", data["branch"])
    print("BIN:", data["bin"])
    print("Cash register:", data["cash_register"])
    print("Shift:", data["shift"])
    print("Receipt order number:", data["receipt_order_number"])
    print("Receipt number:", data["receipt_number"])
    print("Cashier:", data["cashier"])
    print("Date:", data["date"])
    print("Time:", data["time"])
    print("Payment method:", data["payment_method"])
    print("Total amount:", data["total_amount"])
    print()

    print("=== PRODUCTS ===")
    for product in data["products"]:
        print(f"{product['item_number']}. {product['name']}")
        print("   Quantity:", product["quantity"])
        print("   Unit price:", product["unit_price"])
        print("   Subtotal:", product["subtotal"])
        print("   Total price:", product["total_price"])
        print()

    print("=== ALL PRICES ===")
    print(data["all_prices"])
    print()

    print("=== JSON ===")
    print(json.dumps(data, ensure_ascii=False, indent=4))


def main():
    with open("raw.txt", "r", encoding="utf-8") as file:
        text = file.read()

    data = parse_receipt(text)
    print_receipt(data)


if __name__ == "__main__":
    main()