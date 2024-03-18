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

def aggregate_forecast_sales(forecast, freq='MS'):
    """
    Summarizes the forecast into specified frequency aggregate sales.

    Parameters:
    - forecast (pd.DataFrame): Forecast data from Prophet model.
    - freq (str): Frequency string to resample and aggregate forecast values. Defaults to 'MS' (month start)

    Returns:
    - pd.DataFrame: Aggregated sales forecasts.
    """
    # Using 'yhat' as the forecasted values column
    forecast_agg = forecast.set_index('ds')['yhat'].resample(freq).sum().reset_index()
    forecast_agg.rename(columns={'yhat': 'forecasted_sales'}, inplace=True)
    return forecast_agg