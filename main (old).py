!pip install ShopifyAPI
import shopify
import os

SHOPIFY-API-KEY = os.environ['SHOPIFY-API-KEY']
SHOP_NAME = my_secret = os.environ['SHOP_NAME']
API_VERSION = '2024-01'
LEAD_TIME = [60,55,75] # list of historical lead times (time between order placed and delivery of order)

# Calculate the average historical lead time, plus one extra week
AVG_LEAD_TIME = (sum(LEAD_TIME) / len(LEAD_TIME)) + 7

# Initialize Product Shopify Names
PRODUCT1_SHOPIFY_NAME = os.environ['PRODUCT1_SHOPIFY_NAME']
PRODUCT2_SHOPIFY_NAME = os.environ['PRODUCT2_SHOPIFY_NAME']
PRODUCT3_SHOPIFY_NAME = os.environ['PRODUCT3_SHOPIFY_NAME']
PRODUCT4_SHOPIFY_NAME = os.environ['PRODUCT4_SHOPIFY_NAME']
PRODUCT5_SHOPIFY_NAME = os.environ['PRODUCT5_SHOPIFY_NAME']
PRODUCT6_SHOPIFY_NAME = os.environ['PRODUCT6_SHOPIFY_NAME']
PRODUCT7_SHOPIFY_NAME = os.environ['PRODUCT7_SHOPIFY_NAME']
PRODUCT8_SHOPIFY_NAME = os.environ['PRODUCT8_SHOPIFY_NAME']

# Initialize Product Variable Names
PRODUCT1_VAR_NAME = os.environ['PRODUCT1_VAR_NAME']
PRODUCT2_VAR_NAME = os.environ['PRODUCT2_VAR_NAME']
PRODUCT3_VAR_NAME = os.environ['PRODUCT3_VAR_NAME']
PRODUCT4_VAR_NAME = os.environ['PRODUCT4_VAR_NAME']
PRODUCT5_VAR_NAME = os.environ['PRODUCT5_VAR_NAME']
PRODUCT6_VAR_NAME = os.environ['PRODUCT6_VAR_NAME']
PRODUCT7_VAR_NAME = os.environ['PRODUCT7_VAR_NAME']
PRODUCT8_VAR_NAME = os.environ['PRODUCT8_VAR_NAME']

# Set the API key and secret for the ShopifyAPI library (if necessary)
shopify.ShopifyResource.set_site(f"https://{SHOP_NAME}.myshopify.com/admin/api/{API_VERSION}")

# Since you're using a custom app and already have an access token,
# you don't need to generate a new session with API credentials.
# Instead, directly activate the session with the access token for your requests.
shopify.ShopifyResource.activate_session(shopify.Session(f"{SHOP_NAME}.myshopify.com", API_VERSION, SHOPIFY-API-KEY))


### CHECK SHOP NAME
# Test API call to fetch shop details
shop = shopify.Shop.current()
print("Shop Name: "+ shop.name)

### FETCH PRODUCT ID's
# list available product items
products = shopify.Product.find()
print("Product Details:")
for product in products:
    for variant in product.variants:
        print(f"Product Name: {product.title}, Product ID: {product.id}, Variant ID: {variant.id}, Inventory Item ID: {variant.inventory_item_id}, SKU: {variant.sku}")


### MATCH PRODUCT ID's
# Step 1: Create a mapping of product names to your variable naming format
product_mapping = {
    PRODUCT1_SHOPIFY_NAME : PRODUCT1_VAR_NAME,
    PRODUCT2_SHOPIFY_NAME : PRODUCT2_VAR_NAME,
    PRODUCT3_SHOPIFY_NAME : PRODUCT3_VAR_NAME,
    PRODUCT4_SHOPIFY_NAME : PRODUCT4_VAR_NAME,
    PRODUCT5_SHOPIFY_NAME : PRODUCT5_VAR_NAME,
    PRODUCT6_SHOPIFY_NAME : PRODUCT6_VAR_NAME,
    PRODUCT7_SHOPIFY_NAME : PRODUCT7_VAR_NAME,
    PRODUCT8_SHOPIFY_NAME : PRODUCT8_VAR_NAME
}

