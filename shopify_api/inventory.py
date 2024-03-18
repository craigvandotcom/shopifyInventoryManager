import shopify
import numpy as np

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

def calculate_safety_stock_and_order_sizes(sales_data_df, product_info, forecast_results, lead_time_days=67):
    """
    Calculates safety stock levels and order sizes based on sales data and forecasted demand.

    Parameters:
    - sales_data_df (pandas.DataFrame): DataFrame with historical sales data.
    - product_info (dict): Dictionary containing product information.
    - forecast_results (dict): Forecasted sales data.
    - lead_time_days (int): Lead time in days for receiving stock.

    Returns:
    - tuple: Two dictionaries, one for safety stock levels and another for order size recommendations.
    """
    service_level_z = 1.65
    lead_time_months = lead_time_days / 30  # Simple approximation

    monthly_sales_by_product = sales_data_df.groupby(['product_id', pd.Grouper(key='date', freq='M')])['quantity'].sum().reset_index()
    std_dev_by_product = monthly_sales_by_product.groupby('product_id')['quantity'].std().reset_index()

    # Map from product ID to names
    id_to_name_mapping = {details['ProductID']: name for name, details in product_info.items()}
    std_dev_by_product['product_name'] = std_dev_by_product['product_id'].map(id_to_name_mapping)

    safety_stock = {
        row['product_name']: service_level_z * row['quantity'] 
        for _, row in std_dev_by_product.iterrows() if pd.notnull(row['product_name'])
    }

    average_monthly_forecasted_demand = {
        product: np.mean(list(sales.values())) 
        for product, sales in forecast_results.items()
    }

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