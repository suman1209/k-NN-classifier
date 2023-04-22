# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details
from sample import UnknownSample
from constants import DistanceAlgos


class Classifier:
    """ this class is responsible for the classification of the sample"""
    def __init__(self, k: int, dist_algo: str = DistanceAlgos.ed.value):
        self.k = k
        self.dist_algo = dist_algo

    def classify(self, unknownsample: UnknownSample):
        # @todo to be continued
        pass
