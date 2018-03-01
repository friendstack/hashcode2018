import argparse
from collections import namedtuple


Params = namedtuple('Params', field_names=['r', 'c', 'f', 'n', 'b', 't'])
Ride = namedtuple('Ride', field_names=['a', 'b', 'x', 'y', 's', 'f'])


def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str)

    return parser


def calc_metric(params, ride):
    return 1


def make_state(params):
    return [[0, 0] for _ in range(int(params.f))]


def simulate(params, rides):
    state = make_state(params)

    for s in range(int(params.t)):
        step(params, rides)


def step(params, rides):
    metrics = sorted([calc_metric(params, r) for r in rides])


def main():
    args = get_argparser().parse_args()

    params, rides = parse_rides(args)
    result = simulate(params, rides)


def parse_rides(args):
    with open(args.f, 'r') as f:
        params = Params(*f.readline().strip().split(' '))
        rides = []
        for line in f:
            rides.append(Ride(*line.strip().split()))
        return params, rides


if __name__ == '__main__':
    main()
