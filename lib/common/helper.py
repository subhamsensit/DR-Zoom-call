import os
import logger


class HELPER:
    log_path = "C:\\ProgramData\\Zscaler"
    logger = logger.LogGen.loggen()

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








