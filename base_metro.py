class Train:
    """
    Hold information of a train.
    @method: __init__   : magic method, initialize information
    of the train
        @param and attribute: position: the station that the train
        currently in (Station)
        @param and attribute: order: index of the train (int)
    @method: __str__    : magic method, return the string
    representation of the train.
        format: 'T' + order (str)
    """
    def __init__(self, position, order):
        '''
        @method: __init__   : magic method, initialize information
        of the train
            @param and attribute: position: the station that the train
            currently in (Station)
            @param and attribute: order: index of the train (int)
            @attribute: next_station: the station that the train
            is scheduled next turn (Station, default None)
        '''
        self.position = position
        self.order = order
        self.next_station = None

    def __str__(self):
        '''
        Return the string representation of the train.
            format: 'T' + order (str)
        '''
        return 'T' + str(self.order)


class Station:
    """
    Hold information and status of a station.

    @method: __init__: magic method, initialize behavior of the station
        @param and attribute: index: index of the station (int)
        @param and attribute: name: name of the station (str)
        @param and attribute: line: a single line of the station (Line)
    @method: __str__ : magic method, return the string representation of
    the station.
        format: station name + station's position (str)
    @method: position: return the position of the station at present
        format: current line + station's index (str)
    @method: add_line(line_name): add line_name to line_list if not added yet
    """

    def __init__(self, index, name, line):
        """
        Init magic method that defines the initialization behavior of an object
        (the station).
            @param and attribute: index: index of the station (int)
            @param and attribute: name: name of the station (str)
            @param and attribute: line: a single line of the station (Line)
            @attribute: line_list: a list of line names that the station
                        belongs to (list)
            @attribute: busy: status of the station at present
                        (bool, default False)
            @attribute: alter_station: the alternative station that
                        considered the same at the current station in
                        circular line (Station, default None)
        """
        self.index = int(index)
        self.name = name
        self.line = line
        self.line_list = [str(self.line)]
        self.busy = False
        self.alter_station = None

    def __str__(self):
        """
        Magic method, return the string representation of the station under
            format: station name + station's position. (str)
        """
        if not self.alter_station:
            return self.name + '(' + self.position() + ')'
        # else
        return self.name + '(' + self.position() + '&'
        + str(self.alter_station.index) + ')'

    def position(self):
        """
        Return current position of the station.
            format: current line + ':' + station's index. (str)
        """
        return str(self.line) + ':' + str(self.index)

    def add_line(self, line_name):
        """
        Append line_name to line_list if not added yet.
            @param: line_name: line name need to be added (str)
        """
        if line_name not in self.line_list:
            self.line_list.append(line_name)

    def add_alter(self, alter_station):
        '''
        Add current station to the alternative station's alter_station
        attribute and vice versa.
            @param: alter_station: alternative station (Station)
        '''
        self.alter_station = alter_station
        alter_station.alter_station = self


class Line:
    """
    Hold information of a line: line name and station list on the line, every
    item in station list is an object of class Station.

    @method: __init__   : magic method, initialize behavior of the line
        @param and attribute: name: line name (str)
        @param and attribute: station_list: list of station on the line (list)
    @method: __str__    : magic method, return the string representation of
                          the station
    @method: print_stations : print all stations of the line, line by line
    @method: find_station   : find station base on value parameter
    """
    def __init__(self, name, station_list=[]):
        """
        Init magic method that defines the initialization behavior of an object
        (the line).
            @param and attribute: name: line name
            @param and attribute: station_list: list of station on the line
        """
        self.name = name
        self.station_list = station_list

    def __str__(self):
        """
        Magic method, return the string representation of the line under
        format: line name.
        """
        return self.name

    def find_station(self, value):
        """
        Find station base on value parameter.

        @param: value: value with format station name or index or
                       line name + index
        @return: station: station (object of class Station) if find, else None
        """
        for station in self.station_list:
            if station.name == value or station.position() == value or\
               station.index == value:
                return station
        return None


class Path:
    """
    Hold information of a path.

        @@method: __init__: magic method, initialize information
        of the path
    """

    def __init__(self, index, station_list, cost, delta):
        """
        Magic method, initialize information of the path.

            @attribute: index: index of a path
            @attribute: station_list: list of stations
            @attribute: cost: number of turns
            @attribute: delta: 2 if cross in path, else 1
            @attribute: train_number: number of trains
            @attribute: train_list: list of trains
        """
        self.index = index
        self.station_list = station_list
        self.cost = cost
        self.delta = delta
        self.train_number = 0
        self.train_list = None
