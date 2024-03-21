import os
import shopify

def map_product_var():
    """
    Creates a mapping of Shopify product names to variable names using environment variables.

    Returns:
    - dict: A dictionary mapping product names to variable names.
    """
    product_mapping = {
        os.getenv('PRODUCT1_SHOPIFY_NAME'): os.getenv('PRODUCT1_VAR_NAME'),
        os.getenv('PRODUCT2_SHOPIFY_NAME'): os.getenv('PRODUCT2_VAR_NAME'),
        os.getenv('PRODUCT3_SHOPIFY_NAME'): os.getenv('PRODUCT3_VAR_NAME'),
        os.getenv('PRODUCT4_SHOPIFY_NAME'): os.getenv('PRODUCT4_VAR_NAME'),
        os.getenv('PRODUCT5_SHOPIFY_NAME'): os.getenv('PRODUCT5_VAR_NAME'),
        os.getenv('PRODUCT6_SHOPIFY_NAME'): os.getenv('PRODUCT6_VAR_NAME'),
        os.getenv('PRODUCT7_SHOPIFY_NAME'): os.getenv('PRODUCT7_VAR_NAME'),
        os.getenv('PRODUCT8_SHOPIFY_NAME'): os.getenv('PRODUCT8_VAR_NAME')
    }
    return product_mapping

def fetch_details(product_mapping):
    """
    Fetches product details from Shopify.
    Parameters:
    - product_mapping (dict): A dictionary mapping product names to variable names.
    Returns:
    - dict: A dictionary containing product details.
    """

    product_info = {}  # Dictionary to hold your variable names as keys and product/inventory IDs as values

    products = shopify.Product.find()
    for product in products:
        for key, value in product_mapping.items():
            if key.upper() in product.title.upper():  # Using upper() for case-insensitive comparison
                for variant in product.variants:
                    # Assigning product ID and inventory item ID to your dictionary
                    product_info[value] = {
                        "ProductID": product.id,
                        "VariantID": variant.id,
                        "InventoryItemID": variant.inventory_item_id
                    }
                    break  # Exit the inner loop once a match is found
    return product_info
