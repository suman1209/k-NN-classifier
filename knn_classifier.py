# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details

import argparse
from classifier_classes.datamodel import DatasetFactory
from classifier_classes.hyperparameters import HyperParameters as Hp
from classifier_classes.classifier import Classifier
from classifier_classes.constants import Approximations
from classifier_classes.logger import ClassifierLogger
# creating a logger instance only once
logger = ClassifierLogger().get_logger()


class KNNClassifier:
    """This class is the driver script for getting a classification for an Unknown Sample"""
    def __init__(self, raw_input_file_path: str):
        self.data_model = DatasetFactory(raw_input_file_path).create_data_model()
        self.k, self.dist_algo = self.get_optimum_hyper_parameters()
        self.classifier = Classifier(k=self.k, training_data=self.data_model.train_data, dist_algo=self.dist_algo)

    def get_optimum_hyper_parameters(self):
        k, dist_algo = Hp(self.data_model).get_optimum_hp()
        return k, dist_algo

    def find_accuracy(self):
        correct_predictions = 0
        # classifying all the samples in the validation set
        for test_samples in self.data_model.validation_data:
            assert test_samples.val, "This sample is not intended for validatation purpose"
            self.classifier.classify(test_samples)
            if test_samples.is_prediction_true():
                correct_predictions += 1

        num_validation_samples = len(self.data_model.validation_data)
        assert num_validation_samples > 0, "There are no validation samples to find the validation accuracy"
        accuracy = correct_predictions / num_validation_samples
        accuracy = round(accuracy, Approximations.round_nearest_to)
        return accuracy

    def __repr__(self):
        return f"KNNClassifier('{self.data_model.raw_data_path}') created..."


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_inp_data_path', type=str, help='Path to the dataset file')
    args = parser.parse_args()

    clf = KNNClassifier(args.raw_inp_data_path)
    # clf object created
    print(clf)
    # clf data model created
    print(f"The dataset based on the raw data from '{clf.data_model.raw_data_path}' has been successfully created...")
    print(clf.data_model)
    # best hyperparameters
    print(f"Best Hyperparameters chosen: k: {clf.k} dist_algo: {clf.dist_algo}")
    # performance on the validation data
    print(f"Accuracy on the validation data: {clf.find_accuracy()}")

