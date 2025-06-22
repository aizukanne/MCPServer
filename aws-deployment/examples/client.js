// MCP Office Assistant - JavaScript Client Example
// ================================================

class MCPClient {
  constructor(apiUrl, apiKey, projectId = null) {
    this.apiUrl = apiUrl.replace(/\/$/, ''); // Remove trailing slash
    this.headers = {
      'Content-Type': 'application/json',
      'x-api-key': apiKey
    };
    
    if (projectId) {
      this.headers['X-Project-ID'] = projectId;
    }
  }

  async listTools() {
    const response = await fetch(`${this.apiUrl}/tools`, {
      method: 'GET',
      headers: this.headers
    });
    return response.json();
  }

  async executeTool(toolName, args = {}) {
    const response = await fetch(`${this.apiUrl}/tools/${toolName}`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(args)
    });
    return response.json();
  }

  // Convenience methods
  async getWeather(location = 'Whitehorse') {
    return this.executeTool('get_weather_data', { location_name: location });
  }

  async googleSearch(query, options = {}) {
    return this.executeTool('google_search', { search_term: query, ...options });
  }

  async searchAmazon(query, country = 'CA', options = {}) {
    return this.executeTool('search_amazon_products', { query, country, ...options });
  }

  async solveMath(code, params = {}) {
    return this.executeTool('solve_maths', { code, ...params });
  }

  async getEmbedding(text, model = 'text-embedding-ada-002') {
    return this.executeTool('get_embedding', { text, model });
  }

  async browseUrls(urls, fullText = false) {
    return this.executeTool('browse_internet', { urls, full_text: fullText });
  }
}

// Example usage (Node.js)
async function example() {
  const client = new MCPClient(
    'https://your-api-id.execute-api.us-west-2.amazonaws.com/dev',
    'your-api-key',
    'project-a'
  );

  try {
    // List tools
    const tools = await client.listTools();
    console.log('Available tools:', tools.tools?.length || 0);

    // Get weather
    const weather = await client.getWeather('Tokyo');
    console.log('Weather:', weather);

    // Math calculation
    const math = await client.solveMath('result = 10 * 5 + 2');
    console.log('Math result:', math);

    // Google search
    const search = await client.googleSearch('AI news', { after: '2024-01-01' });
    console.log('Search results:', search);

  } catch (error) {
    console.error('Error:', error);
  }
}

// Uncomment to run example
// example();

module.exports = MCPClient;
