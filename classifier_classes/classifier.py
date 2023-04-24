# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details
from typing import List
from classifier_classes.sample import Sample, KnownSample
from classifier_classes.constants import DistanceAlgos
from classifier_classes.distance import DistanceFactory
from classifier_classes.logger import ClassifierLogger
from collections import Counter


class ClassificationAlgo:
    """This is the class for the classification algorithm that will be used by the classifier"""
    pass


class Classifier:
    """ this class is responsible for the classification of the sample"""
    def __init__(self, k: int, training_data: List[Sample],  dist_algo: str = DistanceAlgos.ed4.value):
        self.k = k
        self.dist_algo = DistanceFactory().get_distance_algo(dist_algo=dist_algo)
        self.training_data = training_data

    def classify(self, sample_data: Sample, verbosity=0) -> str:
        k_nearest_neighbours = self.find_k_nearest_neighbours(sample_data)
        counts = Counter([samp.species for samp in k_nearest_neighbours])
        counts_list = list(counts.items())
        counts_list.sort(key=lambda x: x[1])
        # logging the final neighbour counts
        if verbosity:
            logger.debug(f"neigbhour counts to the test_sample: {counts_list}")
        predicted_species = counts_list[-1][0]
        sample_data.classification = predicted_species
        if verbosity:
            logger.debug(f"predicted species = {predicted_species}")
        return predicted_species

    def find_k_nearest_neighbours(self, new_sample, verbosity=0) -> List[KnownSample]:
        dist_diff_with_all_training_data = []
        for idx, training_sample in enumerate(self.training_data):
            dist = self.dist_algo.get_distance(training_sample, new_sample)
            dist_diff_with_all_training_data.append((idx, dist))

        assert len(dist_diff_with_all_training_data) == len(self.training_data),\
            f"len(dist_list)={len(dist_diff_with_all_training_data)} != len(training_data)={len(self.training_data)}"

        # finding the k-nearest neighbours
        sorted_dist_list = dist_diff_with_all_training_data.copy()
        sorted_dist_list.sort(key=lambda x: x[1])
        # logging the distances list after sorting
        if verbosity:
            logger.debug(f"The distance difference of the new sample with every sample in the training dataset..\n"
                         f"{sorted_dist_list}")
        k_nearest_neighbour_indices = [item[0] for item in sorted_dist_list[:self.k]]
        if verbosity:
            logger.debug(f"k-nearest neightbour indices in the training dataset({len(self.training_data)} is \n"
                         f"{k_nearest_neighbour_indices}")
        k_nearest_neighbours = [self.training_data[i] for i in k_nearest_neighbour_indices]
        if verbosity:
            logger.debug(f"k-nearest neightbours are \n {k_nearest_neighbours}")

        return k_nearest_neighbours


if __name__ == "__main__":
    # for understanding and minor testing purposes, created a dummy data
    sample1 = KnownSample(5.1, 3.5, 1.4, 0.2, "Iris-setosa")
    sample2 = KnownSample(4.9, 3.0, 1.4, 0.2, "Iris-setosa")
    sample3 = KnownSample(4.7, 3.2, 1.3, 0.2, "Iris-setosa")
    sample4 = KnownSample(4.6, 3.1, 1.5, 0.2, "Iris-setosa")
    sample5 = KnownSample(5.0, 3.6, 1.4, 0.2, "Iris-setosa")
    test_sample = KnownSample(5.4, 3.9, 1.7, 0.4, "Iris-setosa")
    clf = Classifier(k=3, training_data=[sample1, sample2, sample3, sample4, sample5],
                     dist_algo=DistanceAlgos.ed4.value)  # noqa
    print("predicted_species:->", clf.classify(test_sample))
