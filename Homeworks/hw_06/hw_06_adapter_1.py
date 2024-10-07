"""
1) Перетворення між форматами:

Реалізуй класи, які перетворюватимуть CSV-файл до JSON та навпаки.
Додай функціонал для перетворення XML-файлу до JSON.
"""

import csv
import json
import xmltodict


class CSVToJSON:
    """
    Convert CSV to JSON format.

    :param csv_file: Path to the input CSV file.
    :type csv_file: str
    """
    def __init__(self, csv_file):
        """
        Initialize the CSVToJSON class with the input CSV file.

        :param csv_file: Path to the input CSV file.
        :type csv_file: str
        """
        self.csv_file = csv_file

    def convert(self, json_file):
        """
        Convert the CSV file to JSON format and write it to the output file.

        :param json_file: Path to the output JSON file.
        :type json_file: str
        """
        # ---- Reading CSV and converting to JSON ----
        with open(self.csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = []
            for row in reader:
                data.append(row)

        # ---- Writing JSON to file ----
        with open(json_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)


class JSONToCSV:
    """
    Convert JSON to CSV format.

    :param json_file: Path to the input JSON file.
    :type json_file: str
    """
    def __init__(self, json_file):
        """
        Initialize the JSONToCSV class with the input JSON file.

        :param json_file: Path to the input JSON file.
        :type json_file: str
        """
        self.json_file = json_file

    def convert(self, csv_file):
        """
        Convert the JSON file to CSV format and write it to the output file.

        :param csv_file: Path to the output CSV file.
        :type csv_file: str
        """
        # ---- Reading JSON and converting to CSV ----
        with open(self.json_file, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)

        # ---- Writing CSV to file ----
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


class XMLToJSON:
    """
    Convert XML to JSON format.

    :param xml_file: Path to the input XML file.
    :type xml_file: str
    """
    def __init__(self, xml_file):
        """
        Initialize the XMLToJSON class with the input XML file.

        :param xml_file: Path to the input XML file.
        :type xml_file: str
        """
        self.xml_file = xml_file

    def convert(self, json_file):
        """
        Convert the XML file to JSON format and write it to the output file.

        :param json_file: Path to the output JSON file.
        :type json_file: str
        """
        # ---- Reading XML and converting to JSON ----
        with open(self.xml_file) as xmlfile:
            # я намагався через ручний парсинг, але не зміг перемогти парсинг сабелементів з однаковим тегом
            doc = xmltodict.parse(xmlfile.read(), process_namespaces=True)

        # ---- Writing JSON to file ----
        with open(json_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(doc, jsonfile, ensure_ascii=False, indent=4)


# ---- Creating objects and converting files ----
csv_to_json = CSVToJSON("hw_06_03_list.csv")
csv_to_json.convert("hw_06_adapter_1_from_csv.json")

json_to_csv = JSONToCSV("hw_06_04_list.json")
json_to_csv.convert("hw_06_adapter_1_from_json.csv")

xml_to_json = XMLToJSON("hw_06_05_products.xml")
xml_to_json.convert("hw_06_adapter_1_from_xml.json")
