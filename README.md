# Daily Stock Checker, Order Notifier & Order Calculator
1.  run daily call to Shopy API to retrieve EoD numbers
2.  determine order notification by checking if stock prior to delivery is equal or lower than buffer stock quantity
3.  if yes, send a notification with minimum order amounts for each product, and current stock, imminent order & delivery date

### Tasks
- [x] design high-level structure of project, files, functions etc.
- [x] transform .pynb to single file then to project of files
 - [x] figure out secret_keys between github and replit
- [ ] DEBUG

- [ ] build daily trigger using Scheduler?
    - https://schedule.readthedocs.io/en/stable/
- [ ] manage data export/download/protect
    - [ ] slack / email / 

- [ ] troubleshoot
- [ ] clean code & review
- [ ] complete documentation


# How to use

### Setup

Setup your local variables and secrets:
- shopify API key [SHOPIFY-API-KEY]
- shopify store name [SHOP_NAME]
- product shopify names (exactly matching) [PRODUCT1_SHOPIFY_NAME, PRODUCT2_SHOPIFY_NAME, etc.]
- product variable names (shortened for cleanliness) [PRODUCT1_VAR_NAME, PRODUCT2_VAR_NAME, etc.]

---

# Project Overview

This project interfaces with the Shopify API to fetch sales data and inventory levels, calculate safety stock and order sizes, and forecast future sales using the Prophet forecasting model. It's structured to separate concerns between interacting with the Shopify API, performing forecasting, and utility operations.

## Directory Structure

- `__init__.py`: Makes Python treat the directories as containing packages.
- `shopify_api/`: Contains modules to interact with the Shopify API.
    - `__init__.py`: Package initializer.
    - `client.py`: Sets up the Shopify session.
    - `inventory.py`: Handles inventory level fetching and safety stock calculations.
    - `sales.py`: Fetches sales data and aggregates it for forecasting.
- `forecasting/`: Contains modules for sales forecasting.
    - `__init__.py`: Package initializer.
    - `prophet_model.py`: Wraps the Prophet model for sales forecasting.
    - `utilities.py`: Provides utilities for data manipulation and visualization.
- `main.py`: The entry point for running the project's main workflow.

## Setup Instructions

1. Ensure Python 3.8+ is installed.
2. Install dependencies: Run `poetry install` in the project root directory.
3. Configure `.env` in the project root with your Shopify details:
      SHOP_NAME=your_shop_name
      SHOPIFY_API_KEY=your_api_key
4. Navigate to the `src/` directory to run the main script: `python main.py`.

## Running the project

With your Shopify API details set up in your `.env` file, execute the project's main workflow by running the `main.py` script:

```bash
`python main.py`

This script will handle API session setup, data fetching, stock level calculation, and sales forecasting.

Contributing
Refer to each modules docstrings for detailed descriptions of functions, expected parameters, and return types. Contributions should follow the established modular structure and include appropriate unit tests.

Running Tests
Unit tests are located in the 
../tests/
 directory. To run all tests, execute the following command from the project root:

`poetry run pytest`

Ensure you have pytest installed and configured as per the 
pyproject.toml
 file.

Notes
This project is configurable via environment variables located in the 
.env file. The configs/settings.toml can be modified to adjust application settings such as API versions or date ranges for data fetching.
For more detailed API documentation, see the official Shopify API documentation.

License
This project is licensed under the MIT License - see the LICENSE file in the project root for details.


_This is a general template. Please adapt it according to your projects specifics, the naming conventions youve followed, and any additional or modified functionality not captured here._

