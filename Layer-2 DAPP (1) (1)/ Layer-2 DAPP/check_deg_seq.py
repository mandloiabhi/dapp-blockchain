import numpy as np
import matplotlib.pyplot as plt

def power_law(x, alpha, xmin):
    return (x / xmin) ** (-alpha)

def check_power_law_degree_sequence(degree_sequence):
    # Sort the degree sequence in decreasing order
    degree_sequence = sorted(degree_sequence, reverse=True)
    
    # Calculate the minimum and maximum degree in the sequence
    kmin = min(degree_sequence)
    kmax = max(degree_sequence)
    
    # Generate a range of x values between the minimum and maximum degree
    x = np.arange(kmin, kmax + 1)
    
    # Calculate the theoretical degree distribution using the power law function
    alpha = 1 + len(degree_sequence) / sum(np.log(degree_sequence / kmin))
    y = power_law(x, alpha, kmin)
    
    # Calculate the actual degree distribution
    degree_counts = np.bincount(degree_sequence)
    x_actual = np.nonzero(degree_counts)[0]
    y_actual = degree_counts[x_actual] / len(degree_sequence)
    
    # Plot both the theoretical and actual degree distributions on a log-log scale
    plt.loglog(x, y, label='Theoretical')
    plt.loglog(x_actual, y_actual, '.', label='Actual')
    plt.legend()
    plt.show()
    
    # Check if the distributions form a straight line on the log-log scale
    if np.allclose(np.log(y_actual), np.log(y), rtol=1e-3, atol=1e-3):
        print('The degree sequence follows a power law degree distribution.')
    else:
        print('The degree sequence does not follow a power law degree distribution.')
