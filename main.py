import pandas as pd
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
computes money at the end of the time frame if DCAing (weekly)
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
        end_share_cost = df["Close"][i + DCA_weeks - 1]
        results.append({"LS": LS_shares * end_share_cost, "DCA": DCA_shares * end_share_cost})

    results_df = pd.DataFrame(results).round(2)
    results_dict = {
        'means': 
            {'LS': (results_df["LS"].mean().round(2)),'DCA': (results_df["DCA"].mean().round(2))},
        'medians': 
            {'LS': (results_df["LS"].median().round(2)),'DCA': (results_df["DCA"].median().round(2))},
        'standard_deviations': 
            {'LS': (results_df["LS"].std().round(2)),'DCA': (results_df["DCA"].std().round(2))},
        'Q1': 
            {'LS': (results_df["LS"].quantile(0.25).round(2)),'DCA': (results_df["DCA"].quantile(0.25).round(2))},
        'Q3': 
            {'LS': (results_df["LS"].quantile(0.75).round(2)),'DCA': (results_df["DCA"].quantile(0.75).round(2))},
        'minimums': 
            {'LS': (results_df["LS"].min()),'DCA': (results_df["DCA"].min())},
        'maximums': 
            {'LS': (results_df["LS"].max()),'DCA': (results_df["DCA"].max())},
        'win_rates': 
            {'LS': ((results_df["LS"] > results_df["DCA"]).mean() * 100).round(2),'DCA': (100 - (results_df["LS"] > results_df["DCA"]).mean() * 100).round(2)}
    }
    
    return(results_df, results_dict)
 
def Overlay_Plot(df, dict):
    plt.figure(figsize=(10,6))
    sns.histplot(data = df["LS"], stat = "percent", kde = True, color = "blue", label = "Lump Sum", alpha = 0.5)
    sns.histplot(data = df["DCA"], stat = "percent", kde = True, color = "orange", label = "Dollar Cost Average", alpha = 0.5)
    
    plt.axvline(dict["Q1"]["LS"], color = "blue", linestyle = "--", label = "LS 25%")
    plt.axvline(dict["Q1"]["DCA"], color = "orange", linestyle = "--", label = "DCA 25%")
    plt.axvline(dict["Q3"]["LS"], color = "blue", linestyle = "-.", label = "LS 75%")
    plt.axvline(dict["Q3"]["DCA"], color = "orange", linestyle = "-.", label = "DCA 75%")
    
    plt.title("DCA vs Lump Sum Overlaid")
    plt.xlabel("$")
    plt.ylabel("Frequency %")
    plt.legend()
    plt.grid(alpha = 0.2)
    plt.show() 

df = pd.read_csv("^GSPC_cost.csv")
df = df.round(2)
DCA_weeks = 26
results_df, results_dict=Compare_DCA_LS(df, DCA_weeks, 2088, 10000)

Overlay_Plot(results_df,results_dict)




'''print(f"Weeks: {DCA_weeks}")
for category, metric in results_dict.items():
    print(f"Category: {category}")
    for strat, value in metric.items():
        print(f"    {strat}: {value}")
percent_diff = ((results_dict["means"]["LS"]-results_dict["means"]["DCA"])/results_dict["means"]["DCA"])*100
print(f"Lump summing returns {percent_diff}% more on average")'''