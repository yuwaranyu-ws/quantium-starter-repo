import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

# Load all three CSV files
df1 = pd.read_csv('data/daily_sales_data_0.csv')
df2 = pd.read_csv('data/daily_sales_data_1.csv')
df3 = pd.read_csv('data/daily_sales_data_2.csv')

# Combine all data
df = pd.concat([df1, df2, df3], ignore_index=True)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Filter for Pink Morsel product only
pink_morsel_df = df[df['product'] == 'pink morsel'].copy()

# Clean price column (remove $ sign) and convert to float
pink_morsel_df['price'] = pink_morsel_df['price'].str.replace('$', '').astype(float)

# Calculate daily sales (price * quantity)
pink_morsel_df['sales'] = pink_morsel_df['price'] * pink_morsel_df['quantity']

# Group by date and sum sales across all regions
daily_sales = pink_morsel_df.groupby('date')['sales'].sum().reset_index()

# Sort by date
daily_sales = daily_sales.sort_values('date')

# Initialize Dash app
app = dash.Dash(__name__)

# Define the price increase date
price_increase_date = datetime(2021, 1, 15)

# Create the layout
app.layout = html.Div([
    html.H1(
        "Soul Foods Sales Dashboard - Pink Morsel Analysis",
        style={
            'textAlign': 'center',
            'color': '#2c3e50',
            'marginBottom': '30px',
            'fontFamily': 'Arial, sans-serif'
        }
    ),

    html.Div([
        dcc.Graph(
            id='sales-chart',
            figure={
                'data': [
                    go.Scatter(
                        x=daily_sales['date'],
                        y=daily_sales['sales'],
                        mode='lines',
                        name='Daily Sales',
                        line=dict(color='#3498db', width=2),
                        hovertemplate='Date: %{x}<br>Sales: $%{y:.2f}<extra></extra>'
                    )
                ],
                'layout': go.Layout(
                    title='Pink Morsel Daily Sales Over Time',
                    xaxis={
                        'title': 'Date',
                        'showgrid': True,
                        'gridcolor': '#ecf0f1'
                    },
                    yaxis={
                        'title': 'Total Daily Sales ($)',
                        'showgrid': True,
                        'gridcolor': '#ecf0f1'
                    },
                    hovermode='x unified',
                    plot_bgcolor='white',
                    shapes=[
                        # Add vertical line for price increase date
                        dict(
                            type='line',
                            x0=price_increase_date,
                            x1=price_increase_date,
                            y0=0,
                            y1=1,
                            yref='paper',
                            line=dict(
                                color='red',
                                width=2,
                                dash='dash'
                            )
                        )
                    ],
                    annotations=[
                        dict(
                            x=price_increase_date,
                            y=1,
                            yref='paper',
                            text='Price Increase<br>Jan 15, 2021',
                            showarrow=True,
                            arrowhead=2,
                            arrowcolor='red',
                            ax=50,
                            ay=-50,
                            font=dict(color='red', size=12)
                        )
                    ]
                )
            }
        )
    ], style={'padding': '20px'})
])

# Calculate and print summary statistics
before_increase = daily_sales[daily_sales['date'] < price_increase_date]['sales']
after_increase = daily_sales[daily_sales['date'] >= price_increase_date]['sales']

print("\n" + "=" * 60)
print("PINK MORSEL SALES ANALYSIS")
print("=" * 60)
print(f"\nAverage Daily Sales BEFORE Jan 15, 2021: ${before_increase.mean():,.2f}")
print(f"Average Daily Sales AFTER Jan 15, 2021:  ${after_increase.mean():,.2f}")
print(f"\nDifference: ${after_increase.mean() - before_increase.mean():,.2f}")
print(f"Percentage Change: {((after_increase.mean() - before_increase.mean()) / before_increase.mean() * 100):.2f}%")
print("\n" + "=" * 60 + "\n")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)