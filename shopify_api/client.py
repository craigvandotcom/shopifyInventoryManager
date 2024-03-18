import shopify
import os

def setup_shopify_session(shop_url, api_version, access_token):
    """
    Sets up the Shopify session for API calls.

    Parameters:
    - shop_url (str): The shop URL.
    - api_version (str): The desired API version.
    - access_token (str): The API access token.

    Returns:
    None
    """
    # Set the base site for ShopifyResource to the shop URL with API version
    shopify.ShopifyResource.set_site(f"https://{shop_url}.myshopify.com/admin/api/{api_version}")

    # Activate the session with access token
    shopify.ShopifyResource.activate_session(shopify.Session(f"{shop_url}.myshopify.com", api_version, access_token))

def deactivate_shopify_session():
    """
    Deactivates the current Shopify session.

    Returns:
    None
    """
    shopify.ShopifyResource.clear_session()

# You may include additional functions for specific API calls if needed.