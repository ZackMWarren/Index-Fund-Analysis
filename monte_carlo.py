import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Helper function that returns a list of balances, summarizing the simulated market growth over years
def simulate_market_growth(start_balance, monthly_contribution, years, mu, sigma):
    months = years * 12
    balance = start_balance
    balances = []
    balances.append(balance)

    for _ in range(months):
        # Simulate monthly return
        monthly_return = np.random.normal(mu / 12, sigma / np.sqrt(12))
        balance = balance * (1 + monthly_return) + monthly_contribution
        balances.append(balance)

    return balances

# Function to run monte carlo simulations, which relies on simulate_market_growth
def run_monte_carlo_simulations(n, start_balance, monthly_contribution, years, mu = 0.07, sigma = 0.15):
    all_simulations = []
    
    for _ in range(n):
        simulation = simulate_market_growth(start_balance, monthly_contribution, years, mu, sigma)
        all_simulations.append(simulation)
    
    return pd.DataFrame(all_simulations)

# Function to plot the results of the monte carlo simulations
def plot_simulation_results(sim_df):
    plt.figure(figsize=(12,6))

    # Iterate through each simulation (rows) and plot the results
    for i in range(len(sim_df)):
        plt.plot(sim_df.columns, sim_df.iloc[i, :], color='skyblue', alpha=0.2)

    plt.plot(sim_df.columns, sim_df.median(axis=0), color='black', label='Median Outcome')
    plt.xlabel("Months")
    plt.ylabel("Portfolio Value ($)")
    plt.title("Monte Carlo Simulations of Portfolio Growth")
    plt.grid(True)
    plt.legend()
    plt.show()
