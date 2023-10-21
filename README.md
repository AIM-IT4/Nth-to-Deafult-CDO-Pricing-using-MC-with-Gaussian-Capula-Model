# N-th-to-Default CDO Pricing Project

This project aims to price an N-th-to-default Collateralized Debt Obligation (CDO) using Monte Carlo simulation with a Gaussian copula model. 

## Plots Included

1. Time Series of Defaults
2. Correlation Heatmap
3. Sensitivity Analysis
4. Convergence Plot
![image](https://github.com/AIM-IT4/pricing-of-an-N-th-to-default-Collateralized-Debt-Obligation-CDO-/assets/77675138/3fce7c09-fbd8-4c1a-8080-06eec07d4b2b)
![image](https://github.com/AIM-IT4/pricing-of-an-N-th-to-default-Collateralized-Debt-Obligation-CDO-/assets/77675138/ef3d903b-170f-4811-aaf5-722bd5530c3f)
![image](https://github.com/AIM-IT4/pricing-of-an-N-th-to-default-Collateralized-Debt-Obligation-CDO-/assets/77675138/8d1c0594-3281-413d-a786-05a77863de33)

## Calculations Included

1. Confidence Intervals for the estimated CDO price
2. Value at Risk (VaR) and Conditional VaR
3. Delta and Gamma

Confidence Intervals: The 95% confidence interval for the estimated CDO price is 
[
15.42
,
15.55
]
[15.42,15.55] million.

Value at Risk (VaR) and Conditional VaR: The VaR at a 5% significance level is approximately 9.33 million, and the Conditional VaR is about 7.53 million.

Delta and Gamma: The Delta is approximately 
−
10027.71
−10027.71 and the Gamma is approximately 
172915506.56
172915506.56. These values give us an idea of how sensitive the CDO price is to changes in the default probability. Note that these are simple finite difference approximations and might require further refinement for more accurate results.

## Requirements

- Python 3.x
- NumPy
- Matplotlib
- SciPy
- Seaborn

## How to Run

1. Clone the repository.
2. Run `cdo_pricing.py`.

## Author

Amit Kumar Jha
