# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details

from enum import Enum


class Approximations:
    round_nearest_to = 2


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


class DistanceAlgos(Enum):
    ed4 = "Euclidian"
    mh4 = "Manhattan"


class Species(Enum):
    IrisSetosa = "Iris-setosa"
    IrisVersicolour = "Iris-versicolor"
    IrisVirginica = "Iris-virginica"

    @staticmethod
    def validate(value: str):
        allowed_species = set(item.value for item in Species)
        if value in allowed_species:
            return value
        else:
            raise ValueError(f"{value} is not an Invalid Species")


if __name__ == "__main__":
    print(SplitPercentage.train.value)
    # testing the Species classes
    print(Species.validate("Iris-setosa"))
    # testing the constant names
    print(ConstantNames.species.value, "type - ", type(ConstantNames.species.value))
