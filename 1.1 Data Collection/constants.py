# Path to the ChromeDriver executable for Selenium WebDriver
CHROMEDRIVER_PATH = "./chromedriver.exe"

# Base URL for the Divar website's mobile phones section in Tehran
BASE_URL = "https://divar.ir/s/tehran/mobile-phones"

# Headers for the CSV file where item details will be saved
CSV_HEADERS = [
    "برند و مدل",  # Brand and model of the mobile phone
    "وضعیت",  # Condition of the phone (e.g., new, used)
    "تعداد سیم‌کارت",  # Number of SIM cards supported
    "اصالت برند",  # Brand authenticity
    "حافظهٔ داخلی",  # Internal storage capacity
    "مقدار رم",  # RAM size
    "قیمت",  # Price of the mobile phone
    "رنگ",  # Color of the phone
]

# Number of items to retrieve per batch during scraping
ITEMS_PER_BATCH = 12

# Filename for the CSV file where item details will be saved
CSV_FILENAME = "item_details.csv"

# Delay (in seconds) between scrolling actions to allow the page to load new content
SCROLL_DELAY = 3

# CSS Selectors for various elements on the website
LOAD_MORE_BUTTON_SELECTOR = (
    "button.post-list__load-more-btn-d46f4"  # Selector for the "Load more Items" button
)
ITEM_LINK_SELECTOR = (
    "div.post-list__widget-col-a3fe3 a"  # Selector for item links on the main page
)
DETAIL_SECTION_SELECTOR = (
    "div.post-page__section--padded"  # Selector for the details section on item pages
)
DETAIL_ROW_SELECTOR = (
    "div.kt-base-row"  # Selector for individual rows in the details section
)
ROW_TITLE_SELECTOR = "p.kt-base-row__title"  # Selector for the title of each detail row
ROW_VALUE_SELECTOR = (
    "p.kt-unexpandable-row__value"  # Selector for the value of each detail row
)
