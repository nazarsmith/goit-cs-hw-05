import argparse

parser = argparse.ArgumentParser(
    description="""
    "Read documents, sort them by extension, and copy to a folder of your choice.
    Both the source and the destination folder must be provided.
    """
)
parser.add_argument(
    "source",
    metavar="source",
    nargs=1,
    help="source path to the directory that has files to be read and sorted. Mandatory argument.",
)
parser.add_argument(
    "destination",
    metavar="destination",
    nargs=1,
    help="destination path where the files will be copied and sorted. Mandatory argument.",
)
