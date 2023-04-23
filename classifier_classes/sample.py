# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details

from constants import ConstantNames as Cn
from constants import Species
from exceptions import InvalidSampleError


class Sample:
    """This class represents a sample of the iris plant and the corresponding methods"""
    def __init__(self, sepal_length: float, sepal_width: float,
                 petal_length: float, petal_width: float):
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.classification: str | type(None) = None

    def validate_input_data(self):
        assert self.sepal_length > 0, f"{Cn.sepal_length.value} = {self.sepal_length} <=0 is invalid!"
        assert self.sepal_width > 0, f"{Cn.sepal_width.value} = {self.sepal_width} <=0 is invalid!"
        assert self.petal_length > 0, f"{Cn.petal_length.value} = {self.petal_length} <=0 is invalid!"
        assert self.petal_width > 0, f"{Cn.petal_width.value} = {self.petal_width} <=0 is invalid!"


class KnownSample(Sample):
    def __init__(self, sepal_length: float, sepal_width: float,
                 petal_length: float, petal_width: float, species: str):
        super().__init__(sepal_length, sepal_width, petal_length, petal_width)
        self.validate_input_data()
        self.species = species
        self.train: bool | type(None) = None
        self.val: bool | type(None) = None
        self.hp_tuning: bool | type(None) = None

    @classmethod
    def from_dict(cls, row: dict[str, str]) -> "KnownSample":
        try:

            sample = cls(sepal_length=float(row[Cn.sepal_length.value]),  # noqa
                       sepal_width=float(row[Cn.sepal_width.value]), # noqa
                       petal_length=float(row[Cn.petal_length.value]), # noqa
                       petal_width=float(row[Cn.petal_width.value]), # noqa
                       species=Species.validate(row[Cn.species.value])) # noqa
            return sample
        except ValueError as val_error:
            raise InvalidSampleError(f"Sample {row} is invalid - {str(val_error)}")
        except Exception as exc:
            print(f"Error when constructing the KnownSample object - {str(exc)}")
            raise

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
