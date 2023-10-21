
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, sem, t

# Initialize more realistic parameters
annual_default_probabilities = np.array([0.01, 0.015, 0.02, 0.025, 0.03])  # Different default probabilities
notional_amounts = np.array([10, 20, 30, 40, 50])  # Different notional amounts in million

# Initialize an array to store the discounted payoff for each simulation
discounted_payoff_realistic = np.zeros(num_simulations)

# Monte Carlo simulation using Gaussian copula for realistic scenario
for i in range(num_simulations):
    # Step 1: Generate correlated standard normal variables
    standard_normals = np.random.multivariate_normal(np.zeros(num_cds), correlation_matrix)
    
    # Step 2: Transform standard normals to default times using the inverse survival function
    default_times = -np.log(1 - norm.cdf(standard_normals)) / annual_default_probabilities
    default_times.sort()
    
    # Step 3: Record the time of the N-th default
    n_th_default_time = default_times[N - 1]
    
    # Step 4: Discount the N-th default time back to present value
    # We consider the notional amounts to weight the payoff
    weighted_payoff = np.exp(-risk_free_rate * n_th_default_time) * notional_amounts[N - 1]
    discounted_payoff_realistic[i] = weighted_payoff

# Calculate the expected discounted payoff, which serves as the price of the CDO tranche
cdo_price_realistic = np.mean(discounted_payoff_realistic)

# Plot histogram of discounted payoffs for realistic scenario
plt.hist(discounted_payoff_realistic, bins=50, density=True, alpha=0.75, label=f'Discounted Payoff for {N}-th to Default (Realistic)')
plt.xlabel('Discounted Payoff')
plt.ylabel('Probability Density')
plt.title(f'Distribution of Discounted Payoff for {N}-th to Default CDO (Realistic Scenario)')
plt.legend()
plt.show()

cdo_price_realistic


# Monte Carlo simulation, plots, and calculations
# [The entire Python code for the project will go here]
