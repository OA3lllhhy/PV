import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

path = 'data/quarter_shade_non_illuminated_1.csv'
df = pd.read_csv(path)

def fit_func(x, k):
    return k*x

voltage = df['0A_Voltage']
current = df['0A_Current']

voltage = np.array(voltage)
current = np.array(current)

# Fitting the dark IV curve near the origin
min = -0.05
max = 0.05

mask = (voltage >= min) & (voltage <= max)
voltage_fit = voltage[mask]
current_fit = current[mask]

initial_guess = [1]
popt, pcov = curve_fit(fit_func, voltage_fit, current_fit, p0=initial_guess)
print("k = ", popt[0], "R_sh = ", - 1/popt[0])

plt.plot(voltage_fit, - fit_func(voltage_fit, *popt), 'o', label='fit')
plt.grid()
plt.legend()
plt.show()

