# Web Browsing Tools

These tools provide web browsing and searching capabilities.

## `google_search`

Perform a Google search with advanced operators.

- **Parameters:**
  - `search_term` (string): The term to search for.
  - `before` (string, optional): Returns results before a specific date.
  - `after` (string, optional): Returns results after a specific date.
  - `intext` (string, optional): Returns results with the specified text in the body of the page.
  - `allintext` (string, optional): Returns results with all the specified text in the body of the page.
  - `and_condition` (string, optional): Returns results that include all the specified terms.
  - `must_have` (string, optional): Returns results that must include the specified terms.
- **Returns:**
  - A JSON object containing the search results.

## `browse_internet`

Extract content from multiple URLs.

- **Parameters:**
  - `urls` (list): A list of URLs to browse.
  - `full_text` (boolean, optional): Whether to return the full text of the page or a summary.
- **Returns:**
  - A JSON object containing the content of the URLs.

## `shorten_url`

Create a shortened URL.

- **Parameters:**
  - `url` (string): The URL to shorten.
  - `custom_code` (string, optional): A custom code for the shortened URL.
- **Returns:**
  - A JSON object containing the shortened URL.