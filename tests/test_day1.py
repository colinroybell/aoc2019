from day1 import fuel_needed

def test_fuel_needed_1a():
    ''' Given inputs to fuel_needed for day 1b '''
    assert(fuel_needed(12, 'a') == 2)
    assert(fuel_needed(14, 'a') == 2)
    assert(fuel_needed(1969, 'a') == 654)
    assert(fuel_needed(100756, 'a') == 33583)


def test_fuel_needed():
    ''' Given inputs to fuel_needed for day 1b '''
    assert(fuel_needed(12, 'b') == 2)
    assert(fuel_needed(14, 'b') == 2)
    assert(fuel_needed(1969, 'b') == 966)
    assert(fuel_needed(100756, 'b') == 50346)

