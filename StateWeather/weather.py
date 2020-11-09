'''
you’ll find daily weather data for Morristown, NJ for June 2002.
 Write a program to output the day number (column one) 
 with the smallest temperature spread 
 (the maximum temperature is the second column, 
 the minimum the third column).
'''

            

class Weather():
    data_types = dict()

    def __init__(self, header):
        for key in header:
            Weather.data_types.get(key, None)


def min_spread():
    min_spread = 1000
    min_day = 0

    DAY = 'Dy'
    CITY = 'mo'

    with open('./weather.dat', 'r') as f:
        for line in f:
            weather_item = None
            parts = line.split()
            if len(parts) == 0:
                continue

            if parts[0] == DAY or parts[0] == CITY:
                continue

            if len(parts) < 3:
                continue
            try:

                day = int(parts[0])
                max_temp = int(parts[1].replace('*',''))
                min_temp = int(parts[2].replace('*', ''))
                current_spread = max_temp - min_temp
                if current_spread < min_spread:
                    min_spread = current_spread
                    min_day = day
                #print(f"{day}, {max_temp}, {min_temp}, {current_spread}")
                

            except:
                print("waiting!")

            

    return min_day

print(min_spread())