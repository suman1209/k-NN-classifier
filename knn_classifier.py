# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details

import argparse
from classifier_classes.datamodel import DatasetFactory
from classifier_classes.hyperparameters import HyperParameters as Hp
from classifier_classes.classifier import Classifier
from classifier_classes.logger import ClassifierLogger
from classifier_classes.config import Config
from typing import List
from classifier_classes.sample import KnownSample
from classifier_classes.utilities import find_accuracy

# creating a logger instance only once
logger = ClassifierLogger().get_logger()


class KNNClassifier:
    """This class is the driver script for getting a classification for an Unknown Sample"""
    def __init__(self, raw_input_file_path: str, fast_mode=False):
        """

        :param raw_input_file_path: input dataset_file csv path
        :param fast_mode: whether to execute the computation faster by utilizing multiple cores or not
        """
        self.fast_mode = fast_mode
        self.data_model = DatasetFactory(raw_input_file_path).create_data_model()
        self.k, self.dist_algo = self.get_optimum_hyper_parameters()
        self.classifier = Classifier(k=self.k, training_data=self.data_model.train_data, dist_algo=self.dist_algo)

    def get_optimum_hyper_parameters(self):
        k, dist_algo = Hp(self.data_model).get_optimum_hp(fast_mode=self.fast_mode)
        return k, dist_algo

    @staticmethod
    def find_accuracy(classifier, dataset: List[KnownSample]):
        accuracy = find_accuracy(classifier, dataset)
        return accuracy

    def __repr__(self):
        return f"KNNClassifier('{self.data_model.raw_data_path}') created..."


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_inp_data_path', type=str, help='Path to the dataset file')
    args = parser.parse_args()
    # initialising the configs
    classifier_config = Config()
    # enable fast mode to execute calculations in parallel where possible
    clf = KNNClassifier(args.raw_inp_data_path, fast_mode=False)
    # clf object created
    print(clf)
    # clf data model created
    print(f"The dataset based on the raw data from '{clf.data_model.raw_data_path}' has been successfully created...")
    print(clf.data_model)
    # best hyperparameters
    print(f"Best Hyperparameters chosen: k: {clf.k} dist_algo: {clf.dist_algo}")
    # performance on the validation data
    print(f"Accuracy on the validation data: {clf.find_accuracy(clf.classifier, clf.data_model.validation_data)}%")
