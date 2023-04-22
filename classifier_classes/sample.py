# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details


class Sample:
    """This class represents a sample of the iris plant and the corresponding methods"""
    def __init__(self, sepal_length: float, sepal_width: float,
                 petal_length: float, petal_width: float):
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.classification: str | type(None) = None


class KnownSample(Sample):
    def __init__(self, sepal_length: float, sepal_width: float,
                 petal_length: float, petal_width: float, species: str):
        super().__init__(sepal_length, sepal_width, petal_length, petal_width)
        self.species = species
        self.train: bool | type(None) = None
        self.val: bool | type(None) = None
        self.hp_tuning: bool | type(None) = None

    def __repr__(self):
        return f"KnownSample(sepal_length={self.sepal_length}, sepal_width={self.sepal_width}, " \
               f"petal_length={self.petal_length}, petal_width={self.petal_width}, species={self.species})"


class UnknownSample(Sample):
    def __int__(self, sepal_length: float, sepal_width: float,
                petal_length: float, petal_width: float):
        super().__init__(sepal_length, sepal_width, petal_length, petal_width)

    def __repr__(self):
        return f"KnownSample(sepal_length={self.sepal_length}, sepal_width={self.sepal_width}, " \
               f"petal_length={self.petal_length}, petal_width={self.petal_width})"
