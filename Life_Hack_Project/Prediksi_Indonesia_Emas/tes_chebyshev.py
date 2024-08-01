
import numpy as np
import math
import matplotlib.pyplot as plt
from numpy.polynomial.chebyshev import Chebyshev

# Define the function to be approximated
def f(x):
    #return np.exp(x / 10)
    return np.sin(x) * np.exp(x / 10) 
    #return 10*np.sin(x-10)/(x-10)


# Define the interval
a, b = 0, 30

# Map interval to [-1, 1]
def map_to_chebyshev(x):
    return (2 * x - (b + a)) / (b - a)

# Number of Chebyshev nodes
n = 100

# Chebyshev nodes
x_k = np.cos((2 * np.arange(n + 1) + 1) * np.pi / (2 * (n + 1)))

# Map nodes back to original interval
x_k_mapped = 0.5 * (a + b) + 0.5 * (b - a) * x_k

# Evaluate function at the nodes
y_k = f(x_k_mapped)

# Fit Chebyshev polynomial
chebyshev_poly = Chebyshev.fit(x_k_mapped, y_k, n)
print(chebyshev_poly)

# Evaluate the polynomial
x_vals = np.linspace(a, b, 100)
y_approx = chebyshev_poly(x_vals)

x_ori = np.linspace(a, 100, 100)

# Extrapolate beyond the interval [-10, 10]
x_extrap = np.linspace(10, 15, 10)
y_extrap = chebyshev_poly(x_extrap)

# Plot the function and its approximation
plt.plot(x_ori, f(x_ori), label='Original function')
#plt.plot(x_vals, y_approx, label='Chebyshev approximation')
plt.scatter(x_k_mapped, y_k, color='red', label='Chebyshev nodes')

# Plot the extrapolation
plt.scatter(x_extrap, y_extrap, label='Chebyshev extrapolation')
plt.legend()
plt.show()

