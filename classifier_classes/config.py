# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details

import json
import os.path
from pathlib import Path


class Config:
    CONFIG_JSON = f"classifier_config.json"
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.json_config = self.initilise_json_config()
        self._home_env_var = self._get_home_env_var()
        self.initilise_reports_dir()
    @property
    def report_dir(self):
        return self.json_config["report_directory"]

    @property
    def log_filename(self):
        return f"{self.home_dir}/{self.report_dir}/{self.json_config['log_file_name']}"

    @property
    def home_dir(self):
        return self._home_env_var

    @staticmethod
    def initilise_json_config():
        with open(Config.CONFIG_JSON) as f:
            json_config = json.load(f)
        return json_config

    def initilise_reports_dir(self):
        reports_dir = f"{self.home_dir}/{self.report_dir}"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)

    @staticmethod
    def _get_home_env_var():
        home_dir = os.getenv("CLASSIFIER_HOME_DIR")
        assert isinstance(home_dir, str), f"Invalid env variable for this classifier project {home_dir}" \
                                          f"\nplease set the environment variable as follows" \
                                          f"\nexport CLASSIFIER_HOME_DIR='<../../k-NN-classifier'> in linux"
        home_dir = home_dir.rstrip("/")
        assert Path(home_dir).exists(), f"Invalid home_dir provided - {home_dir}"
        return home_dir
