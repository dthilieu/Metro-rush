#!/usr/bin/env python3

from base_metro import Line, Station
from sys import stderr
from argparse import ArgumentParser, RawDescriptionHelpFormatter


def analyze_single_line(line_data, cross_dictionary, special_data,
                        station_list, line_list, current_line):
    """
    Analyze single raw line data.

        @param: line_data: a single raw data
    """

    def update_line(current_line, station_list, line_list):
        """
        Update line object information under specific condition.

        @param: current_line: current line name object
        @param: station_list: current list of stations
        @param: line_list: current list of lines
        """

        current_line.station_list = station_list
        line_list.append(current_line)
        # if line is circle, add the first and the last to their alter.
        if station_list[0].name == station_list[-1].name:
            station_list[0].add_alter(station_list[-1])

    def create_line(line_data):
        """
        Create line object base on line name.

        @param: line_data: current data line information
        @return: line object according to line name
        """

        line_name = line_data[1:]
        return Line(line_name)

    def get_special_station(line_data):
        """
        Get special data (start train, end train and number of trains).

        @param: line_data: current data line information
        @return: type, position: information of special data accordingly
        """

        type, position = line_data.split('=')
        return type, position

    def create_station(line_data, current_line):
        """
        Create station object base on index, station name and line name
        information.

        @param: line_data: current line name
        @param: current_line: current line name
        @return: station object
        """

        index, name = line_data.split(':')
        return Station(index, name, current_line)

    def create_cross(line_data, current_line):
        """
        Create station with cross line informaton.

        @param: line_data: current line name
        @param: current_line: current line name object
        @return: cross: station object with cross line informaton added
        """

        line_data, cross_line = line_data.split(':Conn: ')
        cross = create_station(line_data, current_line)
        cross.add_line(cross_line)
        return cross

    ################################################
    #   Analyze data under specific condition.     #
    ###############################################

    # Raw data line that includes line name.
    if line_data.startswith('#'):
        # Check if there is a line object with the same name set up yet, update
        if current_line and station_list:
            update_line(current_line, station_list, line_list)
        # Create new line object if not exist yet.
        current_line = create_line(line_data)
        station_list = []

    # Raw data line that includes special data.
    elif '=' in line_data:
        # Check if there is special_data yet, update if yes.
        if not special_data:
            update_line(current_line, station_list, line_list)
        # Add special data to special_data dictionary.
        type, position = get_special_station(line_data)
        special_data[type] = position

    # Raw data line that includes cross line station data.
    elif ':Conn:' in line_data:
        station = create_cross(line_data, current_line)
        # If new cross line, append to cross dictionary.
        if station.name not in cross_dictionary:
            cross_dictionary[station.name] = station.line_list
        else:
            # get old lines from cross dictionary
            old_lines = cross_dictionary[station.name]
            # add line to the new station
            for line in old_lines:
                station.add_line(line)
            # set value for cross in cross dictionary
            cross_dictionary[station.name] = station.line_list
            # add line to the old station with same name
            for old_line in line_list:
                old_station = old_line.find_station(station.name)
                if old_station:
                    old_station.line_list = station.line_list
        station_list.append(station)

    # Normal station
    else:
        station = create_station(line_data, current_line)
        # after set the station, append it to list
        station_list.append(station)

    return station_list, current_line


def analyze_all_data(filename):
    """
    Analyze data under graph data structure base on raw data.

        @return: line_list: a list of line objects (line names)
        @return: cross_dictionary: a dictionary with keys are station names and
        values are all lines according to station keys
        @return: special_data: a dictionary with keys are start train,
                 end train and number of train and values are their
                 information accordingly
    """

    def get_data():
        """
        Get raw data under line by line format from file.

            @return: data: raw data under line by line format from file.
        """

        try:
            fd = open(filename, 'r')
            data = fd.read()
            fd.close()
        except FileNotFoundError:
            print_error_and_exit('file')
        except PermissionError:
            print_error_and_exit('permission')
        except IsADirectoryError:
            print_error_and_exit('dir')
        except UnicodeDecodeError:
            print_error_and_exit('data')
        # Split data into lines
        data = data.splitlines()
        # Remove empty lines
        while '' in data:
            data.remove('')
        return data

    # get data from file
    data = get_data()
    # Create default variables
    current_line = Line(None)
    cross_dictionary = {}
    special_data = {}
    station_list = []
    line_list = []

    # Analyze all data
    for line_data in data:
        station_list, current_line\
         = analyze_single_line(line_data, cross_dictionary, special_data,
                               station_list, line_list, current_line)

    # check if final data is valid
    if station_list and line_list and len(special_data) == 3:
        return line_list, cross_dictionary, special_data
    else:
        print_error_and_exit('data')


def print_error_and_exit(error):
    '''
    Print the error message to stderr and exit with status 1.

        @param: error: error signal
    '''
    error_messages = {
        'file': 'File not found.',
        'permission': 'Permission denied.',
        'data': 'Invalid file.',
        'dir': 'Can not read directory.',
        'end': 'All the trains have reached the end station.'
    }
    if error in error_messages:
        print(error_messages[error], file=stderr)
    else:
        print('Unidentified error occurs.', file=stderr)
    exit(1)


def take_input_args():
    '''
    Take and return the filename and algorithm arguments from input.
    '''
    parser = ArgumentParser(
        description='The Delhi Metro network problem solver',
        formatter_class=RawDescriptionHelpFormatter,
        epilog='''\
                -------------------------------
                Possible choices for algorithm:
                -------------------------------
                    1 (All trains follow one shortest way.)
                    2 (Divided trains into possible ways to optimize cost.)
         ''')
    parser.add_argument('filename', action='store',
                        help='A file that contains a list of metro lines\
                        and metro stations. File must be format correctly.')
    parser.add_argument('--algo', action='store', choices=[1, 2], type=int,
                        default=2, help='The algorithm you choose to solve\
                            the problem. Default 2')
    return parser.parse_args().filename, parser.parse_args().algo
