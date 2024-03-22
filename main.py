from shopify_api.sales import setup_shopify_for_sales, aggregate_sales_data, prepare_for_prophet, fetch_sales_data_previous_months
from shopify_api.inventory import calculate_safety_stock_and_order_sizes
from shopify_api.product_details import map_product_var, fetch_details
from forecasting.prophet_model import run_prophet_forecast
from forecasting.utilities import summarize_forecast_results, plot_forecast
import toml
import os

# UPDATE IMMINENT STOCK
imminent_stock = {
    os.getenv('PRODUCT1_VAR_NAME'): 50,
    os.getenv('PRODUCT2_VAR_NAME'): 30,
    os.getenv('PRODUCT3_VAR_NAME'): 20,
    os.getenv('PRODUCT4_VAR_NAME'): 10,
    os.getenv('PRODUCT5_VAR_NAME'): 0,
    os.getenv('PRODUCT6_VAR_NAME'): 0,
    os.getenv('PRODUCT7_VAR_NAME'): 0,
    os.getenv('PRODUCT8_VAR_NAME'): 0
}

def main():
    # Load settings from TOML file
    with open('configs/settings.toml', 'r') as toml_file:
        settings = toml.load(toml_file)

    # Setup Shopify API Session using updated function names and parameters
    print("Setting up Shopify API session...")
    shop_url = f"{os.environ['SHOP_NAME']}.myshopify.com"
    shopify_api_version = settings['shopify']['shopify_api_version']
    shopify_access_token = os.environ['SHOPIFY_ACCESS_TOKEN']
    setup_shopify_for_sales(shopify_api_version, shop_url, shopify_access_token)

    # Fetch and map product details
    product_mapping = map_product_var()
    product_info = fetch_details(product_mapping)

    # Fetch sales data for previous months
    print("Fetching sales data for previous months...")
    sales_data_df = fetch_sales_data_previous_months()

    # Aggregate sales data
    print("Aggregating sales data...")
    aggregated_sales_data = aggregate_sales_data(sales_data_df) # 'date' to 'month_year'

    # Prep
    print("Preparing the DataFrame for Prophet model...")
    prophet_ready_df = prepare_for_prophet(aggregated_sales_data)

    # The forecasting and plotting logic now runs regardless of the DataFrame's source
    print("Running Prophet model...")
    forecast_results = run_prophet_forecast(prophet_ready_df)

    print("Visualizing the forecast data...")
    plot_forecast(forecast=forecast_results, historical_data=prepare_for_prophet(aggregated_sales_data))

    print("Calculating safety stock levels and order sizes...")
    safety_stock, order_sizes = calculate_safety_stock_and_order_sizes(aggregated_sales_data, product_info, forecast_results, settings)

    print("Summarizing and displaying the forecast results...")
    summary_df = summarize_forecast_results(forecast_results, safety_stock, order_sizes)

    print("Forecast plot saved as 'sales_forecast_plot.png'.")
    print("Forecast summary results saved in 'forecast_summary_results.csv'.")

if __name__ == '__main__':
    main()