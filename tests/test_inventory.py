import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.shopify_api.inventory import fetch_current_stock_levels, calculate_safety_stock_and_order_sizes

class TestInventory(unittest.TestCase):

    def test_fetch_current_stock_levels(self):
        """Test fetching of current stock levels."""
        sample_product_info = {
            'Product1': {'InventoryItemID': '123'},
            'Product2': {'InventoryItemID': '456'}
        }

        sample_response = MagicMock()
        sample_response.available = 100  # Assuming each InventoryItemID has 100 available

        with patch('src.shopify_api.inventory.shopify.InventoryLevel.find', return_value=[sample_response, sample_response]):
            stock_levels = fetch_current_stock_levels(sample_product_info)

        self.assertEqual(stock_levels, {'Product1': 100, 'Product2': 100})

    def test_calculate_safety_stock_and_order_sizes(self):
        """Test calculation of safety stocks and order sizes."""
        sample_sales_data_df = pd.DataFrame({
            'product_id': [1, 1, 2, 2],
            'quantity': [10, 20, 30, 40],
            'date': pd.to_datetime(['2023-01-01', '2023-02-01', '2023-01-01', '2023-02-01']),
        })

        sample_product_info = {
            'Product1': {'ProductID': 1},
            'Product2': {'ProductID': 2},
        }

        sample_forecast_results = {
            'Product1': {pd.Period('2023-03'): 15, pd.Period('2023-04'): 25},
            'Product2': {pd.Period('2023-03'): 35, pd.Period('2023-04'): 45},
        }

        safety_stock, order_sizes = calculate_safety_stock_and_order_sizes(
            sales_data_df=sample_sales_data_df,
            product_info=sample_product_info,
            forecast_results=sample_forecast_results,
            lead_time_days=30
        )

        # Expected safety stock and order sizes should be based on mocked values above
        # Be sure to customize the assertions based on your specific logic within
        # the calculate_safety_stock_and_order_sizes function.
        expected_safety_stock = {'Product1': ..., 'Product2': ...}
        expected_order_sizes = {'Product1': ..., 'Product2': ...}

        self.assertEqual(safety_stock, expected_safety_stock)
        self.assertEqual(order_sizes, expected_order_sizes)

if __name__ == "__main__":
    unittest.main()