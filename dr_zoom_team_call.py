"""
This script will validate Zoom call is successfully initiated when zcc is in Dr mode
and have pulled latest DB
"""
# from lib.common import common_zcc
# from lib.common import common_desktop
# from lib.common import helper
import winreg
import configparser
import logging
import time,os,datetime
from RPA.Windows import Windows


# declaring object of Windows RPA apackage
library= Windows()
#setting up logging

LOG_TIMESTAMP_FORMAT = "%Y-%m-%d %H-%M-%S"

TIME = datetime.datetime.now().strftime(LOG_TIMESTAMP_FORMAT)

# below logger will create log file db_certification.log under current directory
# file path for logging
current_directory=os.getcwd()

log_path_certification=os.path.join(current_directory,"Logs","Dr-zoom.log")
logger=logging.getLogger("Dr")
logger.setLevel(logging.DEBUG)
format=logging.Formatter("'%(asctime)s %(message)s")

fh=logging.FileHandler(log_path_certification,mode="w")
fh.setFormatter(format)
logger.addHandler(fh)
logger.debug("======Zoom Dr log ========")



config = configparser.ConfigParser()
configuration_file_path=os.path.join(current_directory,"configurations.ini")
config.read(configuration_file_path)

reg_path = r"SOFTWARE\WOW6432Node\Zscaler Inc.\Zscaler"
reg_name="dr.zia.path-zoomtest.com"
print(f"registry path {reg_path}")

class Zoom_Team_Dr:

    """
    This class will initiate a Zoom call and Team call in dr state and validate the behaviour
    """
    # def __init__(self):
    #     """
    #     This constructor will initialize values required for zoom call
    #     """
    #     pass
    zoom_window= Windows()
    def getter_dr_registry(self,name):
        """
        This will return the state of dr registry
        :param registry_path:
        :return: True if on else False if off
        """

        try:
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0,
                                          winreg.KEY_READ)
            value, regtype = winreg.QueryValueEx(registry_key, name)
            winreg.CloseKey(registry_key)
            return value
        except WindowsError:
            return None




    def setter_dr_registry(self,name,state="on"):
        """
        This will on or off the registry to trigger dr on or off
        registry path is Computer\HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Zscaler Inc.\Zscaler
        and value is v=1;b=on for dr or and b=off for dr off
        domain name
        :param stete: dr.zia.path-zoomtest.com
        :return:
        """
        try:
            winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
           # registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0,
                                        #  winreg.KEY_WRITE)
            # in registry in regedit give permission or else will throw error
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0,
                                         winreg.KEY_SET_VALUE)
            # turn it on or pff based on state
            if state == "on":
                # set the registry value to turn on
                value= r"v=1;b=on"
                winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
                winreg.CloseKey(registry_key)
                logger.debug(f"Setting up Dr registry {name} to On is successful")
            elif state == "off":
                # set the registry value to turn off
                value = r"v=1;b=off"
                winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
                winreg.CloseKey(registry_key)
                logger.debug(f"Setting up Dr registry {name} to Off is successful")
            else:
                # wrong state return False
                return False
            logger.debug("Registry setting successful")
            return True
        except WindowsError as e:
             logger.debug(f"Exception occured as {e}")
             return False

    def zoom_call_start(self):
        """
        This function will use RPA framework and initiate a Zoom call. If the call is successful
        will return True else False
        :return:
        """
        # Getting zoom meeting details
        meeting_id = config["zoom-call-details"]["zoom-meeting-code"]
        passcode = config["zoom-call-details"]["password"]
        try:
            logger.debug("opening zoom app")
            library.windows_search("Zoom",3)
            zoom_window="name:\"Zoom Cloud Meetings\""
            library.control_window(zoom_window)
            library.click("name:\"Join a Meeting\"")
            # it will go to new window

            library.control_window("name:\"Join Meeting\"")
            logger.debug("Sending meeting ID ")
            time.sleep(2)
            library.send_keys("name:\"Meeting ID or Personal Link Name\"",meeting_id)
            library.send_keys("name:\"Enter your name\"","subham-dr-zooom-test")
            library.click("name:Join")
            # changing the window
            library.control_window("name:\"Enter meeting passcode\"")
            #entering passcode
            time.sleep(2)
            library.send_keys("name:\"Meeting Passcode\"",passcode,1)
            # click join meeting button
            library.click("name:\"Join Meeting\"")
            # switch to waiting for host window

            library.control_window("name:\"Waiting for Host\"")


        except Exception as e:
            logger.debug(f"Error occured as {e}")
            return False
        finally:
            # closing the app

            library.close_current_window()

if __name__ == "__main__":
        obj= Zoom_Team_Dr()
        obj.zoom_call_start()

        # res=obj.setter_dr_registry(name=reg_name,state="off")
        # logger.debug(res)
        # res=obj.getter_dr_registry(reg_name)
        # print(f"registry value of {reg_name} if {res}")
        # # setting dr registry
        #
        # # do a update policy on zcc to Dr take effect
        # # some functions for update policy

        # then check zcc went into safe mode
        # check logs 200 ok
        # now initiate a zoom call and return True
