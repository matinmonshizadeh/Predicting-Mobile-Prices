import time
from webdriver_setup import initialize_webdriver
from item_scraper import (
    retrieve_item_links,
    scroll_and_load_more_items,
    scrape_item_details,
)
from csv_handler import initialize_csv_writer
from constants import BASE_URL, CSV_HEADERS, ITEMS_PER_BATCH, CSV_FILENAME, SCROLL_DELAY


def main():
    # Initialize the WebDriver instance using the custom setup function
    driver = initialize_webdriver()

    try:
        # Open the target URL with the WebDriver
        driver.get(BASE_URL)

        # Initialize the CSV writer to handle CSV file operations
        csv_writer = initialize_csv_writer(CSV_FILENAME, CSV_HEADERS)
        csv_writer.initialize()  # Create and prepare the CSV file

        batch_count = 0  # Initialize batch counter
        while True:
            batch_count += 1  # Increment the batch counter for each loop iteration

            # Scroll down the page and load more items if necessary
            scroll_and_load_more_items(driver)

            # Retrieve item links for the current batch from the webpage
            item_links = retrieve_item_links(driver, ITEMS_PER_BATCH)
            if not item_links:
                break  # Exit the loop if no more items are found

            # Iterate through each link retrieved in the current batch
            for link in item_links:
                # Scrape item details from each link
                item_data = scrape_item_details(driver, link)
                # Prepare a row of data to write to the CSV file
                csv_row = [item_data.get(header, "") for header in CSV_HEADERS]
                csv_writer.write_row(csv_row)  # Write the item details to the CSV file
                print(f"Saved item details to CSV: {csv_row}")

                # Add a delay to avoid getting banned due to frequent requests
                time.sleep(SCROLL_DELAY)  # Pause between processing each item

            # Scroll down the page to load the next batch of items
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print(f"Scrolled down to load next batch ({batch_count + 1})")
            except Exception as e:
                # Print an error message if scrolling fails
                print(f"Error scrolling down for next batch ({batch_count + 1}): {e}")

        # Flush and close the CSV writer to ensure all data is written
        csv_writer.close()

    finally:
        # Close the WebDriver to clean up resources
        driver.quit()
        print("Script execution completed successfully.")


if __name__ == "__main__":
    main()
