from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import variables
import logger


# self.chrome_driver = webdriver.Chrome(executable_path=variables.chrome_path)

class SMUI:
    logger = logger.LogGen.loggen()
    
    smui_login_username_id = "login-panel-input-email"
    smui_login_password_id = "login-panel-input-password"
    smui_login_signin_id = "login-panel-signin-button"
    smui_MA_option_xpath = "//*[@id=\"noprint\"]/div[8]/div/div[3]/span[2]"

    MA_policy_css = ".nav-menu[data-item='policy']"
    MA_dashboard_css = ".nav-menu[data-item='dashboard']"
    MA_administrator_css = ".nav-menu[data-item='administration']"
    MA_ok_xpath = "//span[text()='OK']"
    MA_ZCC_portal = "li[data-hash='mobile-portal']"

    def __init__(self, chrome_driver):
        self.chrome_driver = chrome_driver

    def login_smui_open_ma(self):
        self.logger.info("******** Opening MA From SMUI ********")
        self.logger.info("Logging into SMUI")
        self.chrome_driver.get(variables.smui_url)
        sleep(5)
        self.chrome_driver.maximize_window()

        self.chrome_driver.find_element("id", self.smui_login_username_id).click()
        self.chrome_driver.find_element("id", self.smui_login_username_id).send_keys(variables.login_id)
        sleep(5)

        self.chrome_driver.find_element("id", self.smui_login_password_id).click()
        self.chrome_driver.find_element("id", self.smui_login_password_id).send_keys(variables.login_pwd)
        sleep(5)

        self.chrome_driver.find_element("id", self.smui_login_signin_id).click()
        sleep(20)

        WebDriverWait(self.chrome_driver, 20).until(
            EC.presence_of_element_located(("xpath", self.smui_MA_option_xpath)))

        self.logger.info("Opening MA")
        self.chrome_driver.find_element("xpath", self.smui_MA_option_xpath).click()
        sleep(10)

        WebDriverWait(self.chrome_driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.MA_policy_css)))

        action = ActionChains(self.chrome_driver)
        policy_option = self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_policy_css)
        client_portal = self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_ZCC_portal)
        action.move_to_element(policy_option).click(client_portal).perform()
        sleep(10)

        self.chrome_driver.switch_to.window(self.chrome_driver.window_handles[1])
        self.logger.info("MA Opened")
