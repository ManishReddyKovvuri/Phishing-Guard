from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# Set up Chrome options (optional)
from selenium.webdriver.chrome.options import Options

def get_redirected_url(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without GUI (headless mode)
    chrome_options.add_argument("--no-sandbox")  # Useful for environments like Docker

    # Set up Chrome driver using WebDriver Manager
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Open a website
    driver.get("https://www.google.com")

    # Print the page title to verify
    print("Page title is:", driver.title)

    #url="https://toptier-cleaners.com/"

    print (url)
    try:
            driver.get(url)
            # Wait until page is loaded to a reasonable state (you can adjust this as necessary)
            wait = WebDriverWait(driver, 10)
            wait.until(ec.presence_of_element_located((By.TAG_NAME, 'body')))
            cur_url = driver.current_url  # Get the final URL after potential redirection

            return True, cur_url
    except WebDriverException as e :
            # Return false if an error occurred (e.g., the page didn't load properly)
            return False, e.msg
    finally:
            driver.quit() 


