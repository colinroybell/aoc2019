from day2 import State

def test_2a():
    ''' Given inputs to fuel_needed for day 1b '''
    state = State("1,9,10,3,2,3,11,0,99,30,40,50")
    assert (state.run()==3500)
    state = State("1,0,0,0,99")
    assert (state.run()==2)
    state = State("2,3,0,3,99")
    assert (state.run()==2)
    state = State("2,4,4,5,99,0")
    assert (state.run()==2)
    state = State("1,1,1,4,99,5,6,0,99")
    assert (state.run()==30)