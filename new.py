import numpy as np

# Example data
voltages = np.array([0, -5, 3.3, 2.8, 5.5, -3.2, 4.1])
currents = np.array([10, 20, 30, 40, 50, 60, 70])  # corresponding currents

# Step 1: Filter for positive voltages
positive_indices = voltages > 0  # creates a boolean array
positive_voltages = voltages[positive_indices]
corresponding_currents = currents[positive_indices]

# Step 2: Sort the positive voltages in ascending order
sorted_indices = np.argsort(positive_voltages)
sorted_voltages = positive_voltages[sorted_indices]
sorted_currents = corresponding_currents[sorted_indices]

print("Sorted Voltages:", sorted_voltages)
print("Sorted Currents:", sorted_currents)
