from shopify_api.sales import setup_shopify_for_sales, fetch_sales_data_previous_months, aggregate_sales_data
from shopify_api.inventory import calculate_safety_stock_and_order_sizes
from shopify_api.product_details import map_product_var, fetch_details
from forecasting.prophet_model import run_prophet_forecast
from forecasting.utilities import summarize_forecast_results
import toml
import os

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

    # Fetch sales data for previous months
    sales_data_df = fetch_sales_data_previous_months()

    # Aggregate sales data
    aggregated_sales_data = aggregate_sales_data(sales_data_df)

    # Run forecasting model
    forecast_results = run_prophet_forecast(aggregated_sales_data)

    # Calculate safety stock levels and order sizes using the correct parameters now, including product information
    safety_stock, order_sizes = calculate_safety_stock_and_order_sizes(aggregated_sales_data, product_info, forecast_results)

    # Summarize and display the forecast results
    summarize_forecast_results(forecast_results, safety_stock, order_sizes)

if __name__ == '__main__':
    main()