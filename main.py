import argparse
from collections import namedtuple


Params = namedtuple('Params', field_names=['r', 'c', 'f', 'n', 'b', 't'])
Ride = namedtuple('Ride', field_names=['a', 'b', 'x', 'y', 's', 'f'])


def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str)

    return parser


def calculate_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_wait_time(start, step):
    if start <= step:
        return 0
    return step - start

def get_bonus(distance_to_passenger, passenger_wait_time, step, bonus):
    can_get_bonus = distance_to_passenger + step <= passenger_wait_time;
    if can_get_bonus:
        return bonus
    return 0

def calc_metric(params, ride, vehicle, t, bonus_amount):
    passenger = [ride.a, ride.b]
    end_point = [ride.x, ride.y]
    distance_to_passenger = calculate_distance(vehicle, passenger)
    distance_to_end = calculate_distance(passenger, end_point)
    wait_time = get_wait_time(t, ride.s)
    bonus = get_bonus(distance_to_passenger, ride.s, t, bonus_amount)
    return distance_to_passenger + distance_to_end + wait_time - bonus


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
