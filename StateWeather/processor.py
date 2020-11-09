
from StateWeather.spreaddata import SpreadData
from StateWeather import utils


def main(filepath):
    if not filepath:
        return None

    with open(filepath, 'rt') as f:
        lp = utils.LineParser()
        header = {'Dy':0, 'MxT':1, 'MnT':2}
        data = SpreadData(header)

        for line in f:
            lp.process_line(line, data, data.get_min_spread)

        print(f"Min day: {data.min_day} spread: {data.min_spread}")

            


if __name__ == "__main__":
    main('./weather.dat')