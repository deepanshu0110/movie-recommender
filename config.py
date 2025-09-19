import os

class Config:
    # Data paths
    RAW_DATA_PATH = "data/raw/ml-100k"
    PROCESSED_DATA_PATH = "data/processed"
    MODELS_PATH = "models"
    
    # API settings
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # Model settings
    DEFAULT_N_RECOMMENDATIONS = 10
    MIN_RATINGS_PER_USER = 5
    MIN_RATINGS_PER_MOVIE = 5
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        directories = [
            cls.RAW_DATA_PATH,
            cls.PROCESSED_DATA_PATH,
            cls.MODELS_PATH
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)