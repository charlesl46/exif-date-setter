from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser("exif-setter")

    # positional
    parser.add_argument("path",help="the path where to set exif metadata")

    # optional
    parser.add_argument("-v","--verbose",action="store_true")
    parser.add_argument("-d","--dry",action="store_true")
    parser.add_argument("-s","--single",action="store_true")

    args = parser.parse_args()
    return args