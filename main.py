from helpers import cost

# in numbers of ventilators produced per week
starting_output = 6000
max_output = 12000

# meaning a 10% growth rate
growth_rate = 1.1

# number of projected weeks
weeks = 12

# costs must be input in this format
weekly_costs = {
    "suppliers": {
        "unit": {
            # cost in dollars per ventilator unit produced
            "battery": 400,
            "controls": 1000,
            "monitor": 2000,
            "safety": 200,
        },
        "fixed": {
        },
        "labor": {
            "wage": 35,
            "hours": 40,
            "count": 20,
        },
    },

    "plants": {
        "unit": {
        },
        "fixed": {
            # fixed costs per week
            "factory": 1000,
            "machinery": 500,
        },
        "labor": {
            "wage": 35,
            "hours": 40,
            "count": 20,
        },
    },

    "warehouses": {
        # initially assuming 0 warehouse cost, but will have to count
        "unit": {
        },
        "fixed": {
        },
        "labor": {
        },
    },

    "transportation": {
        "freightRate": 35,              # dollars per mile
        "tripDistance": 1000,           # miles
        "unitVolume": 6,                # cubic feet
        "freightVolume": 3000,          # cubic feet
        "labor": {
            # freight rate already includes labor cost
        },
    },
}

# estimate costs with logistic growth model
cost(weekly_costs, starting_output, max_output, growth_rate, weeks)
