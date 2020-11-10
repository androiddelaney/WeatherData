
from StateWeather.spreaddata import SpreadData
from StateWeather.utils import RowParser


def main(filepath):
    if not filepath:
        return None

    with open(filepath, 'rt') as f:
        rp = RowParser()
        header = {'Dy':0, 'MxT':1, 'MnT':2}
        get_min_spread_key_map = {'Day': 'Dy', 'Min': 'MnT', 'Max':'MxT'}
        data = SpreadData(header, get_min_spread_key_map)

        for line in f:
            rp.process_line(line, data, data.get_min_spread)

        print(f"Min day: {data.min_day} spread: {data.min_spread}")

            


if __name__ == "__main__":
    main('./weather.dat')