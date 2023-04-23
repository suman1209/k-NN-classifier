# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details
import csv
from sample import KnownSample
from typing import List
from utilities import split_list
from constants import SplitPercentage as Sp
from logger import ClassifierLogger
from constants import ConstantNames as Cn

from config import Config
import datetime
from zoneinfo import ZoneInfo
logger = ClassifierLogger().get_logger()


class DataSet:
    """This class is intended to handle the job of loading the raw dataset from potential sources and
        creating data in the form processable by the classifier
    """
    def __init__(self, raw_data_path):
        self.raw_data_path = raw_data_path

    def split_dataset(self):
        raise Exception("Unexpected Call to the abstract class!")


class CsvParser(DataSet):
    DATASET: List[KnownSample] = []
    """Here the expected dataset is a csv in the following format...
    
       sepal_length,sepal_width,petal_length,petal_width,species
       '5.1','3.5','1.4','0.2','Iris-setosa'
       ...
       ...
       
       """
    def __init__(self, raw_data_path):
        super().__init__(raw_data_path)
        self.uploaded = datetime.datetime.now(tz=ZoneInfo("Asia/Colombo"))
        self.data = self.initialise_data_from_file()
        self.train_data, self.hp_tuning_data, self.validation_data = self.split_dataset()

    def initialise_data_from_file(self):
        assert self.raw_data_path.endswith(".csv"), f"The format of the input file {self.raw_data_path}" \
                                                    f" is not supported yet.."
        with open(self.raw_data_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            bad_sample = []
            for idx, row in enumerate(csv_reader):
                self.validate_input_data(idx, row)
                try:
                    sample = KnownSample.from_dict(row)
                    CsvParser.DATASET.append(sample)
                except Exception as exc:
                    bad_sample.append(idx)
                    logger.debug(f"Invalid Sample {idx}: {row}", str(exc))
        if len(bad_sample) > 0:
            logger.info(f"{len(bad_sample)} bad sample count received, check the log file {Config().log_filename}"
                        f" for the details..")
            if len(bad_sample) >= 0.5 * idx:
                raise Exception("Almost half the input data is invalid!")
        logger.info(f"Dataset uploaded and verified on {self.uploaded}..")
        return row

    @staticmethod
    def validate_input_data(index: int, row: list):
        assert len(row) == 5, f"Expected four features and 1 class label, but received {len(row)} entries for" \
                              f" the entry num {index}"
        assert isinstance(row[Cn.species.value], str), f"the class label is expected to be a str," \
                                        f" but got {row[Cn.species.value]}-{type(row[Cn.species.value])}"  # noqa

    def split_dataset(self):
        """this method takes the list of samples and randomly splits it into training, hp_tuning, and validation
           datasets
        """
        total_dataset_count = len(CsvParser.DATASET)
        assert total_dataset_count > 0, f"The dataset has {total_dataset_count} num of data samples, please check " \
                                        f"the input dataset file.."
        split_components = split_list(CsvParser.DATASET,
                                      Sp.train.value, Sp.hp_tuning.value, Sp.validation.value)
        logger.debug(f"{[(dtype, len(comp)) for dtype, comp in zip(['train', 'hp', 'val'], split_components)]}")
        return split_components

    def __repr__(self):
        return f"CsvParser('{self.raw_data_path}')"


class DatasetFactory:
    def __init__(self, raw_data_path: str):
        self.raw_data_path = raw_data_path

    def create_data_model(self):
        if self.raw_data_path.endswith(".csv"):
            return CsvParser(raw_data_path=self.raw_data_path)
        else:
            raise Exception(f"Format of input data not yet supported {self.raw_data_path}")


if __name__ == "__main__":
    dataset_path = "../Dataset/iris_data.csv"
    data_model = DatasetFactory(dataset_path).create_data_model()