# Step 2: Fetch products and match them to your mapping
product_info = {}  # Dictionary to hold your variable names as keys and product/inventory IDs as values

products = shopify.Product.find()
for product in products:
    for key, value in product_mapping.items():
        if key.upper() in product.title.upper():  # Using upper() for case-insensitive comparison
            for variant in product.variants:
                # Assigning product ID and inventory item ID to your dictionary
                product_info[value] = {
                    "ProductID": product.id,
                    "VariantID": variant.id,
                    "InventoryItemID": variant.inventory_item_id
                }

# Step 3: Verify the assigned IDs (for demonstration, you can print or use them as needed)
for name, ids in product_info.items():
    print(f"{name}: {ids}")



### FETCH SALES_DATA PREVIOUS 12 MONTHS
from datetime import datetime
import shopify

# Assuming your Shopify API session is already set up

from datetime import datetime
from dateutil.relativedelta import relativedelta

# Get today's date
today = datetime.today()

# Calculate the first day of the current month
first_day_current_month = today.replace(day=1)

# Calculate the start date as the first day of the month, 12 months before the current month
start_date = first_day_current_month - relativedelta(months=12)

# Calculate the end date as the last day of the month before the current month
# By subtracting one day from the first day of the current month
end_date = first_day_current_month - relativedelta(days=1)

# Convert dates to ISO format strings
start_date_str = start_date.date().isoformat()
end_date_str = end_date.date().isoformat()

# Initialize a list to store sales data
sales_data = []

# Set initial params for the API call
params = {
    "created_at_min": start_date_str,
    "created_at_max": end_date_str,
    "status": "any",
    "limit": 250
}

while True:
    orders = shopify.Order.find(**params)
    for order in orders:
        for line_item in order.line_items:
            sales_data.append({
                'product_id': line_item.product_id,
                'quantity': line_item.quantity,
                'date': order.created_at
            })

    # Check if there's a next page of orders
    if orders.has_next_page():
        # Correctly access the 'next_page_url' property
        next_page_info = orders.next_page_url.split("page_info=")[-1] if orders.next_page_url else None
        if next_page_info:
            params = {"page_info": next_page_info}
        else:
            break
    else:
        break

# Now, `sales_data` contains historical sales data for all orders within the date range
print(sales_data)


### RUN PROPHET ML TO FORECAST NEXT 4 MONTHS

import pprint
from prophet import Prophet
import pandas as pd

# Initialize a dictionary to store forecast results
forecast_results = {}
sales_data_df = pd.DataFrame(sales_data)

# Ensure 'date' column is datetime type
sales_data_df['date'] = pd.to_datetime(sales_data_df['date'])

for product_name, details in product_info.items():
    product_id = details['ProductID']

    # Filter sales data for the current product
    df_product = sales_data_df[sales_data_df['product_id'] == product_id]

    # Aggregate sales data by month
    df_product_monthly = df_product.resample('M', on='date').quantity.sum().reset_index()

    if df_product_monthly.shape[0] >= 2:
        # Prepare DataFrame for Prophet
        df_forecast = df_product_monthly.rename(columns={'date': 'ds', 'quantity': 'y'})
        df_forecast['ds'] = df_forecast['ds'].dt.tz_localize(None)  # Make timezone-naive

        # Forecasting with Prophet
        model = Prophet()
        model.fit(df_forecast)
        future = model.make_future_dataframe(periods=4, freq='M')
        forecast = model.predict(future)

        # Store forecasted sales for the next 4 months
        forecasted_sales = forecast[['ds', 'yhat']].tail(4)

        # Convert forecasted sales DataFrame to a dictionary with date as key
        forecast_sales_dict = dict(zip(forecasted_sales.ds.dt.strftime('%Y-%m'), forecasted_sales.yhat))

        forecast_results[product_name] = forecast_sales_dict
    else:
        print(f"Insufficient data to forecast for product {product_name}")

