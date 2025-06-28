# Getting Started

This guide provides step-by-step instructions for setting up the MCP Office Assistant Server.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+:** Required for running the server.
- **Git:** For cloning the repository.
- **`uv`:** For dependency management.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mcp-office-assistant
   ```

2. **Install dependencies:**
   ```bash
   # First, install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Create virtual environment and install dependencies
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file with the necessary API keys and configuration details.

## Configuration

- Ensure your `config.py` file is properly configured.
- Set up Weaviate, DynamoDB tables, and other dependencies as needed.

## Running the Server

Once everything is set up, you can start the server with the following command:

```bash
python main.py