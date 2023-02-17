import logging
import os

current_dir=os.getcwd()
log_file_path= os.path.join(current_dir,"Logs","zcc.log")
class LogGen:
    @staticmethod
    def loggen():
        logging.basicConfig(filename= log_file_path,
                            format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', force=True)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        return logger
