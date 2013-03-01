
from math import log, exp

def euclideanDist(vec1, vec2):
    sum = 0
    for elem1, elem2 in zip(vec1, vec2):
        sum += abs(elem1 - elem2)
    return sum

def vaporPressure(temperature, rel_humidity):
    return rel_humidity * 611 * exp(2.5e6 / 461.5 * (1 / 273.15 - 1 / temperature))

def mixedSaturatedParcel(args, initial_args):
    mixed_temperature, pressure, mixed_vapor_pres = args
    init_mixed_temperature, init_pressure, init_mixed_vapor_pres = initial_args

    mixed_saturation_temp = init_mixed_temperature + (2.5e6 * 0.622) / (pressure * 1005.) * (init_mixed_vapor_pres - vaporPressure(mixed_temperature, 1.))
    mixed_saturation_vapor_pres = vaporPressure(mixed_temperature, 1.)

    solution = [ (mixed_saturation_temp + mixed_temperature) / 2, pressure, (mixed_saturation_vapor_pres + mixed_vapor_pres) / 2 ]
#   print solution
    return solution

def condensationTemp(args, initial_args):
    A = 2.53e8
    B = 5.42e3

    temperature, pressure, mixing_ratio = args
    init_temperature, init_pressure, init_mixing_ratio = initial_args

    condensation_pres = init_pressure * (temperature / init_temperature) ** (7. / 2.)
    condensation_temp = B / log((0.622 * A) / (mixing_ratio * init_pressure) * (init_temperature / temperature) ** (7. / 2.))
    return [ condensation_temp, condensation_pres, mixing_ratio ]

def wetBulbTemp(args, initial_args):
    A = 2.53e8
    B = 5.42e3

    temperature, pressure, mixing_ratio = args
    init_temperature, init_pressure, init_mixing_ratio = initial_args

    wet_bulb_temp = init_temperature - (2.5e6 / 1005.) * (0.622 / pressure * A * exp(-B / temperature) - mixing_ratio)
    return [ wet_bulb_temp, pressure, mixing_ratio ]

def solveIteratively(func, args, first_guess=None, tolerance=1e-5):
    if first_guess is None: first_guess = args

    counter = 0
    solution = func(first_guess, args)
    last_solution = [ s + tolerance * 2 for s in solution ]
    while euclideanDist(solution, last_solution) > tolerance:
        last_solution = solution
        solution = func(last_solution, args)

        counter += 1
#       if counter > 30:
#           print "Too many iterations ..."
#           return [ -999 for a in args ]
    return solution

def main():
    print "Condensation Temperature:"
    solution = solveIteratively(condensationTemp, [ 299.87, 95.25, 17.005e-3 ])
    print "Temperature:", solution[0] - 273.15, "C"
    print "Pressure:", solution[1] * 10, "hPa"
    print "Mixing Ratio:", solution[2] * 1000, "g/kg"
    print
    print "Wet Bulb Temperature:"
    solution = solveIteratively(wetBulbTemp, [ 268.15, 80., 2.13e-3 ])
    print "Temperature:", solution[0] - 273.15, "C"
    print "Pressure:", solution[1] * 10, "hPa"
    print "Mixing Ratio:", solution[2] * 1000, "g/kg"
    print
    print "Wet Bulb Potential Temperature:"
    solution = solveIteratively(wetBulbTemp, [ 285.7, 100., 2.13e-3 ], [ 280., 100., 2.13e-3 ])
    print "Temperature:", solution[0], "K"
    print "Pressure:", solution[1] * 10, "hPa"
    print "Mixing Ratio:", solution[2] * 1000, "g/kg"
    print
    print
    print "Mixed Saturation Temperature:"
    mixed_temperature = (303.15 + 275.15) / 2
    mixed_vapor_pressure = (vaporPressure(303.15, .9) + vaporPressure(275.15, .8)) / 2

    solution = solveIteratively(mixedSaturatedParcel, [ mixed_temperature, 100000., mixed_vapor_pressure ])
    print "Temperature:", solution[0], "K"
    print "Pressure:", solution[1] / 100, "hPa"
    print "Vapor Pressure:", solution[2] / 100, "hPa"
    return

if __name__ == "__main__":
    main()
