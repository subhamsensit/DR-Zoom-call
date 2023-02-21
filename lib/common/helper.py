import os,sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
current_directory = os.getcwd()
# adding library folder
# current library directory
sys.path.append(os.path.join(current_directory,"lib","common"))
from lib.common import zscaler_logger



class HELPER:
    log_path = "C:\\ProgramData\\Zscaler"
    logger = zscaler_logger.LogGen.loggen()

    def read_logs_latency_based_zen(self):
        filenames = os.listdir(self.log_path)
        tray_logs = list(filter(lambda x: "ZSATunnel_" in x, filenames))
        tray_logs.sort(reverse=True)
        last_logs = self.log_path + "\\" + tray_logs[0]

        self.logger.info("******** Checking logs ********")
        check = False
        for line in reversed(open(last_logs).readlines()):
            if "latencyBasedZenEnablement" in line:
                self.logger.info("Found logs for policy")
                if "\"latencyBasedZenEnablement\":true" in line and "\"zenProbeInterval\":30,\"zenProbeSampleSize\":3,\"zenThresholdLimit\":45" in line:
                    self.logger.info("Latency Based ZEN is enabled and all params are set correctly")
                    check = True
                else:
                    self.logger.info("Latency Based ZEN is enabled and params are not set correctly")
                    check = False
                break

        if check:
            assert True
        else:
            assert False

    def read_logs_sme_swapping(self):
        filenames = os.listdir(self.log_path)
        tray_logs = list(filter(lambda x: "ZSATunnel_" in x, filenames))
        tray_logs.sort(reverse=True)
        last_logs = self.log_path + "\\" + tray_logs[0]

        self.logger.info("******** Checking logs ********")
        check = False
        for line in reversed(open(last_logs).readlines()):
            if "ZPHM::LBZ: HTTP latency better for the other ZEN, swapping" in line:
                self.logger.info("Found logs for policy")
                check = True
                break

        if check:
            assert True
        else:
            assert False

    def read_logs_for_secondary_sme(self):
        filenames = os.listdir(self.log_path)
        tray_logs = list(filter(lambda x: "ZSATunnel_" in x, filenames))
        tray_logs.sort(reverse=True)
        last_logs = self.log_path + "\\" + tray_logs[0]

        self.logger.info("******** Checking logs ********")
        check = False
        for line in reversed(open(last_logs).readlines()):
            if "return \"PROXY" in line and "; DIRECT\";" in line:
                req_line = line.split(' ')
                ip = [req_line[-2].split(':')[0], req_line[-4].split(':')[0]]
                self.logger.info("SM IPs from logs: " + str(ip))
                return ip

    def check_last_tunnel_logs_for_string(self, to_check):
        """
        :param to_check: string which we have to find in logs
        :return: T/F
        """

        filenames = os.listdir(self.log_path)
        tray_logs = list(filter(lambda x: "ZSATunnel_" in x, filenames))
        tray_logs.sort(reverse=True)
        last_logs = self.log_path + "\\" + tray_logs[0]

        self.logger.info("******** Checking logs ********")
        check = False
        for line in reversed(open(last_logs).readlines()):
            if to_check in line:
                self.logger.info(f"Found given string {to_check} in tunnel logs")
                check = True
                break

        return check
