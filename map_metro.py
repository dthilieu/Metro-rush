#!/usr/bin/env python3
from sys import stderr
from read_input import print_error_and_exit


class Map:
    """
    Hold all information of map.
        @param and attribute: line_list: a list of line name
        @param and attribute: special_data: a dictionary with keys are start
                              train, end train and number of train with its
                              information accordingly
        @param and attribute: cross_dictionary: a dictionary with keys are
                              station names and values are all lines according
                              to station keys
    """
    def __init__(self, line_list, special_data, cross_dictionary):
        """
        Init magic method that defines the initialization behavior of an object
        (the map).

        @param: self: default param
        @param and attribute: line_list: a list of line name
        @param and attribute: special_data: a dictionary with keys are start
                              train, end train and number of train with its
                              information accordingly
        @param and attribute: cross_dictionary: a dictionary with keys are
                              station names and values are all lines according
                              to station keys
        """
        self.line_list = line_list
        self.cross_dictionary = cross_dictionary
        self.start_station = None
        self.end_station = None
        self.train_number = 0
        self.ignore_stations = []
        # set values for start & end station, number of trains
        self.set_init_data(special_data)
        self.possible_paths = []

    def set_init_data(self, special_data):

        def find_station(value):
            """
            Find station object from the map by line name & index.
            @param: value: line name & index (Ex: "Blue Line:1")
            @return: station: station (object of class Station) if find,
            else None
            """
            for line in self.line_list:
                station = line.find_station(value)
                if station:
                    return station
            return None

        def set_start_data():
            """
            Set value for special data.
            """
            for key, value in special_data.items():
                try:
                    # set values for attributes
                    if key == 'TRAINS':
                        self.train_number = int(value)
                    elif key == 'START':
                        self.start_station = find_station(value)
                    elif key == 'END':
                        self.end_station = find_station(value)
                    # if any extra data other than those 3, print error then
                    # exit
                    else:
                        raise ValueError
                except ValueError:
                    print_error_and_exit('data')

        def check_valid_data():
            """
            Check if data is valid or not, if not print error message and exit.
            """
            # check final information
            if self.train_number < 1 or not self.start_station\
               or not self.end_station:
                print_error_and_exit('data')
            # check if the start point is the same as end point
            if self.start_station == self.end_station\
               or self.start_station == self.end_station.alter_station:
                print_error_and_exit('end')

        def set_ignore_data():
            """
            Set data that need to be ignored.
            """
            self.ignore_stations = [self.start_station]
            if self.start_station.alter_station:
                self.ignore_stations.append(self.start_station.alter_station)

        set_start_data()
        check_valid_data()
        set_ignore_data()

    def get_line(self, line_name):
        """
        Find line object by line name.

            @param: name: name of line
            @return: line object if found, else None
        """
        for line in self.line_list:
            if line.name == line_name:
                return line
        return None

    def get_near_station_pairs(self, station, checked_stations={}):
        """
        Get near station pairs.

            @param: station: current station
            @param: checked_stations: checked stations, default value
                    empty list
            @return: near_station_list: list of near station
        """
        def get_next_station_pair(index):
            """
            Get next station pair, add to next_station_list.

                @param: index: index of the station (int)
            """
            next_index = [index+1, index-1]
            for idx in next_index:
                try:
                    next_station = line.find_station(idx)
                except AttributeError:
                    pass
                if next_station and next_station not in checked_station_list:
                    near_station_list.append([next_station, station])

        def find_cross_stations():
            """
            Find cross stations and insert to next_station_list (prioritize).

                @return: next_station_list: list of next stations
            """
            next_station_list = []
            for line_name in station.line_list:
                try:
                    line = self.get_line(line_name)
                    next_station = line.find_station(station.name)
                except AttributeError:
                    pass
                # if not found, move to next line
                if not next_station:
                    continue
                # if found, priority station in the destination line
                elif line == self.end_station.line:
                    next_station_list.insert(0, next_station)
                # add other stations
                else:
                    next_station_list.append(next_station)
            return next_station_list

        def add_cross_pairs():
            """
            Add cross pairs to near_station_list if not in checked_station_list

                @return: near_station_list: list of near stations
            """
            for next_station in next_station_list:
                if next_station not in checked_station_list:
                    near_station_list.append([next_station, station])
            return near_station_list

        def find_in_line_stations():
            """
            Find station stations in a line.

                @return: near_station_list: list of near stations
            """
            try:
                in_line_station = line.find_station(station.position())
            except AttributeError:
                pass
            # find next normal pairs
            get_next_station_pair(in_line_station.index)
            # if line is circle
            if in_line_station.alter_station:
                get_next_station_pair(in_line_station.alter_station.index)
            return near_station_list

        near_station_list = []
        checked_station_list = [key for key in checked_stations.keys()]
        checked_station_list += self.ignore_stations
        # if station is a cross
        if station.name in self.cross_dictionary:
            next_station_list = find_cross_stations()
            if next_station_list:
                near_station_list = add_cross_pairs()

        # find in line station
        line = station.line
        near_station_list = find_in_line_stations()
        return near_station_list

    def breadth_first_search(self, start, end):
        """
        Find the shortest path.

            @param: start: first station
            @param: end: end station
            @return: shortest path
        """
        def create_queue_stations_dict():
            """
            Create queue stations dictionary (path).

                @return: checked_stations: dictionary of checked stations,
                                           key is station, value is its
                                           pre_station
            """
            checked_stations = {}
            queue = [[start, end]]
            # find queue for bfs
            while queue:
                station, pre_station = queue.pop(0)
                checked_stations[station] = pre_station
                if station == end or station == end.alter_station:
                    break
                queue += self.get_near_station_pairs(station, checked_stations)
            return checked_stations

        def get_path_from_dict(start, end, path=[]):
            """
            Get path from checked_stations dictionary.

                @param: start: start station
                @param: end: end station
                @param: path: path from start to end, default value is empty
                              list
                @return: path: path from start to end, default value is empty
                              list
            """
            while start != end and start != end.alter_station:
                path.append(end)
                try:
                    end = checked_stations[end]
                except KeyError:
                    end = checked_stations[end.alter_station]
            return path

        def get_bfs_path():
            """
            Get shortest path from start to end.

                @return: path: shortest path from start to end
            """
            path = []
            # find path and add to list, from end to start
            if end in checked_stations or end.alter_station in\
               checked_stations:
                path = get_path_from_dict(start, end)
                # add start station to list
                path.append(start)
                # reverse to get the list from start to end
                path.reverse()
            return path

        checked_stations = create_queue_stations_dict()
        path = get_bfs_path()
        return path

    def find_possible_paths(self):
        '''
        Find all possible seperate paths from start to end station.
        (These paths have no station in common.)

            @return: possible_path: all possible paths from start to end
        '''

        def ignore_cross(station):
            """
            Ignore all related cross stations.

                @param: station: current station
            """
            if station == self.end_station or station == self.start_station:
                return
            for line_name in station.line_list:
                line = self.get_line(line_name)
                if not line:
                    continue
                cross = line.find_station(station.name)
                if cross not in self.ignore_stations:
                    self.ignore_stations.append(cross)

        def add_next_to_path():
            """
            If start next to end, add into possible path.
            """
            path = [self.start_station, self.end_station]
            if path not in self.possible_paths:
                self.possible_paths.append(path)

        def nearby_bfs():
            '''
            Do BFS for all the other stations that next to the start station.

                @return: path: path from start to end
            '''
            start = station_pair[0]
            path = self.breadth_first_search(start, self.end_station)
            if path:
                # add start point to path
                path.insert(0, self.start_station)
            return path

        def ignore_middle_stations():
            '''
            Add all the stations except first and last one to ignore list.
            '''
            for station in min_path[1:-1]:
                if station not in self.ignore_stations:
                    self.ignore_stations.append(station)
                    ignore_cross(station)

        # find all possible stations that next to the start station
        near_stations = self.get_near_station_pairs(self.start_station)
        while near_stations:
            min_path = []
            for station_pair in near_stations:
                # if start next to end, add it to path and continue to
                # next pair.
                if self.end_station in station_pair or\
                   self.end_station.alter_station in station_pair:
                    add_next_to_path()
                    continue
                # do BFS for all the other stations that next to the
                # start station.
                path = nearby_bfs()
                # compare it to min path and replace min path
                if not min_path or len(path) < len(min_path):
                    min_path = path
            # if shortest path found, append it to list
            if min_path:
                # add ignore stations
                ignore_middle_stations()
                # add full path to possible path list
                self.possible_paths.append(min_path)
                # check if any other way to search from start point
                near_stations = self.get_near_station_pairs(self.start_station)
            # if not any path found, end the process
            else:
                break
        return self.possible_paths

    def get_shortest_path(self):
        '''
        Return the shortest path from start to end station.
        '''
        min_path = []
        # get shortest path from all possible paths.
        for path in self.find_possible_paths():
            if not min_path or len(path) < len(min_path):
                min_path = path
        return [min_path]
