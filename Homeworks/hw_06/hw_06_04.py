"""
Завдання 4: Робота з JSON
Створи JSON-файл з інформацією про книги, кожна книга повинна мати: назву, автора, рік видання,
наявність (True або False).

    Напиши програму, яка:
-   Завантажує JSON-файл.
-   Виводить список доступних книг (наявність True).
-   Додає нову книгу в цей файл.
"""

import json
from pprint import pprint

# ---- Define the initial catalog of books ----
catalog = [
    {"назва": "To Kill a Mockingbird", "автор": "Harper Lee", "рік": 1960, "наявність": True},
    {"назва": "1984", "автор": "George Orwell", "рік": 1949, "наявність": False},
    {"назва": "The Great Gatsby", "автор": "F. Scott Fitzgerald", "рік": 1925, "наявність": True},
    {"назва": "Pride and Prejudice", "автор": "Jane Austen", "рік": 1813, "наявність": True},
    {"назва": "The Catcher in the Rye", "автор": "J.D. Salinger", "рік": 1951, "наявність": False},
    {"назва": "The Hobbit", "автор": "J.R.R. Tolkien", "рік": 1937, "наявність": True},
    {"назва": "Brave New World", "автор": "Aldous Huxley", "рік": 1932, "наявність": True}
]

# ---- Write the catalog to a JSON file ----
with open("hw_06_04_list.json", 'w', encoding='utf-8') as file:
    json.dump(catalog, file, ensure_ascii=False, indent=4)

# ---- Load the books from the JSON file and print available ones ----
with open("hw_06_04_list.json", 'r', encoding='utf-8') as file:
    books = json.load(file)
    # print(json.dumps(books, ensure_ascii=False, indent=4))
    # pprint(books, width=40, sort_dicts=False)
    print("\nКниги у наявності:")
    for book in books:
        if book['наявність']:
            print(f"- {book['назва']}")

# ---- Define more books to add to the catalog ----
more_books = [
    {"назва": "The Alchemist", "автор": "Paulo Coelho", "рік": 1988, "наявність": False},
    {"назва": "The Da Vinci Code", "автор": "Dan Brown", "рік": 2003, "наявність": True}
]

# ---- Add the new books to the list and write to an updated JSON file ----
# Зробив окремий файл для цього пункту для наглядності
with open("hw_06_04_list_updated.json", 'w', encoding='utf-8') as file:
    books.extend(more_books)
    json.dump(books, file, ensure_ascii=False, indent=4)
    print(f"\nДодано до списку:")
    for book in more_books:
        print(f"- {book['назва']}")
