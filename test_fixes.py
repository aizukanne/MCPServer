#!/usr/bin/env python3
"""Test script to verify the fixes for the MCP server issues."""

import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def test_config_import():
    """Test if config.py can be imported without errors."""
    logger.info("Testing config.py import...")
    try:
        import config
        logger.info("✓ config.py imported successfully")
        
        # Check if base_url is defined
        if hasattr(config, 'base_url'):
            logger.info(f"✓ base_url is defined: {config.base_url}")
        else:
            logger.error("✗ base_url is not defined in config")
            
        # Check Weaviate client functions
        if hasattr(config, 'get_or_create_weaviate_client'):
            logger.info("✓ get_or_create_weaviate_client function exists")
        else:
            logger.error("✗ get_or_create_weaviate_client function not found")
            
        if hasattr(config, 'close_weaviate_client'):
            logger.info("✓ close_weaviate_client function exists")
        else:
            logger.error("✗ close_weaviate_client function not found")
            
        return True
    except Exception as e:
        logger.error(f"✗ Failed to import config.py: {e}")
        return False

def test_service_imports():
    """Test if services can be imported without errors."""
    logger.info("\nTesting service imports...")
    
    services = [
        'services.odoo_service',
        'services.storage_service',
        'services.web_service'
    ]
    
    all_good = True
    for service in services:
        try:
            __import__(service)
            logger.info(f"✓ {service} imported successfully")
        except Exception as e:
            logger.error(f"✗ Failed to import {service}: {e}")
            all_good = False
            
    return all_good

def test_main_import():
    """Test if main.py can be imported without errors."""
    logger.info("\nTesting main.py import...")
    try:
        import main
        logger.info("✓ main.py imported successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to import main.py: {e}")
        return False

def test_weaviate_cleanup():
    """Test Weaviate client cleanup."""
    logger.info("\nTesting Weaviate client cleanup...")
    try:
        from config import get_or_create_weaviate_client, close_weaviate_client
        
        # Try to get client (it may be None if not configured)
        client = get_or_create_weaviate_client()
        if client:
            logger.info("✓ Weaviate client created")
        else:
            logger.info("✓ Weaviate client not configured (expected if credentials missing)")
        
        # Test cleanup
        close_weaviate_client()
        logger.info("✓ Weaviate cleanup function executed")
        return True
    except Exception as e:
        logger.error(f"✗ Weaviate cleanup test failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("Starting MCP Server fix verification...\n")
    
    tests = [
        test_config_import,
        test_service_imports,
        test_main_import,
        test_weaviate_cleanup
    ]
    
    results = []
    for test in tests:
        results.append(test())
        
    # Summary
    logger.info("\n" + "="*50)
    logger.info("TEST SUMMARY")
    logger.info("="*50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        logger.info(f"✓ All tests passed ({passed}/{total})")
        logger.info("\nThe fixes have been applied successfully!")
        logger.info("You should now be able to run the MCP server without the previous errors.")
    else:
        logger.error(f"✗ Some tests failed ({passed}/{total} passed)")
        logger.error("\nThere are still some issues to resolve.")
        
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())