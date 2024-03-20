from shopify_api.my_shopify_client import setup_shopify_session
from shopify_api.inventory import fetch_current_stock_levels, calculate_safety_stock_and_order_sizes
from shopify_api.sales import fetch_sales_data_previous_months
from shopify_api.product_details import fetch_details
from forecasting.prophet_model import run_prophet_forecast
from forecasting.utilities import summarize_forecast_results
import os
import pandas as pd
import shopify

def main():
    # Load settings from TOML file
    with open('configs/settings.toml', 'r') as toml_file:
        settings = toml.load(toml_file)
    
    # Setup Shopify API Session
    shop_name = os.getenv('SHOP_NAME')
    shopify_api_version = '2024-01'
    shopify_api_key = os.getenv('SHOPIFY_API_KEY')
  
    setup_shopify_session(shop_name, shopify_api_version, shopify_api_key)

    # Fetch product details
    product_info = fetch_details(product_mapping)

    # Fetch current stock levels
    current_stock_levels = fetch_current_stock_levels(product_info)

    # Fetch sales data for previous months
    sales_data = fetch_sales_data_previous_months()

    # Calculate safety stock levels and order sizes
    safety_stock, order_sizes = calculate_safety_stock_and_order_sizes(sales_data, current_stock_levels)

    # Run forecasting model
    forecast_results = run_prophet_forecast(sales_data)

    # Summarize and display the forecast results
    summarize_forecast_results(forecast_results, safety_stock, order_sizes)

if __name__ == '__main__':
    main()