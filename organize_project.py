#!/usr/bin/env python3
"""
MCP Office Assistant - Project Organization Script
==================================================

This script automatically organizes all the files from the artifacts into the correct 
directory structure for both local MCP server and AWS Lambda deployment.
"""

import os
import shutil
import json
from pathlib import Path
from typing import Dict, List

class ProjectOrganizer:
    """Organizes MCP Office Assistant project files."""
    
    def __init__(self, base_path: str = "."):
        """Initialize with the base project path."""
        self.base_path = Path(base_path)
        self.aws_deployment_path = self.base_path / "aws-deployment"
        
    def create_directory_structure(self):
        """Create the complete directory structure."""
        print("📁 Creating directory structure...")
        
        # Main project directories
        directories = [
            "handlers",
            "services", 
            "schemas",
            "utils",
            "docs",
            "aws-deployment/cloudformation",
            "aws-deployment/src/handlers",
            "aws-deployment/src/services",
            "aws-deployment/src/schemas", 
            "aws-deployment/src/utils",
            "aws-deployment/layers/dependencies",
            "aws-deployment/examples",
            "aws-deployment/scripts"
        ]
        
        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Created {directory}/")
            
            # Create __init__.py files for Python packages
            if any(pkg in directory for pkg in ['handlers', 'services', 'schemas', 'utils']):
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    init_file.write_text("# MCP Office Assistant package\n")
                    print(f"   📄 Created {directory}/__init__.py")
    
    def create_parameter_files(self):
        """Create CloudFormation parameter files."""
        print("\n📄 Creating CloudFormation parameter files...")
        
        # Import parameter templates
        from project_templates import ParameterTemplates
        templates = ParameterTemplates()
        
        param_files = {
            "cloudformation/parameters-dev.json": templates.get_dev_parameters(),
            "cloudformation/parameters-staging.json": templates.get_staging_parameters(),
            "cloudformation/parameters-prod.json": templates.get_prod_parameters()
        }
        
        for file_path, content in param_files.items():
            full_path = self.aws_deployment_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not full_path.exists():
                full_path.write_text(content)
                print(f"   ✅ Created aws-deployment/{file_path}")
    
    def create_utility_scripts(self):
        """Create utility scripts."""
        print("\n🔧 Creating utility scripts...")
        
        # Import script templates
        from script_templates import ScriptTemplates
        templates = ScriptTemplates()
        
        scripts = {
            "scripts/setup_environment.sh": templates.get_setup_script(),
            "examples/test_api.sh": templates.get_test_script(),
            "scripts/cleanup.sh": templates.get_cleanup_script(),
            "copy_artifacts.sh": templates.get_copy_script()  # Root level
        }
        
        for script_path, content in scripts.items():
            if script_path.startswith("copy_artifacts.sh"):
                # Root level script
                full_path = self.base_path / script_path
            else:
                # AWS deployment script
                full_path = self.aws_deployment_path / script_path
            
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not full_path.exists():
                full_path.write_text(content)
                os.chmod(full_path, 0o755)
                print(f"   ✅ Created {script_path} (executable)")
    
    def create_config_files(self):
        """Create configuration and environment files."""
        print("\n⚙️ Creating configuration files...")
        
        # Import config templates
        from config_templates import ConfigTemplates
        templates = ConfigTemplates()
        
        configs = {
            ".env.example": templates.get_env_template(),
            ".gitignore": templates.get_gitignore_template(),
            "examples/client.js": templates.get_js_client_template()
        }
        
        for config_path, content in configs.items():
            if config_path.startswith('.'):
                # Root level files
                full_path = self.base_path / config_path
            else:
                # AWS deployment files
                full_path = self.aws_deployment_path / config_path
            
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not full_path.exists():
                full_path.write_text(content)
                print(f"   ✅ Created {config_path}")
    
    def create_documentation(self):
        """Create documentation files."""
        print("\n📚 Creating documentation files...")
        
        # Import doc templates
        from doc_templates import DocumentationTemplates
        templates = DocumentationTemplates()
        
        docs = {
            "docs/API_REFERENCE.md": templates.get_api_reference(),
            "docs/TROUBLESHOOTING.md": templates.get_troubleshooting_guide(),
            "docs/CHANGELOG.md": templates.get_changelog(),
            "DEPLOYMENT_COMPARISON.md": templates.get_deployment_comparison()
        }
        
        for doc_path, content in docs.items():
            full_path = self.base_path / doc_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not full_path.exists():
                full_path.write_text(content)
                print(f"   ✅ Created {doc_path}")
    
    def display_artifact_instructions(self):
        """Display instructions for copying artifacts."""
        print("\n📋 ARTIFACT COPYING INSTRUCTIONS")
        print("=" * 50)
        
        artifact_mappings = [
            {
                "name": "CloudFormation Template",
                "artifact": "cloudformation/mcp-infrastructure.yaml",
                "destination": "aws-deployment/cloudformation/mcp-infrastructure.yaml",
                "description": "Main infrastructure template"
            },
            {
                "name": "Lambda Handlers",
                "artifact": "src/lambda_handlers.py", 
                "destination": "aws-deployment/src/lambda_handlers.py",
                "description": "Main Lambda function handlers"
            },
            {
                "name": "Specialized Handlers",
                "artifact": "src/specialized_handlers.py",
                "destination": "aws-deployment/src/specialized_handlers.py", 
                "description": "Heavy operation handlers"
            },
            {
                "name": "Deployment Script",
                "artifact": "deploy.sh",
                "destination": "aws-deployment/deploy.sh",
                "description": "Main deployment automation script"
            },
            {
                "name": "SAM Configuration",
                "artifact": "samconfig.toml",
                "destination": "aws-deployment/samconfig.toml",
                "description": "SAM CLI configuration"
            },
            {
                "name": "Python Client Example",
                "artifact": "examples/client.py",
                "destination": "aws-deployment/examples/client.py",
                "description": "Python API client example"
            },
            {
                "name": "AWS Deployment Guide", 
                "artifact": "AWS_DEPLOYMENT_GUIDE.md",
                "destination": "aws-deployment/AWS_DEPLOYMENT_GUIDE.md",
                "description": "Complete AWS deployment documentation"
            },
            {
                "name": "Tool Schemas",
                "artifact": "schemas/tool_schemas.py",
                "destination": "schemas/tool_schemas.py (and copy to aws-deployment/src/schemas/)",
                "description": "MCP tool schema definitions"
            },
            {
                "name": "All Handlers",
                "artifact": "handlers/*.py (8 files)",
                "destination": "handlers/ (and copy to aws-deployment/src/handlers/)", 
                "description": "MCP tool handler implementations"
            },
            {
                "name": "All Services",
                "artifact": "services/*.py (8 files)",
                "destination": "services/ (and copy to aws-deployment/src/services/)",
                "description": "Business logic service implementations"
            },
            {
                "name": "Utilities",
                "artifact": "utils/*.py (3 files)",
                "destination": "utils/ (and copy to aws-deployment/src/utils/)",
                "description": "Validation, formatting, and text processing utilities"
            }
        ]
        
        for i, mapping in enumerate(artifact_mappings, 1):
            print(f"\n{i:2d}. {mapping['name']}")
            print(f"    📂 Copy: {mapping['artifact']}")
            print(f"    📍 To:   {mapping['destination']}")
            print(f"    📝 Desc: {mapping['description']}")
    
    def verify_setup(self):
        """Verify the project setup is complete."""
        print("\n🔍 Verifying project setup...")
        
        required_files = [
            "aws-deployment/cloudformation/parameters-dev.json",
            "aws-deployment/scripts/setup_environment.sh",
            "aws-deployment/examples/test_api.sh",
            "copy_artifacts.sh",
            ".env.example",
            ".gitignore"
        ]
        
        required_dirs = [
            "handlers",
            "services", 
            "schemas",
            "utils",
            "aws-deployment/src",
            "aws-deployment/cloudformation",
            "aws-deployment/examples",
            "docs"
        ]
        
        # Check directories
        missing_dirs = []
        for directory in required_dirs:
            if not (self.base_path / directory).exists():
                missing_dirs.append(directory)
        
        # Check files
        missing_files = []
        for file_path in required_files:
            if not (self.base_path / file_path).exists():
                missing_files.append(file_path)
        
        if not missing_dirs and not missing_files:
            print("   ✅ All required directories and files created!")
        else:
            if missing_dirs:
                print(f"   ❌ Missing directories: {missing_dirs}")
            if missing_files:
                print(f"   ❌ Missing files: {missing_files}")
    
    def display_next_steps(self):
        """Display next steps for the user."""
        print("\n" + "="*60)
        print("🎉 PROJECT ORGANIZATION COMPLETE!")
        print("="*60)
        
        print("\n📋 NEXT STEPS:")
        print("\n1. 📥 Copy Artifact Files:")
        print("   • Download all artifacts from the conversation")
        print("   • Create an 'artifacts' directory") 
        print("   • Place artifact files in the artifacts directory")
        print("   • Run: ./copy_artifacts.sh")
        
        print("\n2. 🔑 Configure API Keys:")
        print("   • Edit: aws-deployment/cloudformation/parameters-dev.json")
        print("   • Replace all 'REPLACE_WITH_YOUR_*' values")
        print("   • Copy .env.example to .env and fill in values")
        
        print("\n3. 🧪 Test Locally:")
        print("   • Ensure your config.py and url_shortener.py work")
        print("   • Run: python main.py")
        print("   • Test with your AI application")
        
        print("\n4. ☁️ Deploy to AWS:")
        print("   • Install prerequisites: ./aws-deployment/scripts/setup_environment.sh")
        print("   • Deploy: cd aws-deployment && ./deploy.sh dev us-west-2 deploy")
        print("   • Test: python examples/client.py")
        
        print("\n5. 📖 Read Documentation:")
        print("   • Local setup: SETUP.md")
        print("   • AWS deployment: aws-deployment/AWS_DEPLOYMENT_GUIDE.md")
        print("   • Integration guide: INTEGRATION_GUIDE.md")
        print("   • API reference: docs/API_REFERENCE.md")
        
        print("\n🔗 USEFUL COMMANDS:")
        print("   • Copy artifacts: ./copy_artifacts.sh")
        print("   • Setup AWS: ./aws-deployment/scripts/setup_environment.sh")
        print("   • Deploy dev: cd aws-deployment && ./deploy.sh dev us-west-2 deploy")
        print("   • Test API: ./aws-deployment/examples/test_api.sh <API_URL> <API_KEY>")
        print("   • Cleanup: ./aws-deployment/scripts/cleanup.sh dev us-west-2")
        
        print(f"\n📁 PROJECT STRUCTURE:")
        print(f"   Root: {self.base_path.absolute()}")
        print(f"   AWS:  {self.aws_deployment_path.absolute()}")
    
    def run_organization(self):
        """Run the complete project organization process."""
        print("🚀 MCP Office Assistant - Project Organization")
        print("=" * 50)
        
        try:
            self.create_directory_structure()
            self.create_parameter_files()
            self.create_utility_scripts()
            self.create_config_files()
            self.create_documentation()
            self.verify_setup()
            self.display_artifact_instructions()
            self.display_next_steps()
            
        except Exception as e:
            print(f"\n❌ Error during organization: {e}")
            return False
        
        return True


def main():
    """Main entry point."""
    import sys
    
    # Get base path from command line or use current directory
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    organizer = ProjectOrganizer(base_path)
    success = organizer.run_organization()
    
    if success:
        print(f"\n✨ Project organization completed successfully!")
        print(f"🎯 Next: Run ./copy_artifacts.sh to copy your artifact files")
    else:
        print(f"\n💥 Project organization failed. Check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()