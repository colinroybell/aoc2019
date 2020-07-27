def fuel_needed(mass, part):
    assert(part == 'a' or part == 'b')
    fuel_sum = 0
    while mass > 0:
            fuel = mass // 3 - 2
            if fuel < 0:
                fuel = 0           
            fuel_sum += fuel
            # Only recurse for part b    
            if (part == 'a'):
                fuel = 0    
            mass = fuel
    return fuel_sum
