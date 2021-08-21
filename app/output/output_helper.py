import os


def output_path(file_name):
    """Simple function to generate output path"""

    output_folder = os.path.expanduser("~") + "/Downloads/"
    output_file_path = os.path.normpath(output_folder + file_name)
    return output_file_path
