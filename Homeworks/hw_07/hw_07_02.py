"""
    Завдання 2. Мокування за допомогою unittest.mock.

    Напишіть програму для отримання даних з веб-сайту та протестуйте його
за допомогою моків. Напишіть клас WebService, який має метод get_data(url: str) -> dict.
Цей метод повинен використовувати бібліотеку requests, щоб робити GET-запит
та повертати JSON-відповідь. Використовуйте unittest.mock для макування HTTP-запитів.
Замокуйте метод requests.get таким чином, щоб він повертав фейкову відповідь
(наприклад, {"data": "test"}), та протестуйте метод get_data.

    Напишіть кілька тестів:
-   перевірка успішного запиту (200);
-   перевірка обробки помилки (404 чи інші коди).
"""

import unittest.mock

import requests


class WebService:
    """
    Represent a web service for fetching data from a URL.

    The WebService class provides a method to get JSON data from a URL using a GET request.
    """

    @staticmethod
    def get_data(url):
        """
        Get JSON data from the specified URL.

        :param url: The URL to send the GET request to.
        :type url: str
        :return: The JSON data from the response.
        :rtype: dict
        """
        response = requests.get(url, timeout=30)
        return response.json()


class TestWebService(unittest.TestCase):
    """
    Represent the test cases for the WebService class.

    The TestWebService class contains unit tests for the WebService class, focusing on the success
    and error scenarios of the get_data method.
    """

    @unittest.mock.patch('requests.get')
    def test_get_data_success(self, mock_success):
        """
        Test get_data method when the GET request is successful.

        This test mocks the requests.get method to simulate a successful response
        with status code 200 and a valid JSON body.

        :param mock_success: Mock object for requests.get
        :type mock_success: unittest.mock.Mock
        """
        mock_success.return_value.status_code = 200
        mock_success.return_value.json.return_value = {"data": "test"}

        service = WebService()
        result = service.get_data("https://somerandomurl.com")

        self.assertEqual(result, {"data": "test"})

    @unittest.mock.patch('requests.get')
    def test_get_data_error(self, mock_error):
        """
        Test get_data method when the GET request returns an error.

        This test mocks the requests.get method to simulate a failed response
        with status code 400 and an error JSON body.

        :param mock_error: Mock object for requests.get
        :type mock_error: unittest.mock.Mock
        """
        mock_error.return_value.status_code = 400
        mock_error.return_value.json.return_value = {"error": "not found"}

        service = WebService()
        result = service.get_data("https://somerandomurl.com")

        self.assertEqual(result, {"error": "not found"})


# ---- Main Execution ----
if __name__ == "__main__":
    unittest.main()
