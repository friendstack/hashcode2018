import argparse
import math
from collections import namedtuple


Params = namedtuple('Params', field_names=['r', 'c', 'f', 'n', 'b', 't'])
Ride = namedtuple('Ride', field_names=['a', 'b', 'x', 'y', 's', 'f'])


def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str)

    return parser


def calculate_distance(a, b):
    return math.abs(a[0] - b[0]) + math.abs(a[1] - b[1])


def main():
    args = get_argparser().parse_args()

    rides, params = parse_rides(args)

    print(rides)
    print(params)


def parse_rides(args):
    with open(args.f, 'r') as f:
        params = Params(*f.readline().strip().split(' '))
        rides = []
        for line in f:
            rides.append(Ride(*line.strip().split()))
        return params, rides


if __name__ == '__main__':
    main()
