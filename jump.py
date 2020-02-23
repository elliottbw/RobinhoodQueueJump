import selenium.webdriver
import selenium.webdriver.support.expected_conditions as expected_conditions
import selenium.common.exceptions

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

from random import choice
from string import ascii_letters


class QueueJumpBot:
    EMAIL_ENTRY_XPATH = "/html/body/div[1]/div[2]/div[1]/header[1]/div/div/div/div[1]/div[1]/div/div[3]/div/div/form/div/input"
    EMAIL_SUBMIT_XPATH = "/html/body/div[1]/div[2]/div[1]/header[1]/div/div/div/div[1]/div[1]/div/div[3]/div/div/form/div/div/button/span[2]/span"
    CLOSE_BUTTON_XPATH = "/html/body/div[5]/div/div[3]/div/div/header/div/button"
    NOT_YOU_XPATH = "/html/body/div[1]/div[3]/nav/div/div[2]/button"
    FAILED_XPATH = "/html/body/div[1]/div[1]/div[1]/header[1]/div/div/div/div[1]/div[1]/div/div[3]/div/div/form/div[2]/div/span"

    def __init__(self, firefox_binary_location: str, gecko_binary_location: str, headless=True, bot_id=0):
        self.firefox_options = Options()
        self.firefox_options.binary_location = firefox_binary_location
        self.firefox_options.headless = headless

        self.capabilities = DesiredCapabilities().FIREFOX
        self.capabilities["marionette"] = True

        self.driver = selenium.webdriver.Firefox(capabilities=self.capabilities,
                                                 options=self.firefox_options,
                                                 executable_path=gecko_binary_location)

        self.bot_id_string = f"on bot ID {bot_id}"

    def __del__(self):
        self.driver.quit()

    def _get_element_by_xpath(self, xpath: str):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.XPATH, xpath))
        )

    def load_robinhood(self, referral_code: str):
        self.driver.get(f"https://uk.robinhood.com/{referral_code}")

    def commit_referral(self, email: str):
        email_entry_element = self._get_element_by_xpath(self.EMAIL_ENTRY_XPATH)
        email_submit_element = self._get_element_by_xpath(self.EMAIL_SUBMIT_XPATH)

        email_entry_element.send_keys(email)
        email_submit_element.click()

        print(f"Referred email {email} {self.bot_id_string}")

        try:
            finished_element = self._get_element_by_xpath(self.CLOSE_BUTTON_XPATH)
            finished_element.click()
            not_you_element = self._get_element_by_xpath(self.NOT_YOU_XPATH)
            not_you_element.click()

        except selenium.common.exceptions.TimeoutException:
            try:
                failed_element = self._get_element_by_xpath(self.FAILED_XPATH)
                email_submit_element.click()

                finished_element = self._get_element_by_xpath(self.CLOSE_BUTTON_XPATH)
                finished_element.click()
                not_you_element = self._get_element_by_xpath(self.NOT_YOU_XPATH)
                not_you_element.click()
            except selenium.common.exceptions.TimeoutException:
                print(f"Failed to refer {self.bot_id_string}")

        print(f"Reset {self.bot_id_string}")

    @staticmethod
    def generate_random_email(length: int = 12, provider: str = "gmail") -> str:
        string = "".join([choice(ascii_letters) for _ in range(length)])
        email = f"{string}@{provider}.com"

        return email

