import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

from tsai.all import *

df = pd.read_csv("data/thu_chi_csv.csv", index_col=0)
print(f"Dữ liệu bao gồm {df.shape[0]} dòng và {df.shape[1]} cột:")

df = df.rename(columns={"Ngày":"date", "Giờ":"time", "Số tiền thu":"income","Số tiền chi":"spend", "Số dư":"balance","Hạng mục con":"small_category" , "Hạng mục cha": "big_category" })

# Convert the date column to a pandas datetime object
df['date'] = pd.to_datetime(df['date'])

# Sort the dataframe by date
df = df.sort_values(by='date').reset_index()
df.drop(["STT"], axis=1, inplace=True)
df.head()

# Extract year, month, and day columns
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df.head()

# Extract hour and minute columns
df['hour'] = df['time'].str.split(':', expand=True)[0]
df['minute'] = df['time'].str.split(':', expand=True)[1]

# Convert hour and minute columns to numeric type
df['hour'] = pd.to_numeric(df['hour'])
df['minute'] = pd.to_numeric(df['minute'])
df.head(5)

# Convert hour and minute columns to radians
df['hour_rad'] = 2 * np.pi * df['hour'] / 24
df['minute_rad'] = 2 * np.pi * df['minute'] / 60

# Convert hour and minute columns to sin and cos values
df['hour_sin'] = np.sin(df['hour_rad'])
df['hour_cos'] = np.cos(df['hour_rad'])
df['minute_sin'] = np.sin(df['minute_rad'])
df['minute_cos'] = np.cos(df['minute_rad'])
df.head()

money_cols = ["income","spend","balance"]
def money_div_1000(dataframe, cols = money_cols):
    for col in cols:
        dataframe[col] = dataframe[col]/1000
    return dataframe    
df = money_div_1000 (df)
df.head()

# Aggregate the dataframe by day and sum the money out column for each category
df_money_out = df.groupby(['date', 'big_category']).agg({'spend': ['sum']})
df_money_out.columns = ['spend_sum']
df_money_out = df_money_out.reset_index()
df_money_out.head(8)

df_money_out_a_day = df.groupby(['date']).agg({'spend': ['sum']})
df_money_out_a_day.columns = ['spend_in_a_day']

# Group the data by day, month, and year and sum the money spent
daily_totals = df.groupby('date').sum()
monthly_totals = df.resample('M', on='date').sum()
yearly_totals = df.resample('Y', on='date').sum()

# Create subplots for the different time periods
fig, axs = plt.subplots(2, 1, figsize=(20, 10))

# Plot the daily totals
axs[0].plot(daily_totals.index, daily_totals['spend'])
axs[0].set_title('Money spent per day')
axs[0].set_xlabel('Date')
axs[0].set_ylabel('Money spent')

# Plot the monthly totals
axs[1].plot(monthly_totals.index, monthly_totals['spend'])
axs[1].set_title('Money spent per month')
axs[1].set_xlabel('Month')
axs[1].set_ylabel('Money spent')

# Show the plot
plt.tight_layout()
plt.show()

# Create subplots for the different time periods
fig, axs = plt.subplots(2, 1, figsize=(20, 10))

# Plot the daily totals
axs[0].plot(daily_totals.index, daily_totals['income'])
axs[0].set_title('Income per day')
axs[0].set_xlabel('Date')
axs[0].set_ylabel('Income')

# Plot the monthly totals
axs[1].plot(monthly_totals.index, monthly_totals['income'])
axs[1].set_title('Income per month')
axs[1].set_xlabel('Month')
axs[1].set_ylabel('Income')

# Show the plot
plt.tight_layout()
plt.show()

df_money_out_category = df.groupby(['big_category'])['spend'].sum().reset_index()

fig, ax = plt.subplots(figsize=(15, 7))
# Create a bar chart to show the total money spent in each category and big category
sns.barplot(x="big_category", y="spend", data=df_money_out_category)

# Set the chart title and axis labels

plt.title("Total money spent by big category")
plt.xlabel("Category")
plt.ylabel("Money out")
ax.tick_params(axis='x', rotation=45)
