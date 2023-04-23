# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details
from classifier_classes.datamodel import CsvParser
from classifier_classes.constants import DistanceAlgos as Da
from tqdm import tqdm
from classifier_classes.classifier import Classifier
from classifier_classes.logger import ClassifierLogger

logger = ClassifierLogger().get_logger()


class HyperParameters:
    potential_k_values = [1, 3, 5, 7, 9, 11, 13]
    potential_dist_algos = [Da.ed4.value, Da.mh4.value]

    def __init__(self, data_model: CsvParser):
        self.training_data = data_model.train_data
        self.hp_tuning_data = data_model.hp_tuning_data
        self.validation_data = data_model.validation_data

    def get_optmum_hp(self) -> tuple[int, str]:
        tuning_results = []
        for k in tqdm(HyperParameters.potential_k_values):
            for dis_algo in HyperParameters.potential_dist_algos:
                classifier = Classifier(k=k, training_data=self.training_data, dist_algo=dis_algo)
                test_score = 0
                for hp_tuning_samples in self.hp_tuning_data:
                    assert hp_tuning_samples.hp_tuning, "This is not a sample that can be used for hp tuning"
                    classifier.classify(hp_tuning_samples)
                    if hp_tuning_samples.is_prediction_true():
                        test_score += 1
                tuning_results.append((k, dis_algo, test_score))
        sorted_tuning_results = tuning_results.copy()
        sorted_tuning_results.sort(key=lambda x: x[2])
        logger.debug(f"Hyperparameter Tuning Results sorted according to test_score: {sorted_tuning_results}")
        best_k, best_dist_algo = sorted_tuning_results[-1][0], sorted_tuning_results[-1][1]
        logger.debug(f"best_k, best_dist_algo:-> {best_k, best_dist_algo}")
        return best_k, best_dist_algo
