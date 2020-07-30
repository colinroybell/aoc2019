import sys

cache = {}
def cases(part, digits, last_digit, last_digit_count, double, minimum, maximum):
    state = (digits,last_digit,last_digit_count,double,minimum,maximum)
    print("Called with {}".format(state))
    if state in cache:
        print("In cache: {}".format(cache[state]))
        return cache[state]
    count = 0
    minimum_first_digit = int(minimum[0])
    maximum_first_digit = int(maximum[0])

    min_digit = max(minimum_first_digit, last_digit)
    max_digit = min(maximum_first_digit, 9)

    for d in range(min_digit, max_digit + 1):
        if part == 'a':
           new_double = double or (d == last_digit)
           # Don't need to track last digit count
           new_last_digit_count = 0
        else:
           new_double = double or \
               (d != last_digit and last_digit_count == 2)
           if d == last_digit:
               new_last_digit_count = last_digit_count + 1
           else:
               new_last_digit_count = 1     

        new_minimum = "0"*(digits-1)
        new_maximum = "9"*(digits-1)
        if d == min_digit:
            new_minimum = minimum[1:]
        if d == max_digit:
            new_maximum = maximum[1:]

        if digits == 1:
            # Need the extra condition in the 'b' case. Has already been
            # taken into account in the 'a' case
            if new_double or (d == last_digit and last_digit_count == 1):
                count += 1
        else:
            count += cases(part, digits-1, d, new_last_digit_count, new_double, new_minimum, new_maximum)
    cache[state] = count
    print("{} -> {}".format(state,count))        
    return count
    
def day4a():
    return cases('a', 6, -1, 0, False, "145852", "616942")

def day4b():
    return cases('b', 6, -1, 0, False, "145852", "616942")

if __name__ == "__main__":
    if 'a' in sys.argv:
        print(day4a())
    if 'b' in sys.argv:
        print(day4b())    