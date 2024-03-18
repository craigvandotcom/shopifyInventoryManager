import unittest
from unittest.mock import patch
import pandas as pd
from src.forecasting.prophet_model import format_sales_data_for_prophet, run_prophet_forecast
# If you have relevant functions in utilities.py, import them here as well.

class TestSalesForecasting(unittest.TestCase):

    def setUp(self):
        # Sample sales data simulating fetched data
        self.sample_sales_data = pd.DataFrame({
            'date': pd.date_range(start='2022-01-01', periods=4, freq='M'),
            'quantity': [10, 20, 30, 40],
            'product_id': [1, 1, 1, 1]  # Assuming a single product for simplicity
        })

    def test_format_sales_data_for_prophet(self):
        """Test that sales data is correctly formatted for Prophet."""
        formatted_data = format_sales_data_for_prophet(self.sample_sales_data)

        # Check that 'ds' and 'y' columns exist
        self.assertIn('ds', formatted_data.columns)
        self.assertIn('y', formatted_data.columns)

        # Check that the number of rows matches the input data
        self.assertEqual(len(formatted_data), len(self.sample_sales_data))

    @patch('src.forecasting.prophet_model.Prophet')
    def test_run_prophet_forecast(self, mock_prophet):
        """Test the forecasting process."""
        # Mocking Prophet model's behavior
        mock_model = mock_prophet.return_value
        mock_model.fit.return_value = None  # Prophet's fit method doesn't return anything
        mock_model.make_future_dataframe.return_value = self.sample_sales_data[['date']].rename(columns={'date':'ds'})
        mock_model.predict.return_value = pd.DataFrame({'ds': pd.date_range(start='2022-05-01', periods=4, freq='M'), 'yhat': [50, 60, 70, 80]})

        forecasted_data = run_prophet_forecast(format_sales_data_for_prophet(self.sample_sales_data), periods=4)

        # Assert 'yhat' column exists in the forecast data
        self.assertIn('yhat', forecasted_data.columns)

        # Check forecasted periods length
        self.assertEqual(len(forecasted_data), 8)  # Original 4 months + 4 forecasted

        # Verify the mock was called as expected
        mock_prophet.assert_called_once()

if __name__ == '__main__':
    unittest.main()