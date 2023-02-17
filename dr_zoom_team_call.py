"""
This script will validate Zoom call is successfully initiated when zcc is in Dr mode
and have pulled latest DB
Requirements

1. DR DB list from ZIA team (SMSM) - SMSM will stop upload DRDB

2. List in centos VM
Script will validate

Duplicate enteries
Format for each ip, url
Private IP should be subnet range
Cross check Zoom/Team IPs with their official list
3. Hit Win machine and trigger script in win to test Zoom call (Headless ZCC is running)
Win Script:

Change registry and enable DR and use local DR DB
Test Zoom with and without DR and results should match
It will call Zoom and test
4. If call status, send result to centOS script

5. Centos script will upload new DR DB file to S3 bucket

Monitor in CentOS to check DR DB integrity

It will be running every 15 min and download prod DR DB and check Hash of the file and cross check with local Hash
Monitor to check Zoom call

Have monitor if fails, send an email - Separate script with Prod DR DB


"""
from lib.common import common_zcc
# from lib.common import common_desktop
from lib.common import helper
import winreg
import configparser
import logging
import time, os
import subprocess
from RPA.Windows import Windows
import pyautogui
from datetime import datetime

# declaring object of Windows RPA apackage
windows = Windows()
# setting up logging

LOG_TIMESTAMP_FORMAT = "%Y-%m-%d %H-%M-%S"

TIME = datetime.now().strftime(LOG_TIMESTAMP_FORMAT)

# below logger will create log file db_certification.log under current directory
# file path for logging
current_directory = os.getcwd()

log_path_certification = os.path.join(current_directory, "Logs", "Dr-zoom.log")
zoom_logger = logging.getLogger("Dr")
zoom_logger.setLevel(logging.DEBUG)
format = logging.Formatter("'%(asctime)s %(message)s")

fh = logging.FileHandler(log_path_certification, mode="w")
fh.setFormatter(format)
zoom_logger.addHandler(fh)
zoom_logger.debug("======Zoom Dr log ========")

config = configparser.ConfigParser()
configuration_file_path = os.path.join(current_directory, "configurations.ini")
config.read(configuration_file_path)

reg_path = r"SOFTWARE\WOW6432Node\Zscaler Inc.\Zscaler"
reg_name = "dr.zia.path-zoomtest.com"
zoom_logger.debug(f"registry path {reg_path}")


