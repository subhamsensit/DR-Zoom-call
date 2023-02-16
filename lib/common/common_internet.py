from selenium import webdriver
import variables
import logger


class InternetAccess:
    message_xpath = "/html/body/main/div[2]/div[1]"
    chrome_driver = webdriver.Chrome(executable_path=variables.chrome_path)
    logger = logger.LogGen.loggen()

    def verify_internet_access(self):
        self.logger.info("******** Checking Internet Access ********")
        try:
            self.logger.info("Opening ip.zscaler.com")
            self.chrome_driver.get(variables.internet_access_url)

            self.logger.info("Checking message")
            web_access = self.chrome_driver.find_element("xpath", self.message_xpath).text
            self.logger.info("Message: " + web_access)

            if "You are accessing the Internet via a Zscaler" in web_access:
                self.logger.info("Internet is accessed via Zscaler")
                assert True
            else:
                self.logger.error("Internet is not accessed via Zscaler")
                assert False
        except:
            self.logger.error("Cannot Open Webpage")
            assert False
        finally:
            self.chrome_driver.quit()

    def verify_no_internet_access(self):
        self.logger.info("******** Checking for NO Internet Access ********")
        try:
            self.logger.info("Opening ip.zscaler.com")
            self.chrome_driver.get(variables.internet_access_url)

            self.logger.info("Checking message")
            web_access = self.chrome_driver.find_element("xpath", self.message_xpath).text
            self.logger.info("Message: " + web_access)
            if "You are accessing the Internet via a Zscaler" not in web_access:
                self.logger.info("Internet is not accessed via Zscaler")
                assert True
            else:
                self.logger.error("Internet is accessed via Zscaler")
                assert False
        except:
            self.logger.error("Cannot Open Webpage")
            assert False
        finally:
            self.chrome_driver.quit()
