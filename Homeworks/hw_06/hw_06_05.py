"""
Завдання 5: Робота з XML.
Створи XML-файл, що містить інформацію про продукти магазину: назва продукту, ціна, кількість на складі.

    Напиши програму, яка:
-   Читає XML-файл і виводить назви продуктів та їхню кількість.
-   Змінює кількість товару та зберігає зміни в XML-файл.
"""

from xml.etree import ElementTree as ET
import xml.dom.minidom

# ---- Create inventory data ----
inventory = [
    {"Name": "Молоко", "Price": 25, "Quantity": 50},
    {"Name": "Хліб", "Price": 10, "Quantity": 100}
]

# ---- Create XML root element and add products as subelements ----
root = ET.Element('products')

for item in inventory:
    product = ET.SubElement(root, 'product')
    for key, value in item.items():
        detail = ET.SubElement(product, key)
        detail.text = str(value)

# ---- Write XML to file ----
tree = ET.ElementTree(root)
# tree.write('hw_06_05_products.xml', encoding='utf-8')

xml_str = ET.tostring(root, encoding='utf-8')
pretty_xml_str = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="    ")

with open("hw_06_05_products.xml", "w", encoding="utf-8") as file:
    file.write(pretty_xml_str)

# ---- Parse the created XML and print product names and prices ----
upd_tree = ET.parse("hw_06_05_products.xml")
upd_root = upd_tree.getroot()

for product in upd_root:
    for detail in product:
        if detail.tag == 'Name':
            print(f"Продукт: {detail.text}")
        elif detail.tag == 'Price':
            print(f"Ціна: {detail.text}")

# ---- Update product quantity, approach #1 ----
for product in upd_root:
    for name in product:
        if name.tag == 'Name' and name.text == 'Молоко':
            for qty in product:
                if qty.tag == 'Quantity':
                    qty.text = str(75)

# ---- Update product quantity, approach #2 ----
for product in upd_root.findall('product'):
    name = product.find('Name').text
    if name == 'Хліб':
        quantity = product.find('Quantity')
        quantity.text = str(120)

# ---- Write updated XML to the new file ----
tree = ET.ElementTree(upd_root)
tree.write('hw_06_05_products_updated.xml', encoding='utf-8')
