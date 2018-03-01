import argparse
from collections import namedtuple


Params = namedtuple('Params', field_names=['r', 'c', 'f', 'n', 'b', 't'])
Ride = namedtuple('Ride', field_names=['a', 'b', 'x', 'y', 's', 'f'])

Cars = []


class Car(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_available = 0
        self.assigned_rides = []


class RideResult(object):
    def __init__(self, index, overall_distance, metric):
        self.index = index
        self.overall_distance = overall_distance
        self.metric = metric


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
    can_get_bonus = distance_to_passenger + step <= passenger_wait_time
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
    time = distance_to_passenger + distance_to_end + wait_time
    metric = time - bonus
    return RideResult(ride.index, time, metric)


def make_state(params):
    return [Car(0, 0) for _ in range(int(params.f))]


def simulate(params, rides):
    state = make_state(params)

    for s in range(int(params.t)):
        step(params, rides)


def free_cars(cars):
    for car in [i for i in cars if i.is_available > 0]:
        car.is_available -= 1


def assign_rides(metrics, freed_cars):
    for i, car in enumerate(freed_cars):
        car.assign_rides.push(metrics)
        car.is_available = metrics[i]


def step(params, rides):
    free_cars(Cars)
    freed_cars = [i for i in Cars if i.is_available == 0]
    metrics = sorted([calc_metric(params, r) for r in rides])
    assign_rides(metrics, freed_cars)


def main():
    args = get_argparser().parse_args()

    params, rides = parse_rides(args)

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
