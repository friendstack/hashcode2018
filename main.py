import argparse
from collections import namedtuple


Params = namedtuple('Params', field_names=['r', 'c', 'f', 'n', 'b', 't'])
Ride = namedtuple('Ride', field_names=['a', 'b', 'x', 'y', 's', 'f', 'i'])

CARS = []


class Car(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_available = 0
        self.assigned_rides = []


class RideResult(object):
    def __init__(self, index, overall_distance, metric, ride):
        self.ride = ride
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
    distance_to_passenger = calculate_distance([vehicle.x, vehicle.y], passenger)
    distance_to_end = calculate_distance(passenger, end_point)
    wait_time = get_wait_time(t, ride.s)
    bonus = get_bonus(distance_to_passenger, ride.s, t, bonus_amount)
    time = distance_to_passenger + distance_to_end + wait_time
    metric = time - bonus
    return RideResult(ride.i, time, metric, ride)


def make_state(params):
    return [Car(0, 0) for _ in range(int(params.f))]


def simulate(params, rides):
    global CARS
    state = make_state(params)
    CARS = state

    for i, s in enumerate(range(int(params.t))):
        step(params, rides, i)


def free_cars(cars):
    for car in [i for i in cars if i.is_available > 0]:
        car.is_available -= 1


def assign_ride(rides, metric, car):
    car.assigned_rides.append(metric.index)
    car.is_available = metric.overall_distance
    rides.remove(metric.ride)


def step(params, rides, s):
    free_cars(CARS)
    freed_cars = [i for i in CARS if i.is_available == 0]
    for c in freed_cars:
        if rides:
            best_result = sorted([calc_metric(params, r, c, s, params.b) for r in rides], key=lambda x: x.metric)[0]
            print(best_result.__dict__)
            assign_ride(rides, best_result, c)


def main():
    args = get_argparser().parse_args()

    params, rides = parse_rides(args)

    simulate(params, rides)
    with open('result', 'w') as f:
        for i, c in enumerate(CARS):
            l = str(i) + ' '
            l += ' '.join(map(str, c.assigned_rides))
            f.write(l)
            f.write('\n')


def parse_rides(args):
    with open(args.f, 'r') as f:
        params = Params(*list(map(int, f.readline().strip().split(' '))))
        rides = []
        for i, line in enumerate(f):
            p = list(map(int, line.strip().split()))
            rides.append(Ride(*p, i))
        return params, rides


if __name__ == '__main__':
    main()
