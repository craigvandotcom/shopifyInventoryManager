from prophet import Prophet
import pandas as pd


def run_prophet_forecast(prophet_ready_df, periods=4, min_data_points=2):
    """
    Runs a sales forecast using Prophet for each unique product_id with sufficient data.
    
    Parameters:
    - prophet_ready_df (pd.DataFrame): Sales data formatted for Prophet with 'ds', 'y' columns, and includes 'product_id'.
    - periods (int): Number of periods to forecast into the future, with 'M' frequency for months.
    - min_data_points (int): Minimum number of data points required to run the forecast.
    
    Returns:
    - dict: A dictionary with product_id as keys and their forecasted data (pd.DataFrame) as values.
    """
    forecast_results = {}
    unique_products = prophet_ready_df['product_id'].unique()
    
    for product_id in unique_products:
        # Filter data for the current product_id
        product_data = prophet_ready_df[prophet_ready_df['product_id'] == product_id]
    
        # Check if there's enough data to forecast
        if len(product_data.dropna()) < min_data_points:
            print(f"Skipping product_id {product_id} due to insufficient data ({len(product_data)} points).")
            continue  # Skip this product and continue to the next
    
        # Initialize and fit the Prophet model for the current product
        model = Prophet(daily_seasonality=False, yearly_seasonality=True)
        model.fit(product_data[['ds', 'y']])  # Ensure only 'ds' and 'y' are used for fitting
    
        # Create a future dataframe for the specified number of periods
        future_dates = model.make_future_dataframe(periods=periods, freq='M')
    
        # Forecast the future sales for the current product
        forecast = model.predict(future_dates)
    
        # Append product_id to the forecast DataFrame for later reference
        forecast['product_id'] = product_id  # Ensuring each forecast DataFrame carries its product_id
    
        # Store the forecast results using product_id as the key
        forecast_results[product_id] = forecast
    
    return forecast_results



def summarize_forecast_results(forecast):
    """
    Summarizes Prophet's forecast results by extracting relevant columns.

    Parameters:
    - forecast (pd.DataFrame): Full forecast DataFrame returned by Prophet.

    Returns:
    - summary (pd.DataFrame): A summary DataFrame with relevant forecast details.
    """
    summary = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    return summary