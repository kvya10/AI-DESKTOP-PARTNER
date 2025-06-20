from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import WebDriverException

def search_youtube(query):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open YouTube
        driver.get("https://www.youtube.com")

        # Wait for page to load
        time.sleep(3)

        # Find the YouTube search bar
        search_bar = driver.find_element(By.NAME, "search_query")

        # Clear any pre-filled text (just a precaution)
        search_bar.clear()

        # Type the query into the search bar
        search_bar.send_keys(query)

        # Press Enter to search
        search_bar.send_keys(Keys.RETURN)

        # Wait for the search results page to load
        time.sleep(3)

        # Click on the first video
        first_video = driver.find_element(By.XPATH, '(//a[@id="video-title"])[1]')
        first_video.click()

        # Keep checking if the window is still open
        while True:
            try:
                # Try interacting with the window to check if it's still open
                driver.current_url  # If window is closed, this will raise an exception
                time.sleep(1)  # Wait before checking again
            except WebDriverException:
                print("Browser window closed by user.")
                break

    finally:
        driver.quit()  # Ensure the driver quits when the window is closed

# Call the function with your desired query
if __name__ == "_main_":
    query = input("enter the song")
    search_youtube(query)