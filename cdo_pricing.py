
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


import seaborn as sns
from scipy.stats import sem, t

# Initialize variables for additional analyses
num_simulations_list = [1000, 2500, 5000, 7500, 10000]
cdo_prices_convergence = []

# Initialize array to store default times for Time Series plot
default_times_series = np.zeros((num_simulations, num_cds))

# Initialize array to store discounted payoffs for different simulations (Convergence and VaR)
payoffs_for_convergence = np.zeros((max(num_simulations_list),))

# Monte Carlo simulation with Gaussian copula for realistic scenario
for num_simulations in num_simulations_list:
    discounted_payoff_temp = np.zeros(num_simulations)
    for i in range(num_simulations):
        # Generate correlated standard normal variables
        standard_normals = np.random.multivariate_normal(np.zeros(num_cds), correlation_matrix)
        
        # Transform standard normals to default times using the inverse survival function
        default_times = -np.log(1 - norm.cdf(standard_normals)) / annual_default_probabilities
        default_times.sort()
        
        # Store default times for Time Series plot
        if num_simulations == max(num_simulations_list):
            default_times_series[i, :] = default_times
        
        # Record the time of the N-th default
        n_th_default_time = default_times[N - 1]
        
        # Discount the N-th default time back to present value considering notional amounts
        weighted_payoff = np.exp(-risk_free_rate * n_th_default_time) * notional_amounts[N - 1]
        discounted_payoff_temp[i] = weighted_payoff
        
        # Store payoffs for Convergence and VaR analysis
        if num_simulations == max(num_simulations_list):
            payoffs_for_convergence[i] = weighted_payoff

    # Calculate CDO price and store for Convergence plot
    cdo_price_temp = np.mean(discounted_payoff_temp)
    cdo_prices_convergence.append(cdo_price_temp)

# Time Series of Defaults plot
plt.figure(figsize=(10, 6))
plt.plot(default_times_series[:100, :])  # Plotting first 100 simulations for visibility
plt.title('Time Series of Defaults')
plt.xlabel('Simulation')
plt.ylabel('Default Time (Years)')
plt.legend([f'Entity {i+1}' for i in range(num_cds)])
plt.show()

# Correlation Heatmap
correlation_heatmap_data = np.corrcoef(default_times_series, rowvar=False)
sns.heatmap(correlation_heatmap_data, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap of Default Times')
plt.show()

# Sensitivity Analysis: How CDO price changes with variations in default probability, correlation, and risk-free rate
sensitivity_params = {
    'Default Probability': [0.01, 0.015, 0.02, 0.025, 0.03],
    'Correlation': [0.1, 0.2, 0.3, 0.4, 0.5],
    'Risk-Free Rate': [0.005, 0.01, 0.015, 0.02, 0.025]
}
sensitivity_results = {'Default Probability': [], 'Correlation': [], 'Risk-Free Rate': []}

for param, values in sensitivity_params.items():
    for value in values:
        discounted_payoff_temp = np.zeros(num_simulations)
        for i in range(num_simulations):
            if param == 'Default Probability':
                default_times = -np.log(1 - norm.cdf(np.random.multivariate_normal(np.zeros(num_cds), correlation_matrix))) / value
            elif param == 'Correlation':
                temp_corr_matrix = np.full((num_cds, num_cds), value)
                np.fill_diagonal(temp_corr_matrix, 1)
                default_times = -np.log(1 - norm.cdf(np.random.multivariate_normal(np.zeros(num_cds), temp_corr_matrix))) / annual_default_probabilities[0]
            elif param == 'Risk-Free Rate':
                default_times = -np.log(1 - norm.cdf(np.random.multivariate_normal(np.zeros(num_cds), correlation_matrix))) / annual_default_probabilities[0]
            
            default_times.sort()
            n_th_default_time = default_times[N - 1]
            weighted_payoff = np.exp(-value * n_th_default_time) if param == 'Risk-Free Rate' else np.exp(-risk_free_rate * n_th_default_time) * notional_amounts[N - 1]
            discounted_payoff_temp[i] = weighted_payoff
        
        sensitivity_results[param].append(np.mean(discounted_payoff_temp))

# Plotting Sensitivity Analysis
for param, values in sensitivity_params.items():
    plt.plot(values, sensitivity_results[param], marker='o')
    plt.title(f'Sensitivity of CDO Price to {param}')
    plt.xlabel(param)
    plt.ylabel('CDO Price')
    plt.show()

# Convergence Plot
plt.plot(num_simulations_list, cdo_prices_convergence, marker='o')
plt.title('Convergence of CDO Price')
plt.xlabel('Number of Simulations')
plt.ylabel('CDO Price')
plt.show()

# Confidence Intervals for CDO Price
confidence_level = 0.95
degrees_freedom = num_simulations - 1
sample_mean = np.mean(payoffs_for_convergence)
sample_standard_error = sem(payoffs_for_convergence)
confidence_interval = t.interval(confidence_level, degrees_freedom, sample_mean, sample_standard_error)

# Value at Risk (VaR) and Conditional VaR
alpha = 0.05  # Significance level
VaR = np.percentile(payoffs_for_convergence, 100 * alpha)
CVaR = payoffs_for_convergence[payoffs_for_convergence <= VaR].mean()

# Delta and Gamma (Using a simple finite difference approximation)
delta_default_probability = 0.001  # Small change in default probability
cdo_price_up = np.mean(-np.log(1 - norm.cdf(np.random.multivariate_normal(np.zeros(num_cds), correlation_matrix, num_simulations))) / (annual_default_probabilities[0] + delta_default_probability))
cdo_price_down = np.mean(-np.log(1 - norm.cdf(np.random.multivariate_normal(np.zeros(num_cds), correlation_matrix, num_simulations))) / (annual_default_probabilities[0] - delta_default_probability))
Delta = (cdo_price_up - cdo_price_down) / (2 * delta_default_probability)
Gamma = (cdo_price_up - 2 * cdo_price_realistic + cdo_price_down) / (delta_default_probability ** 2)

confidence_interval, VaR, CVaR, Delta, Gamma

