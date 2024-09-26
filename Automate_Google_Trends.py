import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    # Set up Chrome options to disable the "Chrome is being controlled" message
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Initialize the Chrome WebDriver with the modified options
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def open_google_trends(driver, search_input):
    # Open the Google Trends website
    driver.get(f'https://trends.google.com/trends/?date=today 3-m&q={search_input}&hl=en')

def search_term(driver, term):
    # Wait for the search input to be available and locate it by its id
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'i7'))
    )
    # Search for the specified term
    search_box.send_keys(term)

    # Wait for the "Explore" button to become clickable and click it
    explore_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Explore']]"))
    )
    explore_button.click()

def download_csv(driver):
    # Wait for the page to load results
    time.sleep(5)

    # Wait for the "Download CSV" button to become clickable and click it
    download_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'export') and @title='CSV']"))
    )
    # download_button.click()

    # Wait for the download to complete
    time.sleep(1)

def scroll_to_related_queries_section(driver):
    """Scroll down to the 'Related queries' section and ensure it's visible."""
    wait = WebDriverWait(driver, 10)

    while True:
        try:
            # Try to locate the 'Related queries' header using WebDriverWait to wait until it is present in the DOM
            related_queries_section = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'fe-atoms-generic-title') and contains(text(), 'Related queries')]")
            ))

            # Scroll to the 'Related queries' section
            driver.execute_script("arguments[0].scrollIntoView(true);", related_queries_section)
            return related_queries_section
        except Exception as e:
            # Scroll down if the section is not found yet, until we reach the bottom of the page
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)  # Pause for the scroll to take effect

def repeat_search_and_download(driver, term):
    # Locate the new search input for adding a new search term
    new_search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'input-29'))
    )

    # Add the same search term again
    new_search_box.send_keys(term)

    # Wait for a moment before submitting the search
    time.sleep(2)

    # Simulate pressing enter to search
    new_search_box.send_keys(Keys.ENTER)

    # Wait for the new search results to load
    time.sleep(5)

    # Scroll to the 'Related queries' section
    related_queries_section = scroll_to_related_queries_section(driver)

    # Once in view, find the download button within this section's widget-actions div
    csv_button_xpath = ".//following-sibling::widget-actions//button[@title='CSV']"
    download_button = related_queries_section.find_element(By.XPATH, csv_button_xpath)

    # Scroll to the button to ensure it is visible
    driver.execute_script("arguments[0].scrollIntoView(true);", download_button)

    # Click the download button
    download_button.click()

    # Wait for the download to complete (adjust timing as necessary)
    time.sleep(5)

def main():
    # Main function to run the workflow
    search_input = input("Please enter a search term: ")
    driver = setup_driver()
    try:
        open_google_trends(driver, search_input)
        search_term(driver, search_input)
        download_csv(driver)
        repeat_search_and_download(driver, search_input)
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
