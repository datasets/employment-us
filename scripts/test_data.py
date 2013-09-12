from data import *

parser = Parser()
def test_get_row():
    line = '2006 (1)......................  228,815    151,428      66.2 144,427 63.1        2,206     142,221      7,001       4.6      77,387'
    row = parser.get_row(line)
    assert row[0] == '2006'
    assert row[-1] == '1'
    assert row[1] == '228815'


def test_parse_1():
    fo = file('aat1.txt')
    title, rows, fns = parser.parse_1(fo)
    assert title == '1.  Employment status of the civilian noninstitutional population, 1940 to date'
    assert rows[0][0].startswith('1940')
    assert rows[-1][0].startswith('2006')
    assert len(rows) == 2007-1939
    assert len(fns) == 1
    assert fns[0].startswith('1 Not strictly')
    assert fns[0].endswith('Estimates of Error.')


def test_parse_2():
    fo = file('aat2.txt')
    title, rows, fns = parser.parse_2(fo)
    assert title == '2.  Employment status of the civilian noninstitutional population 16 years and over by sex, 1971 to date' 
    assert len(rows) == 2 * (2006-1971) + 2
    assert rows[0][0].startswith('1971')
    assert rows[-1][0].startswith('2006')


