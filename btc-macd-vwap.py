import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_total_start_and_end_time(total_period):
    """
    Returns the start and end time for the total period.

    Args:
        total_period (str): Total period in a format like '1y', '6mo', etc.

    Returns:
        tuple: Start and end time as datetime objects.
    """
    end_time = pd.Timestamp.now()
    start_time = end_time - pd.Timedelta(total_period)
    return start_time, end_time
    
def calculate_vpoc200(df):
  """
  Calculates the 200-day rolling average of the Volume Point of Control (VPOC).

  Args:
      df (pd.DataFrame): DataFrame containing 'Date' and 'VPOC' columns.

  Returns:
      pd.DataFrame: DataFrame with an added 'VPOC200' column.
  """
  df['VPOC200'] = df['VPOC'].rolling(window=200).mean()
  return df

def calculate_vpoc50(df):
  df['VPOC50'] = df['VPOC'].rolling(window=50).mean()
  return df


def plot_vpoc_trend(df, start_date, end_date):

    vpoc_list = []
    date_list = []


    for index, row in df.iterrows():
        # Create price bins for the day's range
        price_bins = np.linspace(row['Low'], row['High'], num=50)
        # Calculate the volume per bin
        volume_per_bin = row['Volume'] / (len(price_bins) - 1) if len(price_bins) > 1 else row['Volume']
        # Find the bin with the maximum volume (this is a simplified approach)
        # In a real VPOC calculation, volume is distributed based on trades within each bin
        # Here, we're just taking the midpoint of the range as a proxy for VPOC for simplicity
        vpoc = (row['Low'] + row['High']) / 2


        vpoc_list.append(vpoc)
        date_list.append(index) # Use index for date


    # Create DataFrame for plotting
    vpoc_df = pd.DataFrame({
        'Date': date_list,
        'VPOC': vpoc_list,
    })

    # calculate vpoc 200
    vpoc_df = calculate_vpoc200(vpoc_df)
    # calculate vpoc 50
    vpoc_df = calculate_vpoc50(vpoc_df)



    return vpoc_df # Return the DataFrame with VPOC data
    
    import datetime

start_time, end_time = get_total_start_and_end_time(TOTAL_PERIOD)
ticker = "BTC-USD"

# Download OHLCV data
df5 = yf.download(ticker, start=start_time, end=end_time, interval='1d')
df5.dropna(inplace=True)

# Get the VPOC data and plot the trendlines using matplotlib within the function
# Refer to the plot_vpoc_trend function in cell VtnJWfG9bC1h for plotting details.
vpoc_data = plot_vpoc_trend(df5, start_time, end_time)

# Display the DataFrame with VPOC
# display(vpoc_data.head())
# Plot trend line orange for 200, blue for 50 using matplotlib
# plt.figure(figsize=(12, 6))
# fig, ax1 = plt.subplots()
fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(10, 3),dpi=100)

# ax1.plot(vpoc_df['Date'], vpoc_df['VPOC50'], label='VPOC 50-day MA', color='blue')

ax1.plot(vpoc_data['Date'], vpoc_data['VPOC200'], label='VPOC 200-day MA', color='orange')
ax2 = ax1.twinx()
ax2.plot(vpoc_data['Date'], vpoc_data['VPOC50'], label='VPOC 50-day MA', color='blue')


plt.title(f'VPOC Trend Line for {ticker}')
plt.xlabel('Date')
plt.ylabel('Price Level (VPOC)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# The plotting logic is within the plot_vpoc_trend function.
# To plot two trendlines with matplotlib, the function uses:
# plt.plot(vpoc_df['Date'], vpoc_df['VPOC50'], label='VPOC 50-day MA', color='blue')
# plt.plot(vpoc_df['Date'], vpoc_df['VPOC200'], label='VPOC 200-day MA', color='orange')
# followed by plt.show()