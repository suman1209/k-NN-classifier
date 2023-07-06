# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details
from __future__ import annotations
from classifier_classes.datamodel import CsvParser
from classifier_classes.constants import DistanceAlgos as Da
from classifier_classes.classifier import Classifier
from classifier_classes.logger import ClassifierLogger
from typing import List, Tuple
from concurrent.futures import ProcessPoolExecutor
from concurrent import futures

logger = ClassifierLogger.logger


class HyperParameters:
    potential_k_values = list(range(1, 40))
    potential_dist_algos = [Da.ed4.value, Da.mh4.value]

    def __init__(self, data_model: CsvParser):
        self.training_data = data_model.train_data
        self.hp_tuning_data = data_model.hp_tuning_data
        self.validation_data = data_model.validation_data

    def get_optimum_hp(self, fast_mode) -> tuple[int, str]:
        tuning_results = []
        num_hp_samples = len(self.hp_tuning_data)
        assert num_hp_samples > 0, "There is no data available for hyperparameter tuning"
        logger.debug(f"num of sample used for hyper parameter tuning: {num_hp_samples}")
        grid_options = []
        for k in HyperParameters.potential_k_values:
            for dis_algo in HyperParameters.potential_dist_algos:
                grid_options.append((k, dis_algo))
        if fast_mode:
            hps: List[futures.Future[tuple[int, str, float]]] = []
            with ProcessPoolExecutor() as workers:
                for grid_option in grid_options:
                    classifier = Classifier(k=grid_option[0], training_data=self.training_data,
                                            dist_algo=grid_option[1])
                    hps.append(workers.submit(classifier.test, self.hp_tuning_data))
                for f in futures.as_completed(hps):
                    if isinstance(f.result(), Exception):
                        print(f"Exception in getting restults from future objects")
                        raise
                    tuning_results.append(f.result())
        else:
            for grid_option in grid_options:
                classifier = Classifier(k=grid_option[0], training_data=self.training_data,
                                        dist_algo=grid_option[1])
                tuning_results.append(classifier.test(self.hp_tuning_data))
        best_k, best_dist_algo = self.select_best_parameters(tuning_results)

        return best_k, best_dist_algo

    @staticmethod
    def select_best_parameters(tuning_results: List[Tuple[int, str, float]]):
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
