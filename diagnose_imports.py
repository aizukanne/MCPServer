#!/usr/bin/env python3
"""
Diagnostic script to identify import failures in the MCP Server application.
"""

import sys
import importlib
import traceback
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_import(module_name, package_name=None):
    """Test importing a module and report any errors."""
    print(f"\n{'='*60}")
    print(f"Testing import: {module_name}")
    print(f"{'='*60}")
    
    try:
        if package_name:
            module = importlib.import_module(module_name, package=package_name)
        else:
            module = importlib.import_module(module_name)
        print(f"✅ SUCCESS: {module_name} imported successfully")
        
        # Check for specific attributes if it's a known module
        if module_name == 'config':
            attrs_to_check = ['client', 'docs_bucket_name', 'openai_api_key']
            for attr in attrs_to_check:
                if hasattr(module, attr):
                    value = getattr(module, attr)
                    if value is None:
                        print(f"⚠️  WARNING: {attr} is None")
                    else:
                        print(f"✅ {attr} is set")
                else:
                    print(f"❌ MISSING: {attr} not found in module")
                    
        return True
    except ImportError as e:
        print(f"❌ IMPORT ERROR: {e}")
        print("\nDetailed traceback:")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {type(e).__name__}: {e}")
        print("\nDetailed traceback:")
        traceback.print_exc()
        return False

def check_package_installed(package_name):
    """Check if a package is installed."""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def main():
    print("MCP Server Import Diagnostics")
    print("="*60)
    
    # Check critical dependencies first
    critical_packages = [
        ('fpdf', 'fpdf==1.7.2'),
        ('openai', 'openai>=1.0.0'),
        ('boto3', 'boto3>=1.26.0'),
        ('weaviate', 'weaviate-client>=3.15.0'),
        ('slack_sdk', 'slack_sdk (not in requirements.txt)'),
        ('markdown2', 'markdown2>=2.4.0'),
        ('mcp', 'mcp>=0.9.0'),
    ]
    
    print("\nChecking critical packages:")
    print("-"*60)
    missing_packages = []
    for package, requirement in critical_packages:
        if check_package_installed(package):
            print(f"✅ {package} is installed")
        else:
            print(f"❌ {package} is NOT installed (requirement: {requirement})")
            missing_packages.append((package, requirement))
    
    # Test importing config module
    config_success = test_import('config')
    
    # Test importing services that depend on config
    if config_success:
        test_import('services.document_service')
    else:
        print("\n⚠️  Skipping document_service import test due to config failure")
        
        # Try importing document_service with mocked dependencies
        print("\nTrying to import document_service with mocked dependencies...")
        
        # Create a mock config module
        import types
        mock_config = types.ModuleType('config')
        mock_config.docs_bucket_name = 'mock-bucket'
        mock_config.client = None
        sys.modules['config'] = mock_config
        
        # Mock fpdf if not installed
        if not check_package_installed('fpdf'):
            mock_fpdf = types.ModuleType('fpdf')
            mock_fpdf.FPDF = type('FPDF', (), {})
            sys.modules['fpdf'] = mock_fpdf
            
        test_import('services.document_service')
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if missing_packages:
        print("\n❌ Missing packages that need to be installed:")
        for package, requirement in missing_packages:
            print(f"   - {requirement}")
        print("\nTo install missing packages, run:")
        print("   pip install -r requirements.txt")
        if any(p[0] == 'slack_sdk' for p in missing_packages):
            print("\n⚠️  Note: slack_sdk is not in requirements.txt")
            print("   You may need to install it separately:")
            print("   pip install slack-sdk")
    
    if not config_success:
        print("\n❌ The config module failed to import, which is causing cascade failures")
        print("   This is likely due to missing dependencies or environment variables")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()