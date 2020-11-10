class SpreadData:
    def __init__(self, header=None, key_map=None) -> None:
        self.data_items = []
        self.__header = header
        self.min_spread = 1000
        self.min_day = 0
        self.raw_header = None
        self.key_map = key_map

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, header):
        if not self.__header:
            self.__header = header

    def get_min_spread(self, data):
        expected = ['Day', 'Max', 'Min']
        
        if self.key_map:
            l = [k for k in expected if k not in self.key_map]
            if len(l) == 0:                
                day = data[self.key_map['Day']]
                max_temp = data[self.key_map['Max']]
                min_temp = data[self.key_map['Min']]
        
                current_spread = max_temp - min_temp
                if current_spread < self.min_spread:
                    self.min_spread = current_spread
                    self.min_day = day