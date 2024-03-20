import shopify

def setup_shopify_session(shop_name, api_version, access_token):
    """
    Sets up the Shopify session for API calls.
  
    Parameters:
    - shop_name (str): The shop URL without https:// and .myshopify.com part.
    - api_version (str): The desired API version.
    - access_token (str): The API access token.
  
    Returns:
    None
    """
    session = shopify.Session(f"{shop_name}.myshopify.com", api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

def deactivate_shopify_session():
    """
    Deactivates the current Shopify session.

    Returns:
    None
    """
    shopify.ShopifyResource.clear_session()
  