# forecast_results now contains the forecasted monthly sales for the next 4 months, for each product
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(forecast_results)


### EXTRACT & STORE RELEVANT FORECAST NUMBERS

# After fitting the model, adjusted to show the future DataFrame for clarity
future = model.make_future_dataframe(periods=4, freq='M')
print("last 5 rows to include the starting point and 4 future periods")
print(future.tail(5))  # Show the last 5 rows to include the starting point and 4 future periods

forecast = model.predict(future)
print()
print("the forecasted values for the next 4 months")
print(forecast[['ds', 'yhat']].tail(4))  # Adjusted to show the forecasted values for the next 4 months


### PLOT PREVIOUS 12 + 4 FORECASTED SALES DATA

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Assuming sales_data_df contains historical sales data
# And forecast_results contains forecasted sales data for the next four months

# Convert historical sales data to a DataFrame with 'Month' and 'Sales' columns
historical_data = sales_data_df.groupby(['product_id', pd.Grouper(key='date', freq='M')])['quantity'].sum().reset_index()
historical_data['Month'] = historical_data['date'].dt.to_period('M')
historical_data.rename(columns={'quantity': 'Sales'}, inplace=True)

# Map product IDs to names
historical_data['Product Name'] = historical_data['product_id'].map({v['ProductID']: k for k, v in product_info.items()})

# Now prepare the forecasted data
forecasted_data = pd.DataFrame(columns=['Product Name', 'Month', 'Sales'])
for product_name, sales_dict in forecast_results.items():
    for month, sales in sales_dict.items():
        forecasted_data = forecasted_data.append({
            'Product Name': product_name,
            'Month': pd.Period(month, freq='M'),
            'Sales': sales
        }, ignore_index=True)

# Combine historical and forecasted sales data
combined_data = pd.concat([historical_data, forecasted_data], ignore_index=True)

# Ensure 'Month' is a datetime type for plotting
combined_data['Month'] = combined_data['Month'].dt.to_timestamp()

# Calculate total sales for each product and sort for legend ordering
total_sales_per_product = combined_data.groupby('Product Name')['Sales'].sum().sort_values(ascending=False)
sorted_product_names = total_sales_per_product.index.tolist()

# Plotting
plt.figure(figsize=(15, 8))
for product_name in sorted_product_names:
    product_data = combined_data[combined_data['Product Name'] == product_name]
    plt.plot(product_data['Month'], product_data['Sales'], marker='o', label=product_name)

today = datetime.today()
plt.axvline(x=today, color='k', linestyle='--', label='Today')
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gcf().autofmt_xdate()
plt.title('Sales Per Month: Past 12 Months and Next 4 Months Forecast')
plt.xlabel('Month')
plt.ylabel('Sales Quantity')
plt.legend(title='Total Sales: High to Low', loc='upper left')
plt.tight_layout()
plt.show()


### CHECK CURRENT STOCK LEVELS

import shopify

# Dictionary to hold the current stock levels for each product
current_stock_levels = {}

for product_name, details in product_info.items():
    inventory_item_id = details['InventoryItemID']

    # Fetch the inventory levels for the given inventory item ID
    # The inventory_item_id needs to be converted to a string as expected by the Shopify API
    inventory_levels = shopify.InventoryLevel.find(inventory_item_ids=str(inventory_item_id))

    # Assuming we only have one location or we sum up inventory across locations
    # If you have multiple locations, you'll need to aggregate quantities accordingly
    if inventory_levels:
        total_quantity = sum([level.available for level in inventory_levels])
        current_stock_levels[product_name] = total_quantity
    else:
        # If no levels are returned, set the quantity to 0 or handle as appropriate
        current_stock_levels[product_name] = 0

# Print out the current stock levels for each product
for product_name, quantity in current_stock_levels.items():
    print(f"{product_name}: {quantity}")


