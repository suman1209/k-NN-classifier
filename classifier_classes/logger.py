import logging
from classifier_classes.config import Config
import os
# @todo debug how to set the environmental variable
os.environ['CLASSIFIER_HOME_DIR'] = 'D:/k-NN-classifier/'


class ClassifierLogger:
    def __init__(self):
        self.log_formater = '%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s'
        self.logger = self.initialise_log_file()

    def initialise_log_file(self):
        home_dir = os.getenv("CLASSIFIER_HOME_DIR")
        assert isinstance(home_dir, str), f"Invalid env variable for this classifier project {home_dir}" \
                                          f"\nplease set the environment variable as follows" \
                                          f"\nexport CLASSIFIER_HOME_DIR='D:/k-NN-classifier'"
        log_filename = home_dir + Config().log_filename
        # Configure the logging module
        logging.basicConfig(
            filename=log_filename,
            level=logging.DEBUG,
            filemode='w',
            format=self.log_formater,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        return logging.getLogger()

    def get_logger(self):
        logger = self.logger
        # console_handler = logging.StreamHandler()
        # console_handler.setFormatter(logging.Formatter(self.log_formater))
        # console_handler.setLevel(logging.INFO)
        # logger.addHandler(console_handler)
        return logger
