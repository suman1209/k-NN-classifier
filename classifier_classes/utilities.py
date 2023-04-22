# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details
import random
import doctest


def split_list(input_list, *percentages):
    """
    Splits a list into multiple components based on predefined percentages.

    Args:
        input_list (list): The input list to split.
        *percentages (float): The percentages of inputs for each component (between 0 and 1).

    Returns:
        A tuple of lists: the split components.

    Examples:
        >>> in_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> c1, c2, c3 = split_list(in_list, 0.4, 0.3, 0.1)
        >>> len(c1)
        4
        >>> len(c2)
        3
        >>> len(c3)
        3
    """
    # Calculate the length of each component based on the predefined percentages
    total_length = len(input_list)
    component_lengths = [int(total_length * p) for p in percentages]
    # If there is a remaining percentage, ignore it and add the remaining elements to the last component
    component_lengths[-1] = total_length - sum(component_lengths[:-1])

    # Split the input list into components
    components = []
    remaining_list = input_list.copy()
    for length in component_lengths[:-1]:
        # Randomly sample elements from the remaining list to create the next component
        component = random.sample(remaining_list, length)
        components.append(component)
        # Remove the selected elements from the remaining list
        remaining_list = [x for x in remaining_list if x not in component]
    # Add the remaining elements to the last component
    components.append(remaining_list)

    # Return the components as a tuple
    return tuple(components)


if __name__ == "__main__":
    # test run
    print(split_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 0.6, 0.3, 0.1))
    # Run the doctests
    doctest.testmod()
