#!/usr/bin/env python3

from map_metro import Map
from read_input import analyze_all_data, take_input_args
from run_metro import get_path_object_list, get_all_train, move_the_train,\
    print_train, check_if_all_train_arrived_end


def main():
    """
    This is main function of this project.
    """
    filename, algo = take_input_args()
    line_list, cross_dictionary, special_data = analyze_all_data(filename)
    # create metro map
    metro = Map(line_list, special_data, cross_dictionary)
    # choose algorithm to run and print
    if algo == 2:
        path_list = get_path_object_list(metro, metro.find_possible_paths())
    # if algo = 1
    else:
        path_list = get_path_object_list(metro, metro.get_shortest_path())

    all_train = get_all_train(path_list)

    i = 0
    while not check_if_all_train_arrived_end(metro, all_train):
        i += 1
        print('Turn:', i)
        path_list = move_the_train(path_list, metro)
        all_train = get_all_train(path_list)
        print_train(all_train, metro)
    print('Total turn:', i)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
