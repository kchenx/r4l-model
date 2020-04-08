# helpers.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math

# Computes cost for a segment with entries for `unit`, `fixed`, and `labor` costs
def segment_cost(costs, n):
    unit_cost = sum(costs["unit"].values()) * n

    fixed_cost = sum(costs["fixed"].values())

    if len(costs["labor"]) == 0:
        labor_cost = 0
    else:
        labor_cost = 1
        for cost in costs["labor"].values():
            labor_cost *= cost

    return unit_cost + fixed_cost + labor_cost


# Returns new number using logistic growth for starting `A`, max capacity `K`, growth rate `r`, and time period `t`
def logistic_growth(A, K, r, t):
    return A * K / (A + (K - A) * math.exp(-r * t))


# Computes cost with logistic growth model for `costs` in the format given at the bottom,
# for starting ventilator number `start_n`, max capacity ventilator number `max_n`, and
# growth rate `r` for `t` weeks.
def cost(costs, start_n, max_n, r, t):
    n = start_n
    # [[suppliers], [plants], [warehouses], [transportation]]
    data = [[], [], [], []]
    for i in range(t):
        # Increase output using logistic growth (does nothing for i = 0)
        n = logistic_growth(start_n, max_n, r, i)
        
        # Calculate cost by segment per week and add to data
        data[0].append(segment_cost(costs["suppliers"], n))
        data[1].append(segment_cost(costs["plants"], n))
        data[2].append(segment_cost(costs["warehouses"], n))
        trcosts = costs["transportation"]
        data[3].append(n * trcosts["freightRate"] * trcosts["tripDistance"] * 
                                      trcosts["unitVolume"] / trcosts["freightVolume"])

    # Divide data through by `multiple`
    multiple = 1000
    npdata = np.array(data) / multiple
    segments = ["Suppliers", "Plants", "Warehouses", "Transportation"]
    suppliers = npdata[0]
    plants = npdata[1]
    warehouses = npdata[2]
    transportation = npdata[3]
    ind = [t for t in range(1, t+1)]

    fig, axs = plt.subplots(2,1)

    # Plot graph
    graph = axs[0]
    graph.bar(ind, suppliers, width=0.6, label="Suppliers", color="green")
    graph.bar(ind, plants, width=0.6, label="Plants", color="blue", bottom=suppliers)
    graph.bar(ind, warehouses, width=0.6, label="Warehouses", color="orange", bottom=suppliers+plants)
    graph.bar(ind, transportation, width=0.6, label="Transportation", color="red", bottom=suppliers+plants+warehouses)

    graph.set_xticks(ind, range(t))
    graph.set_ylabel("Cost in $%ds" % multiple)
    graph.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    graph.set_xlabel("Week")
    graph.legend(loc="lower right")
    graph.set_title("Projected Cost per Week")

    # Add sums to data
    npdata = npdata.tolist()
    npdata = np.append(npdata,[np.sum(npdata, axis=0)], axis=0)
    col = np.array([np.sum(npdata, axis=1)])
    npdata = np.concatenate((npdata,col.T), axis=1)
    formatted_data = [['{:,.0f}'.format(j) for j in i] for i in npdata]

    # Plot table
    axs[1].axis("tight")
    axs[1].axis("off")
    rows = segments
    rows.append("Total")
    columns = ["Week %d" % x for x in range(1, t+1)]
    columns.append("Total")
    the_table = axs[1].table(cellText=formatted_data,
                             rowLabels=rows,
                             colLabels=columns,
                             loc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)
    the_table.scale(1.3, 1.3)

    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.3)

    plt.show()