class Zoom_Team_Dr:
    """
    This class will initiate a Zoom call and Team call in dr state and validate the behaviour
    """

    def __init__(self):
         """
         This constructor will initialize values required for zoom call
         """
         self.zoom_test_result={}
    def getter_dr_registry(self, name):
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

    def setter_dr_registry(self, name=reg_name, state="on"):
        """
        This will on or off the registry to trigger dr on or off
        registry path is Computer\HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Zscaler Inc.\Zscaler
        and value is v=1;b=on for dr or and b=off for dr off
        domain name
        :param state: dr.zia.path-zoomtest.com
        :return: True if setting successful or else False
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
                value = r"v=1;b=on"
                winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
                winreg.CloseKey(registry_key)
                zoom_logger.debug(f"Setting up Dr registry {name} to On is successful")
            elif state == "off":
                # set the registry value to turn off
                value = r"v=1;b=off"
                winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
                winreg.CloseKey(registry_key)
                zoom_logger.debug(f"Setting up Dr registry {name} to Off is successful")
            else:
                # wrong state return False
                return False
            zoom_logger.debug("Registry setting successful")
            return True
        except WindowsError as e:
            zoom_logger.debug(f"Exception occured as {e}")
            return False

    def zoom_call_start(self):
        """
        This function will use RPA framework and initiate a Zoom call. If the call is successful
        will return True else False
        :return: True or False
        """
        # Getting Zoom meeting details
        meeting_id = config["zoom-call-details"]["zoom-meeting-code"]
        passcode = config["zoom-call-details"]["password"]
        meeting_text_element = "name:zoom-test-dr"
        try:
            zoom_logger.debug("opening zoom app")
            windows.windows_search("Zoom", 3)
            zoom_window = "name:\"Zoom Cloud Meetings\""
            windows.control_window(zoom_window, 3)
            windows.click("name:\"Join a Meeting\"", 2)
            # it will go to new window

            windows.control_window("name:\"Join Meeting\"")
            zoom_logger.debug("Sending meeting ID ")
            time.sleep(2)
            windows.send_keys("name:\"Meeting ID or Personal Link Name\"", meeting_id)
            windows.send_keys("name:\"Enter your name\"", "subham-dr-zooom-test")
            windows.click("name:Join")
            # changing the window
            windows.control_window("name:\"Enter meeting passcode\"")
            # entering passcode
            time.sleep(2)
            zoom_logger.debug(f"sending passcode to Zoom Meeting")
            windows.send_keys("name:\"Meeting Passcode\"", passcode)
            # click join meeting button
            windows.click("name:\"Join Meeting\"")
            # switch to waiting for host window

            windows.control_window("name:\"Waiting for Host\"")
            # get elements from zoom window
            meeting_text = windows.get_elements(meeting_text_element)
            zoom_logger.debug(f"zoom call elements {meeting_text}")
            # printing the team text
            for ele in meeting_text:
                zoom_logger.debug(f"printing zoom call elements{ele}")
            if len(meeting_text) == 1:
                # meeting text found so return True
                zoom_logger.debug(f"Zoom Test  text found returning {True}")
                zoom_logger.debug("Zoom test passed ")
                return True
            else:
                zoom_logger.debug(f"Error occured as {e}")
                # Taking screenshot
                zoom_logger.debug("Zoom call failed taking screenshot")
                zoom_screenshot = pyautogui.screenshot()
                file_path = os.path.join(current_directory, "Zoom_screenshots", "zoom-fail.png")
                zoom_logger.debug(f"file path of screen shot {file_path}")
                zoom_screenshot.save(file_path)
                return False

            time.sleep(5)

        except Exception as e:
            zoom_logger.debug(f"Error occured as {e}")
            # Taking screenshot
            zoom_logger.debug("Zoom call failed taking screenshot")
            zoom_screenshot = pyautogui.screenshot()
            file_path = os.path.join(current_directory, "Zoom_screenshots", "zoom-fail.png")
            zoom_logger.debug(f"file path of screen shot {file_path}")
            zoom_screenshot.save(file_path)
            return False
        finally:
            # closing the apps

            windows.close_current_window()
            subprocess.call(["taskkill", "/F", "/IM", "Zoom.exe"])
            subprocess.call(["taskkill", "/F", "/IM", "chrome.exe"])


if __name__ == "__main__":
    try:
        # # declaring objects
        obj = Zoom_Team_Dr()
        zcc_obj = common_zcc.ZCC()
        # # checking Zcc is Connected and not in DR state
        # # set the registry off and
        # # set the registry off and update policy and then check zcc status
        # ret = obj.setter_dr_registry(state="off")
        # zoom_logger.debug(f"returning of registry {ret}")
        # assert ret == True, "Registry setting failed"
        # # update zcc to get effect of dr registry
        # zcc_obj.perform_zcc_update_policy()
        # # check tunnel status is on
        # tunnel_status= zcc_obj.verify_zcc_tunnel_on()
        # # checking zcc is connected service status on
        # if not tunnel_status:
        #     # tunnel is not on before DR
        #     zoom_logger.debug("Tunnel is not up before DR , script will abort")
        # assert tunnel_status == True, "Tunnel is not on ,exiting"
        # # tunnel is up initiate Zoom call
        # res_before_dr = obj.zoom_call_start()
        # obj.zoom_test_result["Zoom_call_before_Dr"] = res_before_dr
        # if not res_before_dr:
        #     # zoom call was not successful
        #     zoom_logger.debug("Zoom call Failed before DR so there is some issue aborting the script")
        # # lets trigger Dr by setting the dr register on
        # zoom_logger.debug("Setting the registry off to trigger DR")
        # registry_res=obj.setter_dr_registry(state="on")
        # zoom_logger.debug(f"Return of DR registry on {registry_res}")
        # assert registry_res, "Setting Dr registry failed"
        # # update policy
        # zcc_obj.zcc_update_policy
        # time.sleep(7) # waiting 7 seconds
        # # check in UI ZCC is in DR state
        # # open zcc
        dr_status=checking_dr_status=zcc_obj.verify_zcc_dr_status()
        zoom_logger.debug(f"Dr status {dr_status} ")
        # check dr status




        # if res True Zoom call succeded

    except Exception as e:
        zoom_logger.debug(f"Exception {e} occured")
