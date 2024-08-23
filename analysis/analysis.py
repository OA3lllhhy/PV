import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy.optimize import minimize_scalar
from scipy.optimize import fsolve

path = 'data/quarter_shade_illuminated_1.csv'
dark = 'data/quarter_shade_non_illuminated_1.csv'
df = pd.read_csv(path)
df_dark = pd.read_csv(dark)

voltage = df['0A_Voltage']
current = df['0A_Current']
dark_voltage = df_dark['0A_Voltage']
dark_current = df_dark['0A_Current']

voltage = np.array(voltage)
current = np.array(current)
dark_voltage = np.array(dark_voltage)
dark_current = np.array(dark_current)
power = voltage*current

def fit_func(x, a, b, c):
    return a - b * np.exp(c * x)

# Extract the data in the interval [0, 0.6]
min = 0
max = 0.6
mask = (voltage >= min) & (voltage <= max)
voltage_fit = voltage[mask]
current_fit = current[mask]

# Fit the IV curve
initial_guess = [0.1, 2e-11, 38]
popt, pcov = curve_fit(fit_func, voltage_fit, -current_fit, p0=initial_guess)
print("a = ", popt[0], "b = ", popt[1], "c = ", popt[2])

# calculate the R^2 value
residuals = -current_fit - fit_func(voltage_fit, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((current_fit - np.mean(current_fit))**2)
r_squared = 1 - (ss_res / ss_tot)
print("R^2 = ", r_squared)

x = np.linspace(0, 0.7, 100)

# finding V_oc, I_sc, V_mp and I_mp (to shade the region on the graph)
def negative_PV(x):
    return - fit_func(x, *popt) * x

def IV(x):
    return fit_func(x, *popt)
    
I_sc = fit_func(0, *popt)
V_op = fsolve(IV, 0.55)

print("V_op: ", V_op[0], "I_sc: ", I_sc, )

result = minimize_scalar(negative_PV, bounds=(0,0.6))
V_mp = result.x
I_mp = fit_func(V_mp, *popt) * V_mp
print("V_mp: ", V_mp, "I_mp: ", I_mp)

# calculate the fill factor
ff = (V_mp * I_mp) / (I_sc * V_op[0])
print("Fill factor: ", ff)

# Plotting IV and PV curves on the same graph
fig, ax = plt.subplots()
ax.semilogx(voltage, -current, label='IV curve',)
ax.semilogx(voltage, -current * voltage, label='PV curve')
#ax.plot(x, fit_func(x, *popt),color ='orange', label='Fitted IV curve')
#ax.plot(x, fit_func(x, *popt) * x, color ='blue', label='Fitted PV curve') 
ax.set_xlabel('Voltage (V)')
ax.set_ylabel('Current (A)')
ax.set_title('IV Curve')
ax.hlines(0, 0, 0.7, colors='black')
ax.set_xlim(0, 0.7)
ax.set_ylim(-0.05, 0.15)
ax.grid()
ax.legend()
plt.show()
