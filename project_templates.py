"""
CloudFormation Parameter Templates
==================================

Templates for CloudFormation parameter files for different environments.
"""

import json


class ParameterTemplates:
    """CloudFormation parameter file templates."""
    
    def get_dev_parameters(self) -> str:
        """Get development environment parameters."""
        params = [
            {"ParameterKey": "Environment", "ParameterValue": "dev"},
            {"ParameterKey": "ProjectName", "ParameterValue": "mcp-office-assistant"},
            {"ParameterKey": "AllowedOrigins", "ParameterValue": "*"},
            {"ParameterKey": "OpenAIApiKey", "ParameterValue": "REPLACE_WITH_YOUR_OPENAI_API_KEY"},
            {"ParameterKey": "SlackBotToken", "ParameterValue": "REPLACE_WITH_YOUR_SLACK_BOT_TOKEN"},
            {"ParameterKey": "OpenWeatherApiKey", "ParameterValue": "REPLACE_WITH_YOUR_OPENWEATHER_API_KEY"},
            {"ParameterKey": "GoogleSearchApiKey", "ParameterValue": "REPLACE_WITH_YOUR_GOOGLE_SEARCH_API_KEY"},
            {"ParameterKey": "GoogleSearchEngineId", "ParameterValue": "REPLACE_WITH_YOUR_SEARCH_ENGINE_ID"}
        ]
        return json.dumps(params, indent=2)
    
    def get_staging_parameters(self) -> str:
        """Get staging environment parameters."""
        params = [
            {"ParameterKey": "Environment", "ParameterValue": "staging"},
            {"ParameterKey": "ProjectName", "ParameterValue": "mcp-office-assistant"},
            {"ParameterKey": "AllowedOrigins", "ParameterValue": "https://staging.yourdomain.com"},
            {"ParameterKey": "OpenAIApiKey", "ParameterValue": "REPLACE_WITH_STAGING_OPENAI_API_KEY"},
            {"ParameterKey": "SlackBotToken", "ParameterValue": "REPLACE_WITH_STAGING_SLACK_BOT_TOKEN"},
            {"ParameterKey": "OpenWeatherApiKey", "ParameterValue": "REPLACE_WITH_STAGING_OPENWEATHER_API_KEY"},
            {"ParameterKey": "GoogleSearchApiKey", "ParameterValue": "REPLACE_WITH_STAGING_GOOGLE_SEARCH_API_KEY"},
            {"ParameterKey": "GoogleSearchEngineId", "ParameterValue": "REPLACE_WITH_STAGING_SEARCH_ENGINE_ID"}
        ]
        return json.dumps(params, indent=2)
    
    def get_prod_parameters(self) -> str:
        """Get production environment parameters.""" 
        params = [
            {"ParameterKey": "Environment", "ParameterValue": "prod"},
            {"ParameterKey": "ProjectName", "ParameterValue": "mcp-office-assistant"},
            {"ParameterKey": "AllowedOrigins", "ParameterValue": "https://yourdomain.com,https://app.yourdomain.com"},
            {"ParameterKey": "OpenAIApiKey", "ParameterValue": "REPLACE_WITH_PRODUCTION_OPENAI_API_KEY"},
            {"ParameterKey": "SlackBotToken", "ParameterValue": "REPLACE_WITH_PRODUCTION_SLACK_BOT_TOKEN"},
            {"ParameterKey": "OpenWeatherApiKey", "ParameterValue": "REPLACE_WITH_PRODUCTION_OPENWEATHER_API_KEY"},
            {"ParameterKey": "GoogleSearchApiKey", "ParameterValue": "REPLACE_WITH_PRODUCTION_GOOGLE_SEARCH_API_KEY"},
            {"ParameterKey": "GoogleSearchEngineId", "ParameterValue": "REPLACE_WITH_PRODUCTION_SEARCH_ENGINE_ID"}
        ]
        return json.dumps(params, indent=2)