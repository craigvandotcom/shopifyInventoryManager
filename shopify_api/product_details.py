# Step 1: Create a mapping of product names to your variable naming format


# Step 2: Fetch products and match them to your mapping
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
  