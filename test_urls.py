import unittest
import requests
import yaml
from termcolor import colored


class TestCustomURLs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load the URLs from the YAML file before running tests."""
        with open("urls.yaml", "r") as file:
            try:
                cls.ymlData = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print("Error loading YAML:", exc)
                cls.ymlData = {}

    def test_urls(self):
        """Test each URL and check if it returns HTTP 200."""
        url_list = self.ymlData.get("urls", [])
        success_count = 0
        failure_count = 0

        print("\nTesting URLs...\n")
        for url in url_list:
            try:
                response = requests.get(url, timeout=10)
                status_code = response.status_code

                if status_code == 200:
                    success_count += 1
                    print(colored(f'[SUCCESS] {url}', 'green'))
                else:
                    failure_count += 1
                    print(colored(f'[ERROR] {url} - Status Code: {status_code}', 'red', attrs=['bold']))
                
                self.assertEqual(status_code, 200, f"{url} returned {status_code}")

            except requests.exceptions.RequestException as e:
                failure_count += 1
                print(colored(f'[ERROR] {url} - {e}', 'red', attrs=['bold']))
                self.fail(f"{url} is unreachable: {e}")

        print("\nSummary Report:")
        print(colored(f"Total URLs tested hi: {len(url_list)}", "blue"))
        print(colored(f"Successful: {success_count}", "green"))
        print(colored(f"Failed: {failure_count}", "red"))

if __name__ == "__main__":
    unittest.main()

