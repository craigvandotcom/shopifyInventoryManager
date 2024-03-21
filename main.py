from shopify_api.sales import setup_shopify_for_sales, aggregate_sales_data, prepare_for_prophet
from shopify_api.inventory import calculate_safety_stock_and_order_sizes
from shopify_api.product_details import map_product_var, fetch_details
from forecasting.prophet_model import run_prophet_forecast
from forecasting.utilities import summarize_forecast_results
import toml
import os
import pandas as pd

def main():
    # Load settings from TOML file
    with open('configs/settings.toml', 'r') as toml_file:
        settings = toml.load(toml_file)

    # Setup Shopify API Session using updated function names and parameters
    shop_url = f"{os.environ['SHOP_NAME']}.myshopify.com"
    shopify_api_version = settings['shopify']['shopify_api_version']
    shopify_access_token = os.environ['SHOPIFY_ACCESS_TOKEN']
    setup_shopify_for_sales(shopify_api_version, shop_url, shopify_access_token)

    # Fetch and map product details
    product_mapping = map_product_var()
    product_info = fetch_details(product_mapping)

    prophet_file_path = 'prophet_ready_df.csv'

    aggregated_sales_data = None  # Initialize aggregated_sales_data before conditional statements

    # Check if the DataFrame has already been saved to avoid running expensive operations
    if os.path.exists(prophet_file_path):
        # Read the DataFrame from CSV
        prophet_ready_df = pd.read_csv(prophet_file_path)
    else:
        # Operations that can be skipped if DataFrame is saved
        from shopify_api.sales import fetch_sales_data_previous_months  # Import here to emphasize conditional import logic

        # Fetch sales data for previous months
        sales_data_df = fetch_sales_data_previous_months()

        # Aggregate sales data
        aggregated_sales_data = aggregate_sales_data(sales_data_df)

        # Prep
        prophet_ready_df = prepare_for_prophet(aggregated_sales_data)

        # Save the DataFrame to a CSV file
        prophet_ready_df.to_csv(prophet_file_path, index=False)

    # Ensure aggregated_sales_data is defined before using it
    if aggregated_sales_data is not None:
        # Run forecasting model
        forecast_results = run_prophet_forecast(prophet_ready_df)

        # Calculate safety stock levels and order sizes using the correct parameters now, including product information
        safety_stock, order_sizes = calculate_safety_stock_and_order_sizes(aggregated_sales_data, product_info, forecast_results, settings)

        # Summarize and display the forecast results
        summarize_forecast_results(forecast_results, safety_stock, order_sizes)

if __name__ == '__main__':
    main()