import logging
from classifier_classes.config import Config
import os


class ClassifierLogger:
    _instance = None
    formatter = '%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s'
    log_filename = Config().log_filename
    logger = logging.getLogger()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            return cls._instance
        else:
            return cls._instance

    @classmethod
    def initialise_log_file(cls):
        home_dir = os.getenv("CLASSIFIER_HOME_DIR")
        assert isinstance(home_dir, str), f"Invalid env variable for this classifier project {home_dir}" \
                                          f"\nplease set the environment variable as follows" \
                                          f"\nexport CLASSIFIER_HOME_DIR='<../../k-NN-classifier'>"
        log_filename = Config().log_filename
        # Configure the logging module
        logging.basicConfig(
            filename=log_filename,
            level=logging.DEBUG,
            filemode='w',
            format=ClassifierLogger.formatter,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        return logging.getLogger()

    def get_logger(self):
        logger = self.initialise_log_file()
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(ClassifierLogger.formatter))
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        return logger