### CALCULATE & STORE CURRENT, SAFETY, FORECASTED DEMAND, ORDER SIZES, CALCULATED STOCK AT NEXT DELIVERY, IDEAL STOCK AT NEXT DELIVERY

import numpy as np
import pandas as pd

service_level_z = 1.65

# Ensure 'date' column is in datetime format
sales_data_df['date'] = pd.to_datetime(sales_data_df['date'])

# Aggregate sales data by product and month
monthly_sales_by_product = sales_data_df.groupby(['product_id', pd.Grouper(key='date', freq='M')])['quantity'].sum().reset_index()

# Calculate the standard deviation of monthly sales for each product
std_dev_by_product = monthly_sales_by_product.groupby('product_id')['quantity'].std().reset_index()

# Create a reverse mapping from product ID to product name
id_to_name_mapping = {details['ProductID']: name for name, details in product_info.items()}

# Use the reverse mapping to assign product names to the standard deviation dataframe
std_dev_by_product['product_name'] = std_dev_by_product['product_id'].map(id_to_name_mapping)

# Proceed with the safety stock calculation using the corrected product names
safety_stock = {row['product_name']: service_level_z * row['quantity'] for index, row in std_dev_by_product.iterrows() if pd.notnull(row['product_name'])}

# Calculate average monthly forecasted demand from forecast_results
average_monthly_forecasted_demand = {product: np.mean(list(sales.values())) for product, sales in forecast_results.items()}

# Define lead time in days and convert it to months (approximation)
LEAD_TIME_DAYS = 67
lead_time_months = LEAD_TIME_DAYS / 30  # Simple approximation

# Calculate forecasted demand for the lead time period instead of monthly
forecasted_demand_lead_time = {
    product: demand * lead_time_months for product, demand in average_monthly_forecasted_demand.items()
}

# Adjust the order size calculation to use forecasted demand for the lead time
order_sizes = {}
for product_name, current_stock in current_stock_levels.items():
    required_stock = 2*forecasted_demand_lead_time.get(product_name, 0) + safety_stock.get(product_name, 0) - current_stock
    order_sizes[product_name] = max(0, required_stock)  # Ensure non-negative order sizes

# Update the forecasted stock levels after the next order considering the lead time demand
forecasted_stock_post_order = {
    product: current_stock_levels[product] + order_sizes.get(product, 0) - forecasted_demand_lead_time.get(product, 0)
    for product in current_stock_levels
}

# safety check with simple calculation of ideal stock level @ time of delivery = safety stock plus forecasted demand
ideal_stock_at_delivery = {}
for product_name, stock in safety_stock.items():
  ideal_stock = stock + forecasted_demand_lead_time.get(product_name, 0)
  ideal_stock_at_delivery[product_name] = ideal_stock

# Calculate Ideal Stock at Next Delivery = Safety Stock + Forecasted Demand Over Lead Time
ideal_stock_at_delivery = {
    product_name: safety_stock[product_name] + forecasted_demand_lead_time.get(product_name, 0)
    for product_name in safety_stock.keys()
}

# Presenting the calculated data
print("Current Stock Levels (Units):")
for product_name, quantity in current_stock_levels.items():
    print(f"{product_name}: {quantity} units")

print("\nSafety Stock Levels (Units):")
for product, stock in safety_stock.items():
    print(f"{product}: {stock:.2f} units")

print("\nForecasted Demand Over Lead Time (Units):")
for product, demand in forecasted_demand_lead_time.items():
    print(f"{product}: {demand:.2f} units")

print("\nOrder Sizes (Units):")
for product, size in order_sizes.items():
    print(f"{product}: {size:.2f} units to reorder")

print("\nForecasted Stock Levels After Next Order Considering Lead Time Demand (Units):")
for product, stock in forecasted_stock_post_order.items():
    print(f"{product}: {max(0, stock):.2f} units")

