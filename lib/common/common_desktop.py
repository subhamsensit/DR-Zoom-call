import os
import time
from RPA.Windows import Windows

import variables
import logger


# file scope local variables to serve all test methods

class WIN_SCREEN:
    windows = Windows()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    zsa_tray = "C:\\Program Files (x86)\\Zscaler\\ZSATray\\ZSATray.exe"
    logger = logger.LogGen.loggen()

    proxy_script_toggle = "id:AutoScript_Toggle"
    proxy_script_enabled = "id:AutoScript_Toggle isEnabled:True"
    settings_window = "name:Settings"
    pac_url = "id:SystemSettings_Proxy_AutomaticConfigScript_ScriptValue"

    clumsy_window = "name:clumsy 0.2"
    clumsy_textbox = "id:101"
    clumsy_lag = "id:108"
    clumsy_lag_amount = "id:112"
    clumsy_start_stop = "id:103"

    def open_settings(self):
        self.logger.info("--- Opening Settings ---")
        self.logger.info("Trying to open Settings from windows search")
        self.windows.windows_search("Change Proxy Settings", 2)
        time.sleep(10)

        try:
            self.windows.control_window(self.settings_window)
        except:
            self.logger.info("Settings can't be opened")
        finally:
            self.logger.info("--- Settings opened successfully ---")

    def open_clumsy(self):
        self.logger.info("--- Opening Clumsy ---")
        self.windows.windows_search("Clumsy", 2)
        time.sleep(10)
        self.windows.send_keys(None, "{LEFT}")
        self.windows.send_keys(None, "{ENTER}")

        try:
            self.windows.control_windows(self.clumsy_window)
        except:
            self.logger.info("Clumsy can't be opened")
        finally:
            self.logger.info("--- Clumsy opened successfully ---")

    def verify_proxy_settings(self):
        self.logger.info("******** Verifying Proxy settings ********")
        self.open_settings()

        self.logger.info("Verifying for Use Script toggle;")
        tunnel = self.windows.get_elements(self.proxy_script_toggle)

        self.logger.info("Elements Found: " + str(len(tunnel)))
        if len(tunnel) == 1:
            self.logger.info("Copying PAC URL")
            pac = self.windows.get_value(self.pac_url)
            self.logger.info("PAC URL = " + pac)
            if pac.split('.')[-1] == "pac" and pac.split('/')[2] == "127.0.0.1:9000":
                self.logger.info("URL is valid")
                self.windows.close_window(self.settings_window)
                assert True
            else:
                self.logger.info("URL is invalid")
                self.windows.close_window(self.settings_window)
                assert False

    def block_sme_using_clumsy(self, ip):
        self.logger.info("******** Blocking SME ********")
        self.open_clumsy()

        self.logger.info("Adding IP")
        self.windows.send_keys(self.clumsy_textbox, "{CTRL}a")
        self.windows.send_keys(self.clumsy_textbox, "outbound and ip.DstAddr = " + ip)
        self.windows.click(self.clumsy_lag)
        self.windows.send_keys(self.clumsy_lag_amount, "{CTRL}a")
        self.windows.send_keys(self.clumsy_lag_amount, "1000")
        self.windows.click(self.clumsy_start_stop)
        self.logger.info("******** Completed ********")


    def stop_clumsy(self):
        self.windows.click(self.clumsy_start_stop)



    def zoom_call_start(self):
        """
        This function will start a Zoom call
        :return: True is the call successful or False if call did not go through
        """
    def zoom_call_stop(self):
        """
        This will stop the ongoing Zoom call
        :return: True if it successfully stopped the call else False
        """





