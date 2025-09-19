import urllib.request
import zipfile
import os

def download_movielens():
    """Download and extract MovieLens 100K dataset"""
    url = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
    zip_path = "data/raw/ml-100k.zip"
    
    # Create directories
    os.makedirs("data/raw", exist_ok=True)
    
    # Download
    print("Downloading MovieLens dataset...")
    try:
        urllib.request.urlretrieve(url, zip_path)
        print("Download completed!")
    except Exception as e:
        print(f"Download failed: {e}")
        return False
    
    # Extract
    print("Extracting dataset...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("data/raw/")
        print("Dataset downloaded and extracted successfully!")
        
        # Clean up zip file
        os.remove(zip_path)
        print("Cleanup completed!")
        return True
    except Exception as e:
        print(f"Extraction failed: {e}")
        return False

if __name__ == "__main__":
    success = download_movielens()
    if success:
        print("\n✅ Dataset ready! Next step: python train_model.py")
    else:
        print("\n❌ Dataset download failed. Please try again.")