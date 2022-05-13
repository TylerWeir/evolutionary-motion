import matplotlib.pyplot as plt
import pickle
import argparse


def display(path, frame_duration):
    with open(path, "rb") as f:
        data = pickle.load(f)

    for l in data:
        plt.clf()
        plt.xlim(0, len(l))
        # plt.ylim(0, 5000)
        plt.plot(list(range(len(l))), l)
        plt.pause(frame_duration)
    
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", metavar="INPUT_FILEPATH", type=str, default=None, help="Path to pickle file of data")
    parser.add_argument("-f", "--frameduration", metavar="FRAME_DURATION", type=float, default=0.5, help="Path to pickle file of data")
    args = parser.parse_args()

    if args.infile:
        display(args.infile, args.frameduration)


if __name__ == "__main__":
    main()
