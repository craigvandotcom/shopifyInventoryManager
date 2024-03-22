import shopify
import numpy as np
import pandas as pd

def fetch_current_stock_levels(product_info):
    """
    Fetches the current stock levels for each product.

    Parameters:
    - product_info (dict): A dictionary containing product information, particularly InventoryItemIDs.

    Returns:
    - dict: A dictionary with product names as keys and current stock levels as values.
    """
    current_stock_levels = {}

    for product_name, details in product_info.items():
        inventory_item_id = details['InventoryItemID']
        inventory_levels = shopify.InventoryLevel.find(inventory_item_ids=str(inventory_item_id))

        if inventory_levels:
            total_quantity = sum([level.available for level in inventory_levels])
            current_stock_levels[product_name] = total_quantity
        else:
            current_stock_levels[product_name] = 0

    return current_stock_levels

def calculate_safety_stock_and_order_sizes(sales_data_df, product_info, forecast_results, settings, lead_time_days=67):
    """
    Calculates safety stock levels and order sizes based on sales data and forecasted demand.
    Parameters:
    - sales_data_df (pandas.DataFrame): DataFrame with historical sales data.
    - product_info (dict): Dictionary containing product information.
    - forecast_results_df (pd.DataFrame): Forecasted sales data in DataFrame.
    - settings (dict): A dictionary containing settings including 'shopify' configuration.
    - lead_time_days (int): Lead time in days for receiving stock, defaults to 67 if not specified.
    Returns:
    - tuple: Two dictionaries, one for safety stock levels and another for order size recommendations.
    """
    service_level_z = 1.65
    lead_time_days = settings['shopify'].get('lead_time_days', lead_time_days)
    lead_time_months = lead_time_days / 30  # Simple approximation

    # Transform DF 'month_year' to datetime format if present in the DataFrame
    if 'month_year' in sales_data_df.columns:
        sales_data_df['month_year'] = pd.to_datetime(sales_data_df['month_year'])

    monthly_sales_by_product = sales_data_df.groupby(['product_id', pd.Grouper(key='month_year', freq='M')])['quantity'].sum().reset_index()
    std_dev_by_product = monthly_sales_by_product.groupby('product_id')['quantity'].std().reset_index()

    # Map from product ID to names
    id_to_name_mapping = {details['ProductID']: name for name, details in product_info.items()}
    std_dev_by_product['product_name'] = std_dev_by_product['product_id'].map(id_to_name_mapping)

    safety_stock = {
        row['product_name']: service_level_z * row['quantity'] 
        for _, row in std_dev_by_product.iterrows() if pd.notnull(row['product_name'])
    }

    average_monthly_forecasted_demand = {}
    for product, details in product_info.items():
        product_id = details['ProductID']
        forecasted_product_data = forecast_results[forecast_results['product_id'] == product_id]
        average_forecast = np.mean(forecasted_product_data['yhat']) if not forecasted_product_data.empty else 0
        product_name = id_to_name_mapping.get(product_id, None)
        if product_name:
            average_monthly_forecasted_demand[product_name] = average_forecast

    forecasted_demand_lead_time = {
        product: demand * lead_time_months 
        for product, demand in average_monthly_forecasted_demand.items()
    }

    current_stock_levels = fetch_current_stock_levels(product_info)

    order_sizes = {}
    for product_name, current_stock in current_stock_levels.items():
        required_stock = 2 * forecasted_demand_lead_time.get(product_name, 0) + safety_stock.get(product_name, 0) - current_stock
        order_sizes[product_name] = max(0, required_stock)

    return safety_stock, order_sizes