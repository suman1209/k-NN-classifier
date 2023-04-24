# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details
from classifier_classes.datamodel import CsvParser
from classifier_classes.constants import DistanceAlgos as Da
from tqdm import tqdm
from classifier_classes.classifier import Classifier
from classifier_classes.logger import ClassifierLogger
from typing import List, Tuple

logger = ClassifierLogger().get_logger()


class HyperParameters:
    potential_k_values = [1, 3, 5, 7, 9, 11, 13]
    potential_dist_algos = [Da.ed4.value, Da.mh4.value]

    def __init__(self, data_model: CsvParser):
        self.training_data = data_model.train_data
        self.hp_tuning_data = data_model.hp_tuning_data
        self.validation_data = data_model.validation_data

    def get_optimum_hp(self) -> tuple[int, str]:
        tuning_results = []
        num_hp_samples = len(self.hp_tuning_data)
        assert num_hp_samples > 0, "There is no data available for hyperparameter tuning"
        logger.debug(f"num of sample used for hyper parameter tuning: {num_hp_samples}")
        for k in tqdm(HyperParameters.potential_k_values):
            for dis_algo in HyperParameters.potential_dist_algos:
                classifier = Classifier(k=k, training_data=self.training_data, dist_algo=dis_algo)
                test_score = 0
                for hp_tuning_samples in self.hp_tuning_data:
                    assert hp_tuning_samples.hp_tuning, "This is not a sample that can be used for hp tuning"
                    classifier.classify(hp_tuning_samples)
                    if hp_tuning_samples.is_prediction_true():
                        test_score += 1
                test_score = test_score / num_hp_samples
                tuning_results.append((k, dis_algo, test_score))

        best_k, best_dist_algo = self.select_best_parameters(tuning_results)

        return best_k, best_dist_algo

    @staticmethod
    def select_best_parameters(tuning_results: List[Tuple[int, str, int]]):
        sorted_tuning_results = tuning_results.copy()
        sorted_tuning_results.sort(key=lambda x: x[2])
        logger.debug(f"Hyperparameter Tuning Results sorted according to test_score: {sorted_tuning_results}")

        # the parameters will be selected such that k is minimum for faster computations
        """
        e.g. Consider a case like this - (k, dist_algo, num_correct_scores)
        [(5, 'Manhattan', 7), (5, 'Euclidian', 29), (7, 'Euclidian', 29), (13, 'Euclidian', 29)]
        the best parameters should chosen should be (5, 'Euclidian', 29), choosing the parameter corresponding to
        the highest score is not the optimal solution
        """
        highest_score = max(sorted_tuning_results, key=lambda x: x[2])[2]
        # all hyperparameters having the highest score
        hps_having_highest_score = [hp for hp in sorted_tuning_results if hp[-1] == highest_score]
        sorted_best_hps = hps_having_highest_score.copy()
        sorted_best_hps.sort(key=lambda x: x[0])
        logger.debug(f"{sorted_best_hps = }")
        # choosing the hp with the lowest k-value
        best_k, best_dist = sorted_best_hps[0][0], sorted_best_hps[0][1]
        logger.debug(f"best_k, best_dist_algo:-> {best_k, best_dist}")
        return best_k, best_dist
