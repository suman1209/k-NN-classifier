# Copyright (c) 2023 Suman
# This software is released under the MIT License.
# Contact Suman via sumanrbt1997@gmail.com for further details
import random
import doctest
import os
import difflib
import re
# to get reproducible results
random.seed(10)


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


def compare_two_files(reflog_path: str, out_file_path: str, test_name: str,
                      diff_output_path="tests/regressions/test_output/",):
    """
    Parameter
    _________

    reflog_path: (str) path to the reflog file
    out_file_path: (str) path to the output file
    test_name: (str) name of the test, e.g. console, patterns_csv etc...
    Returns
    _______
    test_restult: (bool) True or False
    """
    assert os.path.exists(reflog_path), f"reflog {reflog_path} does not exists!"
    assert os.path.exists(out_file_path), f"out_file_path {out_file_path} does not exists!"

    # Importing difflib
    # get list of reflog lines
    with open(reflog_path) as file_1:
        reflog_path_text = file_1.readlines()

    # get list of out_file lines
    with open(out_file_path) as file_2:
        out_file_path_text = file_2.readlines()

    # Remove ANSI escape codes using regular expressions
    out_file_path_text_cleaned = []
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    for line in out_file_path_text:
        cleaned_line = ansi_escape.sub('', line)
        if cleaned_line:
            out_file_path_text_cleaned.append(cleaned_line.strip())

    reflog_path_text_cleaned = [line.strip() for line in reflog_path_text]
    # Compare files and get the result
    # Find and print the diff:
    line_diff = ""
    for line in difflib.unified_diff(
            reflog_path_text_cleaned, out_file_path_text_cleaned, fromfile='console_reflog_text',
            tofile='out_file_path_text_cleaned', lineterm=''):
        line_diff += line + "\n"
    with open(diff_output_path + f"{test_name}_diff.txt", "w") as diff_file:
        diff_file.write(line_diff)

    return reflog_path_text_cleaned == out_file_path_text_cleaned


if __name__ == "__main__":
    # test run
    print(split_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 0.6, 0.3, 0.1))
    # Run the doctests
    doctest.testmod()
