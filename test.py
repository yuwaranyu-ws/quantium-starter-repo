import pandas as pd
import os

# Build path relative to the script's location
base_dir = os.path.dirname(__file__)

files = [
    os.path.join(base_dir, 'data', 'daily_sales_data_0.csv'),
    os.path.join(base_dir, 'data', 'daily_sales_data_1.csv'),
    os.path.join(base_dir, 'data', 'daily_sales_data_2.csv'),
]

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Filter to Pink Morsels only
df = df[df['product'] == 'pink morsel']

# Calculate sales (strip $ from price, then multiply by quantity)
df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)
df['sales'] = df['quantity'] * df['price']

# Keep only required columns and save
df[['sales', 'date', 'region']].to_csv('output.csv', index=False)