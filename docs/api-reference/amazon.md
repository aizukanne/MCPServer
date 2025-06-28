# Amazon Integration

These tools provide integration with Amazon's product search.

## `search_amazon_products`

Search for products on Amazon.

- **Parameters:**
  - `query` (string): The search query.
  - `country` (string, optional): The Amazon marketplace to search in.
  - `page` (integer, optional): The page number of the search results.
  - `sort_by` (string, optional): The sorting criteria for the results.
  - `product_condition` (string, optional): The condition of the product.
  - `is_prime` (boolean, optional): Whether to only show Prime-eligible products.
  - `deals_and_discounts` (boolean, optional): Whether to only show products with deals and discounts.
- **Returns:**
  - A JSON object containing the search results.

## `search_and_format_products`

Search for products and format the results.

- **Parameters:**
  - `query` (string): The search query.
  - `country` (string, optional): The Amazon marketplace to search in.
  - `max_products` (integer, optional): The maximum number of products to return.
  - `**options`: Additional search options.
- **Returns:**
  - A formatted string containing the search results.