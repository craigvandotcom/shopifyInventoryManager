import shopify
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

def setup_shopify_for_sales(api_version, shop_url, access_token):
    """
    Helper function to set up Shopify API before fetching sales data.
    """
    shopify.ShopifyResource.set_site(f"https://{shop_url}.myshopify.com/admin/api/{api_version}")
    shopify.ShopifyResource.activate_session(shopify.Session(f"{shop_url}.myshopify.com", api_version, access_token))

def fetch_sales_data_previous_months(months_back=12):
    """
    Fetches sales data from the previous specified number of months till now.

    Parameters:
    - months_back (int): Number of months to look back for sales data.

    Returns:
    - pd.DataFrame: A DataFrame with columns for product_id, quantity, and date of sales.
    """
    today = datetime.today()
    start_date = today.replace(day=1) - relativedelta(months=months_back)
    end_date = today.replace(day=1) - relativedelta(days=1)

    start_date_str = start_date.date().isoformat()
    end_date_str = end_date.date().isoformat()

    sales_data = []
    params = {
        "created_at_min": start_date_str,
        "created_at_max": end_date_str,
        "status": "any",
        "limit": 250
    }

    while True:
        orders = shopify.Order.find(**params)
        for order in orders:
            for line_item in order.line_items:
                sales_data.append({
                    'product_id': line_item.product_id,
                    'quantity': line_item.quantity,
                    'date': order.created_at
                })

        # Check if there's a next page of orders
        if orders.has_next_page():
            # Correctly access the 'next_page_url' property
            next_page_info = orders.next_page_url.split("page_info=")[-1] if orders.next_page_url else None
            if next_page_info:
                params = {"page_info": next_page_info}
            else:
                break
        else:
            break

    return pd.DataFrame(sales_data)

def aggregate_sales_data(sales_data):
    """
    Aggregates sales data by product_id and month.

    Parameters:
    - sales_data (pd.DataFrame): DataFrame containing sales data with product_id, quantity, and date.

    Returns:
    - pd.DataFrame: DataFrame aggregated by month and product_id.
    """
    sales_data['date'] = pd.to_datetime(sales_data['date']).dt.date
    sales_data['month_year'] = pd.to_datetime(sales_data['date']).dt.to_period('M')

    return sales_data.groupby(['product_id', 'month_year'])['quantity'].sum().reset_index()