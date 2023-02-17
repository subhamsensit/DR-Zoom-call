from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep
import variables
import zscaler_logger


class SMUIFwdProfile:
    logger = logger.LogGen.loggen()

    MA_fwd_profile_css = ".nav-menu-list-item[data-hash*='onnet']"
    MA_fwd_profile_delete_xpath = "//span[text()='" + variables.forwarding_profile_name + "']/../..//span[@data-type='delete']"
    MA_fwd_profile_add_css = "#add-onnet-policy .control-button.-js-add-button"
    MA_fwd_profile_name_css = "input[data-form-element-name='name']"
    MA_fwd_profile_pkt_filter_xpath = "//span[contains(text(),'Packet Filter Based')]"
    MA_fwd_profile_tunnel_xpath = "//*[@id='general']//span[@class='radio-button-text'][normalize-space()='Tunnel']"

    MA_fwd_profile_tunnel_v2_xpath = "//div[@class='network-config1']//div[contains(@class,'tunnelSelection')]//span[contains(text(),'Tunnel 2.0')]"
    MA_fwd_profile_tunnel_v2_tunnel_type_xpath = "//div[@class='network-config1']//div[contains(@class,'advancedTunnelSelection')]//span[contains(text(),'Transport Settings')]"
    MA_fwd_profile_tunnel_v2_tls_xpath = "//div[@class='network-config1']//div[contains(@class,'transportSelection')]//span[text()='TLS']"
    MA_fwd_profile_tunnel_v1_xpath = "//div[@class='network-config1']//div[contains(@class,'tunnelSelection')]//span[contains(text(),'Tunnel 1.0')]"
    MA_fwd_profile_enforce_proxy_xpath = "//div[@class='network-config1']//span[text()='Enforce Proxy']"
    MA_fwd_profile_none_xpath = "//div[@class='network-config1']//span[text()='None']"
    MA_fwd_profile_TWLP_xpath = "//div[@class='network-config1']//span[text()='Tunnel with Local Proxy']"

    MA_fwd_profile_vpn_same_as_trusted_css = ".network-config2 .check-box-button.sameAsTrusted"
    MS_fwd_profile_other_same_as_trusted_css = ".network-config3 .check-box-button.sameAsTrusted"
    MA_fwd_profile_save_id = "administration-onnet-config-save"

    MA_fwd_profile_edit_xpath = "//span[text()='" + variables.forwarding_profile_name + "']/../..//span[@data-type='edit']"

    MA_fwd_profile_dynamic_zen_xpath = "//*[@id=\"latencyBasedZenContainer_0\"]/div[2]/span/span[3]"
    MA_fwd_profile_probe_interval_dropdown_xpath = "//*[@id=\"latencyBasedZenContainer_0\"]/div[3]/div[1]/div[2]/div/span"
    MA_fwd_profile_probe_interval_30_xpath = "//*[@id=\"latencyBasedZenContainer_0\"]/div[3]/div[1]/div[2]/div/div/ul/li[1]"
    MA_fwd_profile_probe_interval_60_xpath = "//*[@id=\"latencyBasedZenContainer_0\"]/div[3]/div[1]/div[2]/div/div/ul/li[2]"

    MA_fwd_profile_sample_size_dropdown_xpath = "//*[@id=\"latencyBasedZenContainer_0\"]/div[3]/div[2]/div[2]/div/span"
    MA_fwd_profile_sample_size_3_xpath = "//*[@id=\"latencyBasedZenContainer_0\"]/div[3]/div[2]/div[2]/div/div/ul/li[3]"
    MA_fwd_profile_sample_size_2_xpath = "//*[@id=\"latencyBasedZenContainer_0\"]/div[3]/div[2]/div[2]/div/div/ul/li[2]"

    MA_fwd_profile_threshold_xpath = "//*[@id=\"latencyBasedZenContainer_0\"]/div[3]/div[3]/div[2]/input"

    MA_policy_css = ".nav-menu[data-item='policy']"
    MA_dashboard_css = ".nav-menu[data-item='dashboard']"
    MA_administrator_css = ".nav-menu[data-item='administration']"
    MA_ok_xpath = "//span[text()='OK']"

    def __init__(self, chrome_driver):
        self.chrome_driver = chrome_driver

    def delete_forwarding_profile(self):
        self.logger.info("******** Deleting Forwarding Profile ********")
        self.logger.info("Navigating to Forwarding profiles")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_administrator_css).click()
        sleep(5)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_css).click()
        sleep(5)

        self.logger.info("Deleting Forwarding profile")
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_delete_xpath).click()
        sleep(2)
        self.chrome_driver.find_element("xpath", self.MA_ok_xpath).click()
        sleep(10)
        self.logger.info("Forwarding profile deleted")

    def create_dtls_forwarding_profile(self):
        self.logger.info("******** Creating DTLS Forwarding Profile ********")
        self.logger.info("Navigating to Forwarding profiles")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_administrator_css).click()
        sleep(5)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_css).click()
        sleep(5)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_add_css).click()
        sleep(5)

        self.logger.info("Creating profile")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_name_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_name_css).send_keys(
            variables.forwarding_profile_name)
        sleep(2)
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_pkt_filter_xpath).click()
        sleep(2)
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_tunnel_xpath).click()
        sleep(2)
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_tunnel_v2_xpath).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_vpn_same_as_trusted_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MS_fwd_profile_other_same_as_trusted_css).click()
        sleep(2)

        self.logger.info("Save profile")
        self.chrome_driver.find_element("id", self.MA_fwd_profile_save_id).click()
        self.logger.info("Forwarding Profile Saved")
        sleep(10)

    def change_to_tunnel1_forwarding_profile(self):
        sleep(4)
        self.logger.info("******** Changing Forwarding Profile to Tunnel V1")
        self.logger.info("Navigating to Forwarding profiles")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_administrator_css).click()
        sleep(5)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_css).click()
        sleep(5)
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_edit_xpath).click()
        sleep(5)

        self.logger.info("Editing profile")
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_tunnel_v1_xpath).click()
        sleep(2)

        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_vpn_same_as_trusted_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MS_fwd_profile_other_same_as_trusted_css).click()
        sleep(2)

        self.logger.info("Save profile")
        self.chrome_driver.find_element("id", self.MA_fwd_profile_save_id).click()
        self.logger.info("Forwarding Profile Saved")
        sleep(10)

    def change_to_tls_forwarding_profile(self):
        sleep(4)
        self.logger.info("******** Changing Forwarding Profile to Tunnel V1")
        self.logger.info("Navigating to Forwarding profiles")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_administrator_css).click()
        sleep(5)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_css).click()
        sleep(5)
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_edit_xpath).click()
        sleep(5)

        self.logger.info("Editing profile")
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_tunnel_v2_tunnel_type_xpath).click()
        sleep(2)
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_tunnel_v2_tls_xpath).click()
        sleep(2)

        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_vpn_same_as_trusted_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MS_fwd_profile_other_same_as_trusted_css).click()
        sleep(2)

        self.logger.info("Save profile")
        self.chrome_driver.find_element("id", self.MA_fwd_profile_save_id).click()
        self.logger.info("Forwarding Profile Saved")
        sleep(10)

    def change_to_enforce_proxy_forwarding_profile(self):
        sleep(4)
        self.logger.info("******** Changing Forwarding Profile to Enforce Proxy")
        self.logger.info("Navigating to Forwarding profiles")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_administrator_css).click()
        sleep(5)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_css).click()
        sleep(5)
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_edit_xpath).click()
        sleep(5)

        self.logger.info("Editing profile")
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_enforce_proxy_xpath).click()
        sleep(2)

        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_vpn_same_as_trusted_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MS_fwd_profile_other_same_as_trusted_css).click()
        sleep(2)

        self.logger.info("Save profile")
        self.chrome_driver.find_element("id", self.MA_fwd_profile_save_id).click()
        self.logger.info("Forwarding Profile Saved")
        sleep(10)

    def change_to_none_forwarding_profile(self):
        sleep(4)
        self.logger.info("******** Changing Forwarding Profile to None")
        self.logger.info("Navigating to Forwarding profiles")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_administrator_css).click()
        sleep(5)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_css).click()
        sleep(5)
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_edit_xpath).click()
        sleep(5)

        self.logger.info("Editing profile")
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_none_xpath).click()
        sleep(2)

        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_vpn_same_as_trusted_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MS_fwd_profile_other_same_as_trusted_css).click()
        sleep(2)

        self.logger.info("Save profile")
        self.chrome_driver.find_element("id", self.MA_fwd_profile_save_id).click()
        self.logger.info("Forwarding Profile Saved")
        sleep(10)

    def change_to_twlp_forwarding_profile(self):
        sleep(4)
        self.logger.info("******** Changing Forwarding Profile to TWLP")
        self.logger.info("Navigating to Forwarding profiles")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_administrator_css).click()
        sleep(5)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_css).click()
        sleep(5)
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_edit_xpath).click()
        sleep(5)

        self.logger.info("Editing profile")
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_TWLP_xpath).click()
        sleep(2)

        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_vpn_same_as_trusted_css).click()
        sleep(2)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MS_fwd_profile_other_same_as_trusted_css).click()
        sleep(2)

        self.logger.info("Save profile")
        self.chrome_driver.find_element("id", self.MA_fwd_profile_save_id).click()
        self.logger.info("Forwarding Profile Saved")
        sleep(10)

    def change_to_latency_testing(self):
        sleep(4)
        self.logger.info("******** Changing Forwarding Profile for LAtency testing")
        self.logger.info("Navigating to Forwarding profiles")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_administrator_css).click()
        sleep(5)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_css).click()
        sleep(5)
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_edit_xpath).click()
        sleep(5)

        self.logger.info("Editing profile")

        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_vpn_same_as_trusted_css).click()
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_vpn_same_as_trusted_css).click()

        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_dynamic_zen_xpath).click()
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_probe_interval_dropdown_xpath).click()
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_probe_interval_30_xpath).click()

        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_sample_size_dropdown_xpath).click()
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_sample_size_3_xpath).click()

        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_threshold_xpath).click()
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_threshold_xpath).send_keys(Keys.CONTROL + "A")
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_threshold_xpath).send_keys("45")

        self.logger.info("Save profile")
        self.chrome_driver.find_element("id", self.MA_fwd_profile_save_id).click()
        self.logger.info("Forwarding Profile Saved")
        sleep(10)

    def change_to_latency_testing_2(self):
        sleep(4)
        self.logger.info("******** Changing Forwarding Profile for Latency testing")
        self.logger.info("Navigating to Forwarding profiles")
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_administrator_css).click()
        sleep(5)
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_css).click()
        sleep(5)
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_edit_xpath).click()
        sleep(5)

        self.logger.info("Editing profile")

        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_vpn_same_as_trusted_css).click()
        self.chrome_driver.find_element(By.CSS_SELECTOR, self.MA_fwd_profile_vpn_same_as_trusted_css).click()

        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_dynamic_zen_xpath).click()
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_probe_interval_dropdown_xpath).click()
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_probe_interval_60_xpath).click()

        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_sample_size_dropdown_xpath).click()
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_sample_size_2_xpath).click()

        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_threshold_xpath).click()
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_threshold_xpath).send_keys(Keys.CONTROL + "A")
        self.chrome_driver.find_element("xpath", self.MA_fwd_profile_threshold_xpath).send_keys("40")

        self.logger.info("Save profile")
        self.chrome_driver.find_element("id", self.MA_fwd_profile_save_id).click()
        self.logger.info("Forwarding Profile Saved")
        sleep(10)
