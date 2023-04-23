# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details

import math
from sample import Sample
from constants import DistanceAlgos as Da


class EuclideanDistance:
    """
    A class that calculates the Euclidean distance between two vectors of size 4 using math.hypot.

    >>> v1 = Sample(1, 2, 3, 4)
    >>> v2 = Sample(5, 6, 7, 8)
    >>> EuclideanDistance().get_distance(v1, v2)
    8.0

    >>> v1 = Sample(1, 2, 3, 4)
    >>> v2 = Sample(1, 2, 3, 4)
    >>> EuclideanDistance().get_distance(v1, v2)
    0.0
    """
    @staticmethod
    def get_distance(vect1: Sample, vect2: Sample):
        """
        Calculates and returns the Euclidean distance between the two vectors.

        Returns:
        - The Euclidean distance between the two vectors as a float.
        """
        dist = math.hypot(vect2.petal_width - vect1.petal_width,
                          vect2.petal_length - vect1.petal_length,
                          vect2.sepal_width - vect1.sepal_width,
                          vect2.sepal_length - vect1.sepal_length)
        return dist


class ManhattanDistance:
    """
    A class that calculates the Euclidean distance between two vectors of size 4 using math.hypot.

    >>> v1 = Sample(1, 2, 3, 4)
    >>> v2 = Sample(5, 6, 7, 8)
    >>> ManhattanDistance().get_distance(v1, v2)
    16.0

    >>> v1 = Sample(1, 2, 3, 4)
    >>> v2 = Sample(1, 2, 3, 4)
    >>> ManhattanDistance().get_distance(v1, v2)
    0.0
    """
    @staticmethod
    def get_distance(vect1: Sample, vect2: Sample):
        """
        Calculates and returns the Manhattan distance between the two vectors.

        Returns:
        - The Euclidean distance between the two vectors as a float.
        """
        dist = sum([vect2.petal_width - vect1.petal_width,
                    vect2.petal_length - vect1.petal_length,
                    vect2.sepal_width - vect1.sepal_width,
                    vect2.sepal_length - vect1.sepal_length])

        # converting to float for consistency with other distance algos
        dist = float(dist)
        return dist


class DistanceFactory:
    @staticmethod
    def get_distance_algo(dist_algo):
        if dist_algo == Da.ed4:
            return EuclideanDistance()
        elif dist_algo == Da.mh4:
            return ManhattanDistance()
        else:
            raise Exception(f"Invalid distance algorithm chosen: {dist_algo}")


if __name__ == "__main__":
    # testing
    vector1 = Sample(1, 2, 3, 4)
    vector2 = Sample(5, 6, 7, 8)
    vd = DistanceFactory.get_distance_algo(Da.ed4).get_distance(vector1, vector2)
    print(f"{vd = }")
    md = DistanceFactory.get_distance_algo(Da.mh4).get_distance(vector1, vector2)
    print(f"{md = }")
    import doctest
    doctest.testmod()