print("\nIdeal Stock at Next Delivery (Units):")
for product, stock in ideal_stock_at_delivery.items():
    print(f"{product}: {max(0, stock):.0f} units")  # Use max to ensure non-negative values, round off to 0 decimal places


### ARRANGE DATA INTO DATAFRAME

import pandas as pd

# Assuming you have dictionaries for current_stock_levels, safety_stock, forecasted_demand_lead_time, order_sizes, forecasted_stock_post_order
# and ideal_stock_at_delivery, all keyed by product name

# Define the order of rows for the products
product_order = [
    PRODUCT2_VAR_NAME,
    PRODUCT1_VAR_NAME,
    PRODUCT4_VAR_NAME,
    PRODUCT3_VAR_NAME,
    PRODUCT6_VAR_NAME,
    PRODUCT5_VAR_NAME,
    PRODUCT7_VAR_NAME,
]

# Create a DataFrame
df = pd.DataFrame(index=product_order)

# Populate the DataFrame
df['Current Stock Levels'] = df.index.map(current_stock_levels.get)
df['Safety Stock'] = df.index.map(safety_stock.get)
df['Forecasted Demand Lead Time'] = df.index.map(forecasted_demand_lead_time.get)
df['Order Sizes'] = df.index.map(order_sizes.get)
df['Forecasted Stock Post Order'] = df.index.map(forecasted_stock_post_order.get)
df['Ideal Stock at Next Delivery'] = df.index.map(ideal_stock_at_delivery.get)

# Replace any NaN values with 0 or appropriate default
df.fillna(0, inplace=True)

# Round off all numbers to 0 decimal places
df = df.round(0).astype(int)

from google.colab import data_table
from vega_datasets import data

df

### UPDATED THE DATAFRAME TO FINAL VERSION

import pandas as pd

# Define dummy values for imminent stock
imminent_stock = {
    PRODUCT2_VAR_NAME: 500,
    PRODUCT1_VAR_NAME: 0,
    PRODUCT4_VAR_NAME: 500,
    PRODUCT3_VAR_NAME: 0,
    PRODUCT6_VAR_NAME: 0,
    PRODUCT5_VAR_NAME: 0,
    PRODUCT7_VAR_NAME: 500
}

# Update current_stock_levels to include imminent stock
adjusted_current_stock_levels = {product: current_stock_levels.get(product, 0) + imminent_stock.get(product, 0) for product in product_order}

# Recreate the DataFrame using adjusted current stock levels
df_adjusted = pd.DataFrame(index=product_order)

# Populate the DataFrame using adjusted current stock levels
df_adjusted['Current + Imminent Stock'] = df_adjusted.index.map(adjusted_current_stock_levels.get)
df_adjusted['Safety Stock'] = df_adjusted.index.map(safety_stock.get)
df_adjusted['Demand Lead Time'] = df_adjusted.index.map(forecasted_demand_lead_time.get)
df_adjusted['Order Sizes'] = df_adjusted.index.map(lambda product: max(0, 2*forecasted_demand_lead_time.get(product, 0) + safety_stock.get(product, 0) - adjusted_current_stock_levels[product]))
df_adjusted['Stock Pre-Delivery'] = df_adjusted.index.map(lambda product: adjusted_current_stock_levels[product] - forecasted_demand_lead_time.get(product, 0))
df_adjusted['Stock Post-Delivery'] = df_adjusted.index.map(lambda product: adjusted_current_stock_levels[product] + df_adjusted.loc[product, 'Order Sizes'] - forecasted_demand_lead_time.get(product, 0))
df_adjusted['Ideal Stock at Next Delivery'] = df_adjusted.index.map(lambda product: safety_stock.get(product, 0) + forecasted_demand_lead_time.get(product, 0))

# Replace any NaN values with 0 or appropriate default and round off all numbers to 0 decimal places
df_adjusted.fillna(0, inplace=True)
df_adjusted = df_adjusted.round(0).astype(int)

# Display the DataFrame
df_adjusted