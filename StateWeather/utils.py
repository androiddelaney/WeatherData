import re
from StateWeather.spreaddata import SpreadData
from StateWeather.constants import CONSTS as consts
from StateWeather.constants import REGEX


class RowParser():

    def get_line_type(self, line, re_separator='\s+'):
        if not line:
            return None

        parts = re.sub(re_separator, consts.SEPARATOR, line.strip()).split('<SEP>')

        if len(parts) > 1:
            if REGEX.is_chars.match(parts[0]) and REGEX.is_chars.match(parts[1]):
                return consts.LINETYPES["HEADER"]
            elif REGEX.is_number.match(parts[0]):
                return consts.LINETYPES["DATA"]
            elif REGEX.is_chars.match(parts[0]) and REGEX.is_number.match(parts[1]):
                return consts.LINETYPES["AGG"]
        return None

    def get_line_items(self, line_type, line, header=None):
        parts = line.split()
        if line_type == consts.LINETYPES['HEADER']:
            return self.process_header(parts)
        elif line_type == consts.LINETYPES['DATA']:
            return self.process_data(parts, header)
        return None

    def process_line(self, line, data_object: SpreadData, func=None):
        line_type = self.get_line_type(line)

        if line_type == consts.LINETYPES['HEADER']:
            data_object.header = self.get_line_items(line_type, line)
            data_object.raw_header = line
        elif line_type == consts.LINETYPES['DATA']:
            updated_line = self.insert_missing_values(data_object.raw_header, line)
            values = self.get_line_items(line_type, updated_line, data_object.header)
            if func:
                func(values)
            data_object.data_items.append(values)

    def process_header(self, parts):
        if not parts:
            return None
        elif not isinstance(parts, list):
            return {parts: 0}
        names = dict()
        for i, v in enumerate(parts):
            names[v] = i
        return names

    def process_data(self, parts, header):
        if not parts or not header:
            return None
        header_len = len(header)

        h = [None] * header_len
        for key, value in header.items():
            h[value] = key

        data = dict()
        for i, v in enumerate(parts):
            if i >= header_len:
                break

            if h[i]:
                data[h[i]] = self.clean_value(v.strip(consts.STRIPCHARS))
        return data

    def clean_value(self, value):
        if value.lower().islower():
            return value
        else:
            if REGEX.is_integer.match(value):
                return int(value)
            elif REGEX.is_float.match(value):
                return float(value)

        return consts.NAN  # TODO define path to this scenario ....

    def find_next_start(self, line, position):
        offset_to_next = None
        line_len = len(line)
        if position >= line_len:
            return offset_to_next

        while not offset_to_next:

            seen_spaces = False
            if line[position].isalnum():
                next_pos = position + 1
                while True:
                    if next_pos > len(line) - 1:
                        if not seen_spaces:
                            return len(line) - 1
                        offset_to_next = next_pos
                        break
                    if not seen_spaces:
                        if line[next_pos].isspace():
                            seen_spaces = True
                        next_pos += 1
                    elif seen_spaces:
                        if line[next_pos].isalnum():
                            offset_to_next = next_pos - 1
                            break
                        else:
                            next_pos += 1
            else:
                position += 1

        return offset_to_next

    def insert_missing_values(self, header, data):
        current_pos = 0

        while current_pos < len(header):
            offset_to_next_header = 0

            if header[current_pos].isalnum():
                offset_to_next_header = self.find_next_start(header, current_pos)

            if header[current_pos].isspace():
                current_pos += 1
                continue

            data_seg = data[current_pos:offset_to_next_header]
            if len(data_seg) == 0:
                break

            if REGEX.all_space.match(data_seg):
                insert_point = current_pos + \
                               ((offset_to_next_header - current_pos) // 2)
                start = data[:insert_point]
                end = data[insert_point + 1:]
                data = f"{start}x{end}"
                current_pos = offset_to_next_header
            else:
                current_pos = offset_to_next_header
        return data
