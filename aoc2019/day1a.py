from day1 import fuel_needed

fuel_sum = 0

with open('data/day1.txt','r') as f:
    for line in f:
        mass = int(line)
        fuel_sum += fuel_needed(mass, 'a')

print(fuel_sum)        

