import re


class CONSTS:
    LINETYPES = {'AGG': 'aggregate', 'DATA': 'data', 'HEADER': 'header'}
    STRIPCHARS = '*'
    SEPARATOR = '<SEP>'
    NAN = 'nan'


class REGEX:
    is_chars = re.compile(r"\A[A-Za-z]+?$")
    is_number = re.compile(r"\d?[.]??\d+")
    is_float = re.compile(r"\d+[.]\d+")
    is_integer = re.compile(r"\A\d+$")
    all_space = re.compile(r"\A\s+$")
