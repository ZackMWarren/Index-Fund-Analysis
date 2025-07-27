import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
from pathlib import Path

#when uploaded to streamlit cache data 
if not Path("^GSPC_cost.csv").exists():
    df = yf.download("^GSPC", start="1950-01-01", interval="1wk")
    df.columns = ['Close', 'High', 'Low', 'Open', 'Volume']

    df.to_csv("^GSPC_cost.csv")

'''
computes how much more or less you would make as a percent DCAing
or lump summing, iterates through the history of the s&p 500 until reaching
current week - DCA_weeks
'''
def Compare_DCA_LS(df, DCA_weeks, start_time, money):
    max_start = len(df) - DCA_weeks
    DCA_weekly_money = money/DCA_weeks
    results = []
    print(f"The starting year is {df["Date"][start_time]}")
    
    for i in range(start_time, max_start):
        LS_shares = money / df["Close"][i]
        DCA_shares = 0
        for j in range(i, i + DCA_weeks):
            DCA_shares = DCA_shares + (DCA_weekly_money / df["Close"][j])
        results.append({"Difference": ((LS_shares-DCA_shares)/LS_shares) * 100})

    results_df = pd.DataFrame(results).round(5)
    return(results_df)

#plots difference in return for DCAing a certain ammount of weeks
def Difference_Plot(df, weeks):
    plt.figure(figsize = (10,6))
    sns.histplot(data = df, stat = "percent", kde = True, color = "blue", alpha = 0.5)
    plt.axvline(df.median().item(), color = "blue", linestyle = "--", label = "median")
    plt.axvline(df.quantile(0.25).item(), color = "red", linestyle = "--", label = "25th percentile")
    plt.axvline(df.quantile(0.75).item(), color = "green", linestyle = "--", label = "75th percentile")
    
    plt.title(f"DCA vs Lump Sum ({weeks} weeks)")
    plt.xlabel(f"% Lump Sum beats DCA")
    plt.ylabel("Frequency %")
    plt.legend()
    plt.grid(alpha = 0.2)
    plt.show()

#plots the difference in expected returns at DCA lengths
def DCA_Time_Plot(df, start_week):
    df1=Compare_DCA_LS(df, 4, start_week, 10000)
    df2=Compare_DCA_LS(df, 12, start_week, 10000)
    df3=Compare_DCA_LS(df, 26, start_week, 10000)
    df4=Compare_DCA_LS(df, 52, start_week, 10000)
    df5=Compare_DCA_LS(df, 104, start_week, 10000)
    
    x_vals = [4,12,26,52,104]
    medians = [df.median().item() for df in [df1,df2,df3,df4,df5]]
    q1 = [df.quantile(0.25).item() for df in [df1,df2,df3,df4,df5]]
    q3 = [df.quantile(0.75).item() for df in [df1,df2,df3,df4,df5]]
    
    plt.figure(figsize=(10,6))
    ax = sns.barplot(x=x_vals, y=medians, color="blue")
    bar_centers = [bar.get_x() + bar.get_width()/2 for bar in ax.patches]
    plt.errorbar(x=bar_centers, y=medians, yerr=[np.array(medians) - np.array(q1),
        np.array(q3)-np.array(medians)], capsize=5, fmt="o", label = "1st and 3rd quartile")
    plt.xlabel("DCA Duration (Weeks)")
    plt.ylabel(f"Median % LS Beats DCA")
    plt.title("How Much Lump Sum Beats DCA by Weeks")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1)
    plt.show()

def Find_Start_Year(df, year):
    date_df = pd.to_datetime(df['Date'])
    date_df = date_df[date_df.dt.year == year]
    return date_df.index[0]
    
df = pd.read_csv("^GSPC_cost.csv")
df = df.round(2)
DCA_weeks = 54
start_week = Find_Start_Year(df, 1990)
results_df=Compare_DCA_LS(df, DCA_weeks, start_week, 10000)

DCA_Time_Plot(df, start_week)
Difference_Plot(results_df, DCA_weeks)