from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from constants import CHROMEDRIVER_PATH


def initialize_webdriver():
    """
    Initialize and return a configured WebDriver for Chrome.

    Configures the WebDriver to start in maximized mode and incognito mode.

    Returns:
        driver (webdriver.Chrome): A configured instance of Chrome WebDriver.
    """
    # Create an instance of Chrome Options to specify desired browser settings
    chrome_options = Options()
    # Add option to start the browser maximized
    chrome_options.add_argument("--start-maximized")
    # Add option to start the browser in incognito mode for privacy
    chrome_options.add_argument("--incognito")

    # Create a Service object using the path to the ChromeDriver executable
    service = Service(executable_path=CHROMEDRIVER_PATH)
    # Initialize the Chrome WebDriver with the specified service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver  # Return the configured WebDriver instance
