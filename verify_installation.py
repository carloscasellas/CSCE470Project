# Verify installation
import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.curiouscuisiniere.com")
if response.status_code == 200:
    print("Requests library working correctly!")
    soup = BeautifulSoup(response.content, "html.parser")
    print("BeautifulSoup imported successfully!")
else:
    print(f"Failed to connect: {response.status_code}")