import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from constants import (
    LOAD_MORE_BUTTON_SELECTOR,
    ITEM_LINK_SELECTOR,
    DETAIL_SECTION_SELECTOR,
    DETAIL_ROW_SELECTOR,
    ROW_TITLE_SELECTOR,
    ROW_VALUE_SELECTOR,
    SCROLL_DELAY,
)


def retrieve_item_links(driver, number_of_items):
    """
    Retrieve a batch of item links from the main page.

    Parameters:
        driver (webdriver.Chrome): The WebDriver instance used for scraping.
        number_of_items (int): The number of item links to retrieve.

    Returns:
        list: A list of item links retrieved from the page.
    """
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds for elements to be present
    try:
        # Wait for all item links to be located using the specified CSS selector
        items = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ITEM_LINK_SELECTOR))
        )
        item_links = []  # List to store retrieved item links
        for item in items[:number_of_items]:
            try:
                # Append the href attribute of each item link to the list
                item_links.append(item.get_attribute("href"))
            except StaleElementReferenceException:
                # Handle the case where the element reference becomes stale
                print("Encountered a stale element reference, retrying...")
                items = driver.find_elements(By.CSS_SELECTOR, ITEM_LINK_SELECTOR)
                item_links.append(items[item.index(item)].get_attribute("href"))
        return item_links
    except TimeoutException:
        # Handle the case where item links do not load within the timeout period
        print("Timeout waiting for item links to load")
        return []


def scroll_and_load_more_items(driver):
    """
    Scroll down and click the 'Load more Items' button if present.

    Parameters:
        driver (webdriver.Chrome): The WebDriver instance used for scraping.
    """
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Attempt to find the 'Load more Items' button using the specified CSS selector
        load_more_button = driver.find_element(
            By.CSS_SELECTOR, LOAD_MORE_BUTTON_SELECTOR
        )
        if load_more_button.is_displayed():
            # Click the button if it is displayed
            load_more_button.click()
            print("Clicked 'Load more Items' button")
            # Wait for a specified delay to allow new items to load
            time.sleep(SCROLL_DELAY)
    except NoSuchElementException:
        # Handle the case where the 'Load more Items' button is not found
        print("No 'Load more Items' button found")
    except Exception as e:
        # Handle any other exceptions that may occur
        print(f"Error scrolling and loading more items: {e}")


def scrape_item_details(driver, link):
    """
    Fetch details of an item from its details page.

    Parameters:
        driver (webdriver.Chrome): The WebDriver instance used for scraping.
        link (str): The URL of the item's details page.

    Returns:
        dict: A dictionary containing the item's details.
    """
    # Open the item link in a new browser tab
    driver.execute_script("window.open(arguments[0], '_blank');", link)
    driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab

    item_data = {}  # Dictionary to store the item details

    try:
        # Wait for the details section to be present in the new tab
        details_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, DETAIL_SECTION_SELECTOR))
        )

        # Extract brand and model information
        brand_model_element = details_section.find_element(
            By.CSS_SELECTOR, "div.kt-base-row__end a"
        )
        brand_model = brand_model_element.text.strip()  # Get and clean the text
        item_data["برند و مدل"] = brand_model  # Store it in the dictionary

        # Extract other details from the details section
        rows = details_section.find_elements(By.CSS_SELECTOR, DETAIL_ROW_SELECTOR)
        for row in rows:
            try:
                title_element = row.find_element(By.CSS_SELECTOR, ROW_TITLE_SELECTOR)
                try:
                    value_element = row.find_element(
                        By.CSS_SELECTOR, ROW_VALUE_SELECTOR
                    )
                except NoSuchElementException:
                    # Handle cases where the value is contained in a different element
                    value_element = row.find_element(
                        By.CSS_SELECTOR, "a.kt-unexpandable-row__action"
                    )
                title = title_element.text.strip()  # Clean the title text
                value = value_element.text.strip()  # Clean the value text
                item_data[title] = value  # Store the detail in the dictionary
            except Exception as e:
                # Handle any exceptions that occur while extracting details
                print(f"Error extracting item detail: {e}")

    except TimeoutException:
        # Handle the case where the details section does not load within the timeout period
        print(f"Timeout waiting for item details to load for {link}")
    except Exception as e:
        # Handle any other exceptions that may occur
        print(f"Error processing item {link}: {e}")

    # Close the current tab and switch back to the main page tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return item_data  # Return the dictionary containing the item details
