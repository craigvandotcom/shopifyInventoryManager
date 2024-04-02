import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from datetime import datetime
import pandas as pd

def plot_forecast(forecast_results, historical_data=None, product_mapping=None):
    """
    Plots the forecasted data from the Prophet model along with the historical data, enhanced with product names.
  
    Parameters:
    - forecast_results (dict): Dictionary with product_id as keys and forecasted data (pd.DataFrame) as values.
    - historical_data (pd.DataFrame, optional): Historical data used for fitting the model.
    - product_mapping (dict, optional): Mapping from product variable names to product names.
  
    Returns:
    None. Displays a matplotlib plot.
    """
    plt.figure(figsize=(15, 8))
  
    # Ensure 'ds' in historical_data is in datetime format if historical_data is provided
    if historical_data is not None and 'product_id' in historical_data.columns:
        historical_data['ds'] = pd.to_datetime(historical_data['ds'])
  
    for product_id, forecast in forecast_results.items():
        # Map product_id to product name using product_mapping if available
        product_name = product_mapping.get(product_id, f"Product {product_id}") if product_mapping else str(product_id)
  
        forecast['ds'] = pd.to_datetime(forecast['ds'])
        plt.plot(forecast['ds'], forecast['yhat'], marker='o', label=product_name)
  
        # Plot historical data if provided and applicable
        if historical_data is not None:
            product_historical_data = historical_data[historical_data['product_id'] == product_id].copy()
            product_historical_data.loc[:, 'ds'] = pd.to_datetime(product_historical_data['ds'])
            plt.scatter(product_historical_data['ds'], product_historical_data['y'], color='black', s=20, label=f"History {product_name}")
  
    # Common plot adjustments
    today = datetime.today()
    plt.axvline(x=today, color='k', linestyle='--', label='Today')
  
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gcf().autofmt_xdate()  # Auto-format the dates for readability
  
    plt.title('Product Sales Forecast')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend(title='Product Names', loc='upper left')
    plt.tight_layout()
  
    # Save the plot as an image
    plt.savefig('sales_forecast_plot.png', bbox_inches='tight')
    print("Forecast plot saved as 'sales_forecast_plot.png'.")


def summarize_forecast_results(forecast_results, safety_stock, order_sizes):
    """
    Transforms forecast data along with safety stock and order sizes into a structured DataFrame.

    Parameters:
    - forecast_results (dict): Forecast results keyed by product name.
    - safety_stock (dict): Safety stock levels keyed by product name.
    - order_sizes (dict): Order sizes keyed by product name.

    Returns:
    - pd.DataFrame: A DataFrame similar to df_adjusted in 'main (old).py', combining forecast information
      with safety stock and order sizes for each product name.
    """
    product_order = list(forecast_results.keys())  # Ensure consistent order

    # Initialize data for DataFrame construction
    data = {
        'Product Name': [],
        'Current + Imminent Stock': [],
        'Safety Stock': [],
        'Demand Lead Time': [],
        'Order Sizes': [],
        'Stock Pre-Delivery': [],
        'Stock Post-Delivery': [],
        'Ideal Stock at Next Delivery': []
    }

    # Assuming necessary data received correctly; otherwise, ensure data existence and error handling
    for product_name in product_order:
  
        # Example forecasted demand calculation; replace with real logic
        demand_lead_time = forecast_results['yhat'].sum() / len(forecast_results['yhat'])

        data['Product Name'].append(product_name)
        data['Current + Imminent Stock'].append(imminent_stock)
        data['Safety Stock'].append(safety_stock.get(product_name, 0))
        data['Demand Lead Time'].append(demand_lead_time)
        data['Order Sizes'].append(order_sizes.get(product_name, 0))

        stock_pre_delivery = imminent_stock - demand_lead_time  # Simplified
        data['Stock Pre-Delivery'].append(stock_pre_delivery)

        stock_post_delivery = stock_pre_delivery + data['Order Sizes'][-1]  # Last added order size
        data['Stock Post-Delivery'].append(stock_post_delivery)

        ideal_stock_at_next_delivery = safety_stock.get(product_name, 0) + demand_lead_time
        data['Ideal Stock at Next Delivery'].append(ideal_stock_at_next_delivery)

    # Construct DataFrame
    df_summary = pd.DataFrame(data)
    return df_summary