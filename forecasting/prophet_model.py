from prophet import Prophet
import pandas as pd


def format_sales_data_for_prophet(sales_data):
    """
    Formats sales data into the structure expected by Prophet: a DataFrame with 'ds' and 'y' columns.

    Parameters:
    - sales_data (pd.DataFrame): Original sales data with 'date' and 'quantity' columns.

    Returns:
    - pd.DataFrame: Formatted DataFrame with 'ds' and 'y' columns.
    """
    formatted_data = sales_data.rename(columns={'date': 'ds', 'quantity': 'y'})
    # Make sure 'ds' is datetime type
    formatted_data['ds'] = pd.to_datetime(formatted_data['ds'])
    return formatted_data


def run_prophet_forecast(sales_data, periods=4):
    """
    Runs a sales forecast using Prophet.

    Parameters:
    - sales_data (pd.DataFrame): Sales data formatted for Prophet with 'ds' and 'y' columns.
    - periods (int): Number of periods to forecast into the future.

    Returns:
    - forecast (pd.DataFrame): Forecasted data returned by Prophet, including components.
    """
    # Instantiate and fit the model
    model = Prophet(daily_seasonality=False, yearly_seasonality=True)
    model.fit(sales_data)

    # Create a future dataframe and forecast
    future_dates = model.make_future_dataframe(periods=periods, freq='M')
    forecast = model.predict(future_dates)

    return forecast


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