import os
import time
from RPA.Windows import Windows
#import variables
import zscaler_logger


# file scope local variables to serve all test methods

class ZCC:
    windows = Windows()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    zsa_tray = "C:\\Program Files (x86)\\Zscaler\\ZSATray\\ZSATray.exe"
    app_policy="zoom-team-disaster-recovery-test"
    logger = zscaler_logger.LogGen.loggen()

    taskbar = "name:Taskbar"
    notification_chevron = "name:\"Notification Chevron\""
    zcc_icon_service_disabled = "name:\"Service is disabled.\" type:UIA_ButtonControlTypeId"
    zcc_icon_open_zscaler = "name:\"Open Zscaler\" type:UIA_MenuItemControlTypeId"
    zcc_icon_exit = "name:\"Exit\" type:UIA_MenuItemControlTypeId"

    zcc_window = "id:ZscalerApp"
    zcc_exit_continue = "name:Continue id:ZSABWConfirmAcceptButton"

    zcc_username = "id:ZSAUNFUserNameText"
    zcc_login_button_1 = "name:Login id:ZSAUNFLoginButton"
    zcc_password = "id:ZSAPFPasswordBox"
    zcc_login_button_2 = "name:Login id:ZSAPFLoginButton"
    zcc_logout = "id:ZSAMFLogoutButton"
    zcc_logout_confirm = "id:ZSABWConfirmAcceptButton"

    zcc_ZIA_tab = "id:ZSAMFWebSecurityTab"
    zcc_notification_tab = "id:ZSAMFNotificationsTab"
    zcc_settings_tab = "id:ZSAMFSettingsTab"
    zcc_new_policy_name = "name:\"App Policy:  " + app_policy + "\""
    zcc_tunnel2_dtls = "id:ZSAMFWebSecurityTunnelVersionText name:\"v2.0 - DTLS\""
    zcc_tunnel2_tls = "id:ZSAMFWebSecurityTunnelVersionText name:\"v2.0 - TLS\""
    zcc_tunnel1 = "id:ZSAMFWebSecurityTunnelVersionText name:\"v1.0\""
    zcc_update_policy = "id:ZSAMFSettingsUpdatePolicy"
    zcc_restart_service = "id:ZSAMFSettingsRestartService"
    zcc_tunnel_status_ON = "id:ZSAMFWebSecurityTunnelStatusText name:\"ON\""
    zcc_tunnel_enforce_proxy = "id:ZSAMFWebSecurityTunnelStatusText name:\"Enforce Proxy\""
    zcc_tunnel_none = "id:ZSAMFWebSecurityTunnelStatusText name:\"Disabled\""
    zcc_server = "id:ZSAMFWebSecurityServerIPText"
    zcc_dr_status = "id:ZSAMFWebSecurityTunnelStatusText name:\"Safe Mode\""

    def open_zsa_tray(self):
        self.logger.info("--- Opening Tray ---")
        self.logger.info("Trying to open Tray from windows search")
        self.windows.windows_search("Zscaler", 2)
        time.sleep(10)

        try:
            self.windows.control_window(self.zcc_window)
        except:
            self.logger.info("Tray could not be seen in fore ground")
            self.windows.control_window(self.taskbar)
            self.windows.click(self.notification_chevron)
            self.windows.click(self.zcc_icon_service_disabled)
            self.windows.click(self.zcc_icon_open_zscaler)
            self.windows.control_window(self.zcc_window)
        finally:
            self.logger.info("--- Tray opened successfully ---")

    def perform_zcc_exit(self):
        self.logger.info("******** Closing ZCC ********")
        self.windows.control_window(self.taskbar)
        self.windows.click(self.notification_chevron)
        self.windows.click(self.zcc_icon_service_disabled)
        self.windows.click(self.zcc_icon_exit)
        self.windows.control_window(self.zcc_window)
        self.windows.click(self.zcc_exit_continue)
        self.logger.info("******** ZCC Closed ********")

    def check_menu_items(self):
        self.logger.info("******** Check menu items ********")
        self.windows.click("name:\"ZScaler Menu Button\" id:ZSAUNFMenuButton")
        self.windows.click("name:\"License Agreement Text\" id:ZSASMLicenseButton")
        time.sleep(2)
        self.windows.click("name:OK id:ZSABrowserOKButton")
        self.windows.click("name:\"ZScaler Menu Button\" id:ZSAUNFMenuButton")
        self.windows.click("name:\"About\" id:ZSASMAbouttheContent")
        self.windows.click("name:OK id:ZSASAboutAppOkButton")
        self.windows.click("name:\"ZScaler Menu Button\" id:ZSAUNFMenuButton")
        self.windows.click("name:\"Cloud Name\" id:ZSASMEnterCloudtheContent")
        self.windows.click("name:Cancel id:ZSASMCloudCancelButton")
        self.logger.info("******** Completed ********")

    def perform_zcc_login(self, zpa=False):
        self.logger.info("******** Performing Login ********")
        self.open_zsa_tray()
        self.logger.info("Entering Username")
        self.windows.send_keys(self.zcc_username, "{CTRL}a")
        self.windows.send_keys(self.zcc_username, variables.username)
        self.logger.info("Clicking Login")
        self.windows.click(self.zcc_login_button_1)
        time.sleep(2)

        # Enter Password
        self.logger.info("Entering Password")
        self.windows.send_keys(self.zcc_password, variables.password)
        self.logger.info("Clicking Login")
        self.windows.click(self.zcc_login_button_2)
        time.sleep(2)

        # Enter ZPA Username/Password
        if zpa:
            time.sleep(10)
            self.logger.info("Entering ZPA Username")
            for i in range(0, 6):
                self.windows.send_keys(keys="{TAB}")

            self.windows.send_keys(keys="{CTRL}a")
            self.windows.send_keys(keys=variables.zpa_username)
            self.logger.info("Entering ZPA Password")
            self.windows.send_keys(keys="{TAB}")
            self.windows.send_keys(keys=variables.zpa_password)
            self.windows.send_keys(keys="{ENTER}")
            time.sleep(2)
        else:
            self.logger.info("Skipping ZPA Login")

        time.sleep(5)
        self.logger.info("******** Login attempt completed ********")

    def perform_zcc_logout_without_password(self):
        self.logger.info("******** Performing Logout ********")
        self.open_zsa_tray()
        self.logger.info("Logging_out")
        self.windows.click(self.zcc_logout)
        time.sleep(1)
        self.windows.click(self.zcc_logout_confirm)
        time.sleep(10)
        self.windows.minimize_window(self.zcc_window)
        self.logger.info("******** Logout attempt completed ********")

    def perform_zcc_update_policy(self):
        self.logger.info("******** Performing Update for Policy ********")
        self.open_zsa_tray()
        self.windows.click(self.zcc_settings_tab)
        time.sleep(1)
        self.windows.click(self.zcc_update_policy)
        time.sleep(10)
        self.windows.minimize_window(self.zcc_window)
        self.logger.info("******** Update completed ********")

    def perform_zcc_restart_service(self):
        self.logger.info("******** Performing Restart Service ********")
        self.open_zsa_tray()
        self.windows.click(self.zcc_settings_tab)
        time.sleep(1)
        self.windows.click(self.zcc_restart_service)
        time.sleep(30)
        self.windows.minimize_window(self.zcc_window)
        self.logger.info("******** Restart completed ********")

    def verify_zcc_logged_in(self):
        self.logger.info("******** Verifying Login ********")
        self.open_zsa_tray()
        self.logger.info("Verifying Login")

        try:
            self.logger.info("Checking for Notifications tab")
            elements = self.windows.get_elements(self.zcc_notification_tab)
            self.logger.info("Elements Found: " + str(len(elements)))
            if len(elements) == 1:
                self.logger.info("Login Successful")
                assert True
        except:
            self.logger.error("Login Unsuccessful")
            assert False
        finally:
            self.windows.minimize_window(self.zcc_window)
            self.logger.info("******** Verification Completed ********")

    def verify_zcc_logged_out(self):
        self.logger.info("******** Verifying Logout ********")
        self.open_zsa_tray()
        self.logger.info("Verifying Logout")
        try:
            self.logger.info("Checking for username bar")
            elements = self.windows.get_elements(self.zcc_username)
            self.logger.info("Elements Found: " + str(len(elements)))
            if len(elements) == 1:
                self.logger.info("Logout Successful")
                assert True
        except:
            self.logger.error("Logout Unsuccessful")
            assert False
        finally:
            self.windows.minimize_window(self.zcc_window)
            self.logger.info("******** Verification Completed ********")

    def verify_zcc_new_policy(self):
        self.logger.info("******** Verifying Policy: " + variables.app_policy_name + " ********")
        self.open_zsa_tray()
        self.windows.click(self.zcc_settings_tab)
        try:
            self.logger.info("Verifying policy name")
            policy = self.windows.get_elements(self.zcc_new_policy_name)

            self.logger.info("Elements Found: " + str(len(policy)))
            if len(policy) == 1:
                self.logger.info("Policy Name is shown Correctly")
                assert True
        except:
            self.logger.error("Policy Name is incorrect")
            assert False
        finally:
            self.windows.minimize_window(self.zcc_window)
            self.logger.info("******** Verification Completed ********")

    def verify_zcc_tunnel2_dtls(self):
        self.logger.info("******** Verifying Tunnel V2 DTLS ********")
        self.open_zsa_tray()
        self.windows.click(self.zcc_ZIA_tab)
        try:
            self.logger.info("Verifying for Tunnel 2 DTLS")
            tunnel = self.windows.get_elements(self.zcc_tunnel2_dtls)

            self.logger.info("Elements Found: " + str(len(tunnel)))
            if len(tunnel) == 1:
                self.logger.info("Tunnel type is V2-DTLS")
                assert True
        except:
            self.logger.error("Tunnel type is not V2-DTLS")
            assert False
        finally:
            self.windows.minimize_window(self.zcc_window)
            self.logger.info("******** Verification Completed ********")

    def verify_zcc_tunnel2_tls(self):
        self.logger.info("******** Verifying Tunnel V2 TLS ********")
        self.open_zsa_tray()
        self.windows.click(self.zcc_ZIA_tab)
        try:
            self.logger.info("Verifying for Tunnel 2 TLS")
            tunnel = self.windows.get_elements(self.zcc_tunnel2_tls)

            self.logger.info("Elements Found: " + str(len(tunnel)))
            if len(tunnel) == 1:
                self.logger.info("Tunnel type is V2-TLS")
                assert True
        except:
            self.logger.error("Tunnel type is not V2-TLS")
            assert False
        finally:
            self.windows.minimize_window(self.zcc_window)
            self.logger.info("******** Verification Completed ********")

    def verify_zcc_tunnel1(self):
        self.logger.info("******** Verifying Tunnel V1 ********")
        self.open_zsa_tray()
        self.windows.click(self.zcc_ZIA_tab)
        try:
            self.logger.info("Verifying for Tunnel 1")
            tunnel = self.windows.get_elements(self.zcc_tunnel1)

            self.logger.info("Elements Found: " + str(len(tunnel)))
            if len(tunnel) == 1:
                self.logger.info("Tunnel type is V1")
                assert True
        except:
            self.logger.error("Tunnel type is not V1")
            assert False
        finally:
            self.windows.minimize_window(self.zcc_window)
            self.logger.info("******** Verification Completed ********")

    def verify_zcc_tunnel_enforce_proxy(self):
        self.logger.info("******** Verifying Tunnel is Enforce Proxy ********")
        self.open_zsa_tray()
        self.windows.click(self.zcc_ZIA_tab)
        try:
            self.logger.info("Verifying for Tunnel Status")
            tunnel = self.windows.get_elements(self.zcc_tunnel_enforce_proxy)

            self.logger.info("Elements Found: " + str(len(tunnel)))
            if len(tunnel) == 1:
                self.logger.info("Tunnel status is Enforce Proxy")
                assert True
        except:
            self.logger.error("Tunnel status is not Enforce Proxy")
            assert False
        finally:
            self.windows.minimize_window(self.zcc_window)
            self.logger.info("******** Verification Completed ********")

    def verify_zcc_tunnel_none(self):
        self.logger.info("******** Verifying Tunnel is Disabled ********")
        self.open_zsa_tray()
        self.windows.click(self.zcc_ZIA_tab)
        try:
            self.logger.info("Verifying for Tunnel Status")
            tunnel = self.windows.get_elements(self.zcc_tunnel_none)

            self.logger.info("Elements Found: " + str(len(tunnel)))
            if len(tunnel) == 1:
                self.logger.info("Tunnel status is Disabled")
                assert True
        except:
            self.logger.error("Tunnel status is not Disabled")
            assert False
        finally:
            self.windows.minimize_window(self.zcc_window)
            self.logger.info("******** Verification Completed ********")

    def verify_zcc_tunnel_on(self):

        self.logger.info("******** Verifying Tunnel is connected ********")
        self.open_zsa_tray()
        self.windows.click(self.zcc_ZIA_tab)
        try:
            self.logger.info("Verifying for Tunnel Status")
            tunnel = self.windows.get_elements(self.zcc_tunnel_status_ON)

            self.logger.info("Elements Found: " + str(len(tunnel)))
            if len(tunnel) == 1:
                self.logger.info("Tunnel status is ON")
                assert True
                return True
        except:
            self.logger.error("Tunnel status is not ON")
            assert False
            return False
        finally:
            self.windows.minimize_window(self.zcc_window)
            self.logger.info("******** Verification Completed ********")

    def get_connected_sme_ip(self):
        self.logger.info("******** Verifying Tunnel is connected ********")
        self.open_zsa_tray()
        self.windows.click(self.zcc_ZIA_tab)
        try:
            self.logger.info("Getting SMW IP from ZCC")
            server = self.windows.get_element(self.zcc_server)

            self.logger.info("Elements Found: " + self.windows.get_attribute(server, "Name"))
            return server.split(':')[0]
        except:
            self.logger.error("Could not get SME IP")
            return ""
        finally:
            self.windows.minimize_window(self.zcc_window)
            self.logger.info("******** Completed ********")
    # Dr db code

    def verify_zcc_dr_status(self):
        """
        This function will check zcc service type as safe mode to detect
        DR
        :return:
        """

        self.logger.info("******** Verifying ZCC is in DR state ********")
        self.open_zsa_tray()
        self.windows.click(self.zcc_ZIA_tab)
        try:
            self.logger.info("Verifying for Tunnel Status")
            tunnel = self.windows.get_elements(self.zcc_dr_status)

            self.logger.info("Elements Found: " + str(len(tunnel)))
            if len(tunnel) == 1:
                self.logger.info("DR State on ")
                assert True
                return True
        except Exception as e:
            self.logger.info("Safe mode is not found")
            self.logger.error("DR status is not on")
            assert False
            return False
        finally:
            self.windows.minimize_window(self.zcc_window)
            self.logger.info("******** DR Verification Completed ********")


