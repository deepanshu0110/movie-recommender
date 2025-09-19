import os
import subprocess
import sys
from config import Config

def setup_project():
    """Complete project setup"""
    print("Setting up Movie Recommendation System...")
    
    # Create directories
    Config.create_directories()
    
    # Download data
    print("Downloading MovieLens dataset...")
    subprocess.run([sys.executable, "download_data.py"])
    
    # Train model
    print("Training recommendation model...")
    subprocess.run([sys.executable, "train_model.py"])
    
    print("Setup completed successfully!")
    print("\nTo run the system:")
    print("1. Start API: python run_api.py")
    print("2. Start Dashboard: python run_dashboard.py")

if __name__ == "__main__":
    setup_project()