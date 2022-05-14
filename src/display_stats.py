from math import ceil
import os
import matplotlib.pyplot as plt
import pickle
import argparse
from constants import RANDOM_MIXIN


def display(path, frame_duration, outdir):
    with open(path, "rb") as f:
        data = pickle.load(f)
    
    if frame_duration is None:
        frame_duration = min(0.5, 10 / len(data))
    
    if outdir is not None and not os.path.isdir(outdir):
        os.makedirs(outdir)

    for i, l in enumerate(data):
        plt.clf()
        plt.xlim(0, len(l))
        plt.ylim(bottom=0, top=max(l) + 100)
        plt.ylabel("Agent score")
        plt.title(f"Epoch {i+1}")
        plt.scatter(list(range(len(l))), l, 5)
        plt.plot([len(l) - ceil(len(l) * RANDOM_MIXIN) - 1]*2, [0, 5001], color="orange", label="Random Mixin Threshold")
        plt.legend(loc="lower left")
        plt.pause(frame_duration)
        if outdir is not None:
            plt.savefig(os.path.join(outdir, f"epoch_{i}"))
    
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", metavar="INPUT_FILEPATH", type=str, default=None, help="Path to pickle file of data")
    parser.add_argument("-f", "--frameduration", metavar="FRAME_DURATION", type=float, default=None, help="Path to pickle file of data")
    parser.add_argument("-o", "--outdir", metavar="DIRECTORY", type=str, default=None, help="Save frames as pngs in the folder specified")
    args = parser.parse_args()

    if args.infile:
        display(args.infile, args.frameduration, args.outdir)


if __name__ == "__main__":
    main()
