import requests

url = 'https://pypi.org/'

response = requests.get(url)

if response.status_code == 200:
    with open("hw_06_02_output.txt", 'w') as output:
        output.write(response.text)
        print("Page content successfully saved.")
else:
    print(f"Couldn't load the page. Status code {response.status_code}")
