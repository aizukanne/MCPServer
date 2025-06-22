# MCP Office Assistant - API Reference

## Overview

The MCP Office Assistant provides 26 tools across 8 categories for comprehensive office automation.

## Tool Categories

### 🌤️ Weather Tools

#### get_weather_data
Get current weather information for any location.

**Parameters:**
- `location_name` (string, optional): Location name (default: "Whitehorse")

**Example:**
```python
client.get_weather("New York")
```

#### get_coordinates  
Get latitude and longitude coordinates for a location.

**Parameters:**
- `location_name` (string, required): Location name

**Example:**
```python
client.execute_tool("get_coordinates", location_name="London")
```

### 🌐 Web Browsing Tools

#### google_search
Perform advanced Google search with operators.

**Parameters:**
- `search_term` (string, required): Main search query
- `before` (string, optional): Date before (YYYY-MM-DD)
- `after` (string, optional): Date after (YYYY-MM-DD)  
- `intext` (string, optional): Text that must appear in content
- `allintext` (string, optional): All terms that must appear
- `and_condition` (string, optional): Additional AND term
- `must_have` (string, optional): Exact phrase required

**Example:**
```python
client.google_search("AI research", after="2024-01-01", intext="GPT")
```

#### browse_internet
Extract content from web pages.

**Parameters:**
- `urls` (array, required): List of URLs to browse
- `full_text` (boolean, optional): Return full text vs summary

**Example:**
```python
client.browse_urls(["https://example.com", "https://news.com"])
```

#### shorten_url
Create shortened URLs.

**Parameters:**
- `url` (string, required): URL to shorten
- `custom_code` (string, optional): Custom short code

**Example:**
```python
client.shorten_url("https://very-long-url.com/path")
```

### 💾 Storage & Messages

#### get_message_by_sort_id
Retrieve specific message by ID.

#### get_messages_in_range
Get messages within time range.

#### get_users
Get user information.

#### get_channels
Get channel information.

#### manage_mute_status
Manage channel mute status.

### 💬 Slack Integration

#### send_file_to_slack
Upload files to Slack.

#### update_slack_users
Sync user data from Slack.

#### update_slack_conversations  
Sync channel data from Slack.

### 🏢 Odoo ERP Integration

#### odoo_get_mapped_models
Get available Odoo models.

#### odoo_fetch_records
Retrieve Odoo records.

#### odoo_create_record
Create new Odoo record.

#### odoo_update_record
Update existing Odoo record.

#### odoo_delete_record
Delete Odoo record.

#### odoo_print_record
Generate PDF report for Odoo record.

#### odoo_post_record
Post Odoo record (change status).

### 🛒 Amazon Integration

#### search_amazon_products
Search Amazon marketplace.

#### search_and_format_products
Search Amazon with formatted results.

### 📄 Document Management

#### send_as_pdf
Convert text to PDF and upload to Slack.

#### list_files
List files in S3 bucket.

#### get_embedding
Generate text embeddings.

### 🔧 Utilities

#### solve_maths
Execute mathematical calculations.

#### ask_openai_o1
Query OpenAI O1 model.

## Response Format

All tools return responses in this format:

```json
{
  "status": "success|error",
  "data": { ... },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Authentication

### API Key Authentication
Include in headers:
```
x-api-key: your-api-key-here
```

### Project Identification (Optional)
Include for multi-tenant usage:
```
X-Project-ID: project-name
```

## Rate Limits

- **Default**: 50 requests/second, 10,000/month
- **Burst**: Up to 100 requests in short periods
- **Per-project**: Limits apply per API key

## Error Codes

- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid API key)
- `404` - Tool not found
- `429` - Rate limit exceeded
- `500` - Internal server error
