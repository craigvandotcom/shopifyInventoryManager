# Daily Stock Checker, Order Notifier & Order Calculator
1.  run daily call to Shopy API to retrieve EoD numbers
2.  determine order notification by checking if stock prior to delivery is equal or lower than buffer stock quantity
3.  if yes, send a notification with minimum order amounts for each product, and current stock, imminent order & delivery date

### Tasks
- [x] design high-level structure of project, files, functions etc.
- [ ] transform .pynb to single file then to project of files
- [x] figure out secret_keys between github and replit
- [ ] build daily trigger using Scheduler?
    - https://schedule.readthedocs.io/en/stable/
- [ ] manage data export/download/protect
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