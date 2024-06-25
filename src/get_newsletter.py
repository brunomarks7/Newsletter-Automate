import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

from dotenv import load_dotenv

load_dotenv()

login_url = os.getenv("LOGIN_URL")
user_email = os.getenv("USER_EMAIL")
user_password = os.getenv("USER_PASSWORD")

current_directory = os.getcwd()
download_dir = os.path.join(current_directory, "downloads")
os.makedirs(download_dir, exist_ok=True)

chrome_options = Options()
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    },
)


def login():
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.quit()
        driver.get(login_url)

        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(
            By.CSS_SELECTOR, "button[data-qa='form-login-submit']"
        )

        username_field.send_keys(user_email)
        password_field.send_keys(user_password)
        login_button.click()

        time.sleep(10)

        assert "Projects" in driver.page_source

        item_card_email = driver.find_element(
            By.CSS_SELECTOR, "div[data-qa='itemCard_email']"
        )

        actions = ActionChains(driver)

        actions.move_to_element(item_card_email).perform()
        target_div = driver.find_element(By.CSS_SELECTOR, "div.top[tabindex='0']")
        secondary_button = target_div.find_element(
            By.CSS_SELECTOR, "button[data-qa='secondary-button']"
        )
        secondary_button.click()

        download_button = driver.find_element(
            By.XPATH,
            "//*[@id='app']/div/main/div/div/div[2]/div/div[2]/div[1]/div/div/div[1]/div/article/div/div[3]/div/div/ul/li[4]",
        )

        before_click_files = set(os.listdir(download_dir))

        download_button.click()

        time.sleep(5)

        export_modal_zip = driver.find_element(
            By.CSS_SELECTOR, "div[data-qa='export_modal_zip']"
        )

        export_modal_zip.click()

        time.sleep(20)

        after_click_files = set(os.listdir(download_dir))

        new_files = after_click_files - before_click_files

        zip_downloaded = any(file.endswith(".zip") for file in new_files)

        if zip_downloaded:
            print("O arquivo ZIP foi baixado com sucesso.")
        else:
            print("O download do arquivo ZIP não foi iniciado.")

    finally:
        driver.quit()


if __name__ == "__main__":
    login()
