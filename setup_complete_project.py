#!/usr/bin/env python3
"""
Complete Project Setup Script
============================

This script sets up the complete MCP Office Assistant project structure
and provides step-by-step guidance for integration.
"""

import os
import sys
from pathlib import Path

def main():
    """Main setup process."""
    print("🚀 MCP Office Assistant - Complete Project Setup")
    print("=" * 55)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    print(f"📍 Current directory: {current_dir}")
    
    # Ask user if they want to continue
    print("\nThis script will:")
    print("✅ Create complete directory structure")
    print("✅ Generate all configuration templates")
    print("✅ Create deployment scripts")
    print("✅ Set up documentation")
    print("✅ Provide integration instructions")
    
    response = input("\n❓ Continue with setup? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("❌ Setup cancelled.")
        return
    
    try:
        # Import and run the organizer
        print("\n🔧 Running project organization...")
        
        # Add current directory to Python path for imports
        sys.path.insert(0, str(current_dir))
        
        from organize_project import ProjectOrganizer
        
        organizer = ProjectOrganizer(str(current_dir))
        success = organizer.run_organization()
        
        if success:
            print("\n" + "=" * 60)
            print("🎉 PROJECT SETUP COMPLETE!")
            print("=" * 60)
            
            print("\n📋 IMMEDIATE NEXT STEPS:")
            print("\n1. 📥 Download and organize artifacts:")
            print("   • Create: mkdir artifacts")
            print("   • Download all artifacts from the conversation")
            print("   • Save each artifact with these names:")
            print("     - cloudformation/mcp-infrastructure.yaml → artifacts/cloudformation-template.yaml")
            print("     - src/lambda_handlers.py → artifacts/lambda-handlers.py")
            print("     - src/specialized_handlers.py → artifacts/specialized-handlers.py")
            print("     - deploy.sh → artifacts/deploy-script.sh")
            print("     - samconfig.toml → artifacts/sam-config.toml")
            print("     - examples/client.py → artifacts/client-example.py")
            print("     - AWS_DEPLOYMENT_GUIDE.md → artifacts/aws-deployment-guide.md")
            print("     - All handlers/ files → artifacts/handlers/")
            print("     - All services/ files → artifacts/services/")
            print("     - All schemas/ files → artifacts/schemas/")
            print("     - All utils/ files → artifacts/utils/")
            
            print("\n2. 🔧 Copy artifacts to project:")
            print("   ./copy_artifacts.sh")
            
            print("\n3. 🔑 Configure API keys:")
            print("   • Edit: aws-deployment/cloudformation/parameters-dev.json")
            print("   • Replace all REPLACE_WITH_YOUR_* values")
            print("   • Copy .env.example to .env and fill in values")
            
            print("\n4. 🧪 Test locally (if you have existing config.py):")
            print("   python main.py")
            
            print("\n5. ☁️ Deploy to AWS:")
            print("   cd aws-deployment")
            print("   ./scripts/setup_environment.sh")
            print("   ./deploy.sh dev us-west-2 deploy")
            
            print("\n📚 DOCUMENTATION AVAILABLE:")
            print("   • Integration Guide: INTEGRATION_GUIDE.md")
            print("   • AWS Deployment: aws-deployment/AWS_DEPLOYMENT_GUIDE.md")
            print("   • API Reference: docs/API_REFERENCE.md")
            print("   • Troubleshooting: docs/TROUBLESHOOTING.md")
            print("   • Deployment Options: DEPLOYMENT_COMPARISON.md")
            
            print("\n🎯 QUICK START SUMMARY:")
            print("   1. mkdir artifacts && [download artifacts]")
            print("   2. ./copy_artifacts.sh")
            print("   3. Edit API keys in parameter files")
            print("   4. cd aws-deployment && ./deploy.sh dev us-west-2 deploy")
            
            print(f"\n📁 PROJECT ROOT: {current_dir}")
            print(f"📁 AWS DEPLOYMENT: {current_dir}/aws-deployment")
            
        else:
            print("\n❌ Setup failed. Check error messages above.")
            return 1
            
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Make sure all template modules are in the same directory.")
        return 1
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)