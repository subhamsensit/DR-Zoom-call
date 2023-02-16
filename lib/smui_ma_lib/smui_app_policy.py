from selenium.webdriver.common.by import By
from time import sleep
import variables
import logger


class SMUIAppPolicy:
    logger = logger.LogGen.loggen()

    MA_app_policy_windows_css = ".nav-menu-list-item[data-hash='policy-windows-settings']"
    MA_app_policy_delete_xpath = "//span[text()='" + variables.app_policy_name + "']/../..//span[@data-type='delete']"
    MA_app_policy_add_id = "add-windows-policy"
    MA_app_policy_name_css = ".form-input-text[data-form-element-name='name']"
    MA_app_policy_rule_order_xpath = "//*[@id=\"general\"]/div/div[2]/div[2]/div[1]/div[2]/div/span/span[1]"
    MA_app_policy_rule_order_1_xpath = "//*[@id=\"general\"]/div/div[2]/div[2]/div[1]/div[2]/div/div/ul/li[1]"
    MA_app_policy_enable_css = ".form-input-row .toggle-button[data-form-element-name='active']"
    MA_app_policy_all_groups_xpath = "//span[@class='radio-button groupSelectedType windows']//span[text()='All']"
    MA_app_policy_fwd_profile_list_css = ".dropdown[data-form-element-name='windows-onnet-filter']"
    MA_app_policy_fwd_profile_search_css = "input[id='filter-forwardingProfile-textwindows']"
    MA_app_policy_fwd_profile_complete_search_xpath = "//div[@id='windows-onnet-filter']//span[@class='search-icon fa fa-search']"
    MA_app_policy_new_fwd_profile_css = "li[data-name='" + variables.forwarding_profile_name + "']"
    MA_app_policy_save_css = ".button.primary.-js-mobile-save-button.policy"

    MA_policy_css = ".nav-menu[data-item='policy']"
    MA_dashboard_css = ".nav-menu[data-item='dashboard']"
    MA_administrator_css = ".nav-menu[data-item='administration']"
    MA_ok_xpath = "//span[text()='OK']"

    def __init__(self, chrome_driver):
        self.chrome_driver = chrome_driver

    def delete_app_policy(self):
        self.logger.info("******** Deleting APP Policy ********")
        self.logger.info("Navigating to App profiles")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_policy_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_app_policy_windows_css).click()
        sleep(2)

        self.logger.info("Deleting App policy")
        self.chrome_driver.find_element("xpath", self.MA_app_policy_delete_xpath).click()
        sleep(2)
        self.chrome_driver.find_element("xpath", self.MA_ok_xpath).click()
        sleep(2)
        self.logger.info("App policy deleted")

    def create_dtls_app_policy(self):
        self.logger.info("******** Creating App Policy ********")
        self.logger.info("Navigating to App profiles")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_policy_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_app_policy_windows_css).click()
        sleep(2)
        self.chrome_driver.find_element("id", self.MA_app_policy_add_id).click()
        sleep(2)

        self.logger.info("Creating policy")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_app_policy_name_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_app_policy_name_css).send_keys(
            variables.app_policy_name)
        sleep(2)
        self.chrome_driver.find_element("xpath", self.MA_app_policy_rule_order_xpath).click()
        sleep(2)
        self.chrome_driver.find_element("xpath", self.MA_app_policy_rule_order_1_xpath).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_app_policy_enable_css).click()
        sleep(2)
        self.chrome_driver.find_element("xpath", self.MA_app_policy_all_groups_xpath).click()
        sleep(2)

        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_app_policy_fwd_profile_list_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_app_policy_fwd_profile_search_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_app_policy_fwd_profile_search_css).send_keys(
            variables.forwarding_profile_name)
        sleep(2)
        self.chrome_driver.find_element("xpath", self.MA_app_policy_fwd_profile_complete_search_xpath).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_app_policy_new_fwd_profile_css).click()
        sleep(2)

        self.logger.info("Saving Policy")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_app_policy_save_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_dashboard_css).click()
        sleep(2)
        self.logger.info("App policy saved")
