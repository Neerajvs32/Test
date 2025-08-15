import unittest
import requests
import yaml
from termcolor import colored


class TestCustomURLs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load the URLs from the YAML file before running tests."""
        with open("url.yaml", "r") as file:
            try:
                cls.ymlData = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print("Error loading YAML:", exc)
                cls.ymlData = {}

    def test_main(self):
        """Test each URL and check if it returns HTTP 200."""
        url_list = self.ymlData.get("urls", [])
        success_count = 0
        failure_count = 0
        failed_urls = []  # Store failed URLs with their errors

        # Define a browser-like User-Agent header
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/58.0.3029.110 Safari/537.3"
        }

        print("\nTesting URLs...\n")
        for url in url_list:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                status_code = response.status_code

                if status_code == 200:
                    success_count += 1
                    print(colored(f'[SUCCESS] {url}', 'green'))
                else:
                    failure_count += 1
                    error_msg = f"{url} returned status code {status_code}"
                    failed_urls.append(error_msg)
                    print(colored(f'[ERROR] {url} - Status Code: {status_code}', 'red', attrs=['bold']))

            except requests.exceptions.RequestException as e:
                failure_count += 1
                error_msg = f"{url} is unreachable: {e}"
                failed_urls.append(error_msg)
                print(colored(f'[ERROR] {url} - {e}', 'red', attrs=['bold']))

        print("\nSummary Report:")
        print(colored(f"Total URLs tested: {len(url_list)}", "blue"))
        print(colored(f"Successful: {success_count}", "green"))
        print(colored(f"Failed: {failure_count}", "red"))

        # Only fail the test at the end if there were any failures
        if failed_urls:
            failure_summary = "\n".join(failed_urls)
            self.fail(f"The following URLs failed:\n{failure_summary}")


if __name__ == "__main__":
    unittest.main()