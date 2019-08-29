#!/usr/bin/env python3

from base_metro import Train, Path


def print_train(train_list, metro):
    """
    Get the train and print them.

        @param: train_list: list of all trains
        @param: metro: main Map object of program
    """

    def print_start():
        """
        Get the trains at start station and print them.
        """
        if start_list:
            print(metro.start_station, end='-')
        for train in start_list:
            if train == start_list[-1]:
                print(train, end='|')
            else:
                print(train, end=',')

    def print_normal_station():
        """
        Get the trains at normal station and print them.
        """
        if normal_list:
            normal_list.reverse()
            for train in normal_list:
                if train == normal_list[-1] and not end_list:
                    print(str(train.position) + '-' + str(train), end='')
                else:
                    print(str(train.position) + '-' + str(train), end='|')

    def print_end_station():
        """
        Get the trains at end station and print them.
        """
        if end_list:
            print(metro.end_station, end='-')
        for train in end_list:
            if train == end_list[-1]:
                print(train, end='')
            else:
                print(train, end=',')
        print('\n')

    start_list = []
    normal_list = []
    end_list = []
    for train in train_list:
        if train.position == metro.start_station:
            start_list.append(train)
        elif train.position == metro.end_station:
            end_list.append(train)
        else:
            normal_list.append(train)
    print_start()
    print_normal_station()
    print_end_station()


def check_if_all_train_arrived_end(metro, train_list):
    """
    Check if all train had arrived at the end station.

        @param: metro: main Map object of program
        @param: train_list: list of all trains
        @return: True or False
    """
    for train in train_list:
        if train.position != metro.end_station:
            return False
    return True


def get_busy_station(train_list, end):
    """
    Get the list of station that already had train in it.

        @param: train_list: list of all trains
        @param: end: end station
        @return: busy_station_list: list of busy stations
    """
    busy_station_list = []
    for train in train_list:
        if train.next_station != end:
            busy_station_list.append(train.next_station)
    return busy_station_list


def get_next_step(busy_station_list, train, path):
    """
    Get the next step base on the train's path.

        @param: busy_station_list: list of busy stations
        @param: train: current train
        @param: path: path from start to end
        @return: train: current train
        @return: busy_station_list: list of busy stations
    """

    def get_next_train_and_station_list():
        """
        Get next train and station list from path.

            @return: train: current train
            @return: busy_station_list: list of busy stations
        """
        if path[index + 1] not in busy_station_list:
            train.next_station = path[index + 1]
            busy_station_list.append(path[index + 1])
            return train, busy_station_list
        else:
            train.next_station = train.position
            return train, busy_station_list

    for index, station in enumerate(path):
        if station == train.position:
            try:
                return get_next_train_and_station_list()
            except IndexError:
                pass


def get_next_step_for_all_train(busy_station_list, train_list, path):
    """
    Get the next step base on the train's path.

        @param: busy_station_list: list of busy stations
        @param and return: train_list: list of trains
    """
    for index, _ in enumerate(train_list):
        try:
            train_list[index], busy_station_list =\
                get_next_step(busy_station_list, train_list[index], path)
        except (IndexError, TypeError):
            pass
    return train_list


def change_position(busy_station_list, train_list, path):
    """
    Take train, get the next step and turn position in to next step.

        @param: busy_station_list: list of busy stations
        @param: path: path from start to end
        @param and return: train_list: list of trains
    """
    train_list = get_next_step_for_all_train(busy_station_list,
                                             train_list,
                                             path)
    for index, _ in enumerate(train_list):
        train_list[index].position = train_list[index].next_station
    return train_list


def find_delta(station_list, cross_dictionary):
    """
    Return 2 if there any cross in a path, else return 1

        @param: station_list: list of stations
        @param: cross_dictionary: a dictionary with keys are station names and
                                  values are all lines according to
                                  station keys
        @return: int
    """
    for station in station_list:
        if station.name in cross_dictionary:
            return 2
    return 1


def split_train(train_number, path_list, cross_dictionary):
    """
    Return a list of path object with every has it own train number

        @param: train_number: number of trains
        @param: path_list: list of all paths from start to end
        @param: cross_dictionary: a dictionary with keys are station names and
                                  values are all lines according to
                                  station keys
        @return: path_object_list: a list that content all Path's objects
    """
    path_object_list = []
    for index, path in enumerate(path_list):
        path_object_list.append(Path(index,
                                     path,
                                     len(path) - 1,
                                     find_delta(path, cross_dictionary)))
    i = 1
    while i < train_number + 1:
        path_object_list.sort(key=lambda path: path.cost)
        path_object_list[0].cost += path_object_list[0].delta
        path_object_list[0].train_number += 1
        i += 1
    return path_object_list


def get_all_train(path_list):
    """
    Get all train in every path in path list

        @param: path_list: list of all paths from start to end
        @return: all_train: list of all trains
    """
    all_train = []
    for path in path_list:
        all_train.extend(path.train_list)
    return all_train


def get_path_object_list(metro, path_list):
    """
    Create path object list.

        @param: metro: main Map object of program
        @return: path_list: list of all paths
    """
    path_list = split_train(metro.train_number,
                            path_list,
                            metro.cross_dictionary)
    order = 1
    for path in path_list:
        train_list = [''] * path.train_number
        for index, _ in enumerate(train_list):
            train_list[index] = Train(metro.start_station, order)
            order += 1
        path.train_list = train_list
    return path_list


def move_the_train(path_list, metro):
    """
    Change train's position in all path and return new path list for the
    print function to work.

        @param: metro: main Map object of program
        @param and return: path_list: list of all paths
    """
    for index, path in enumerate(path_list):
        busy_station_list = get_busy_station(path.train_list,
                                             metro.end_station)
        path_list[index].train_list\
            = change_position(busy_station_list, path_list[index].train_list,
                              path.station_list)
    return path_list
