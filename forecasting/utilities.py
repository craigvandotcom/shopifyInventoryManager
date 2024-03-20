import pandas as pd
import matplotlib.pyplot as plt

def plot_forecast(forecast, historical_data=None):
    """
    Plots the forecasted data from Prophet model along with the historical data.

    Parameters:
    - forecast (pd.DataFrame): Forecast data from Prophet model.
    - historical_data (pd.DataFrame, optional): Historical data used for fitting the model.

    Returns:
    None. Displays a matplotlib plot.
    """
    # Plot the forecast
    plt.figure(figsize=(10, 6))
    plt.plot(forecast['ds'], forecast['yhat'], label='Forecast')

    # Plot the uncertainty intervals
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'],
                     color='gray', alpha=0.2, label='Uncertainty Interval')

    # Plot historical data if provided
    if historical_data is not None:
        plt.scatter(historical_data['ds'], historical_data['y'], color='black', s=20, 
                    label='Historical Data')

    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.title('Sales Forecast')
    plt.show()

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
        # Assuming we have a means of calculating immediate stock, for simplicity set to 0
        imminent_stock = 0
        # Example forecasted demand calculation; replace with real logic
        demand_lead_time = sum(forecast_results[product_name].values())/len(forecast_results[product_name])  
        # Aggregate existing and imminent stock for simplified example
        adjusted_current_stock = imminent_stock  

        data['Product Name'].append(product_name)
        data['Current + Imminent Stock'].append(imminent_stock)
        data['Safety Stock'].append(safety_stock.get(product_name, 0))
        data['Demand Lead Time'].append(demand_lead_time)
        data['Order Sizes'].append(order_sizes.get(product_name, 0))

        stock_pre_delivery = imminent_stock - demand_lead_time  # Simplified
        data['Stock Pre-Delivery'].append(stock_pre_delivery)

        stock_post_delivery = stock_pre_delivery + data['Order Sizes'][-1]  # Last added order size
        data['Stock Post-Delivery'].append(stock_pre_delivery)

        ideal_stock_at_next_delivery = safety_stock.get(product_name, 0) + demand_lead_time
        data['Ideal Stock at Next Delivery'].append(ideal_stock_at_next_delivery)

    # Construct DataFrame
    df_summary = pd.DataFrame(data)
    return df_summary