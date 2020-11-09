class SpreadData:
    def __init__(self, header=None) -> None:
        self.data_items = []
        self.__header = header
        self.min_spread = 1000
        self.min_day = 0
        self.raw_header = None

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, header):
        if not self.__header:
            self.__header = header

    def get_min_spread(self, data):
        day = data['Dy']
        max_temp = data['MxT']
        min_temp = data['MnT']
        
        current_spread = max_temp - min_temp
        if current_spread < self.min_spread:
            self.min_spread = current_spread
            self.min_day = day