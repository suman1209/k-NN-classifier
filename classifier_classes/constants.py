# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details

from enum import Enum


class ConstantNames(Enum):
    sepal_length = "sepal_length"
    sepal_width = "sepal_width"
    petal_length = "petal_length"
    petal_width = "petal_width"
    species = "species"


class SplitPercentage(Enum):
    train: float = 0.5
    hp_tuning: float = 0.2
    validation: float = 0.3


class DistanceAlgos:
    ed = "Euclidian"


if __name__ == "__main__":
    print(SplitPercentage.train.value)
