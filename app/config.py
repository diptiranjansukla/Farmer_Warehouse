import os

class Config:
    # Check if we are running in GitHub Actions
    if os.getenv('GITHUB_ACTIONS'):
        SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Sukla%40123@127.0.0.1:3306/farmer_warehouse_db'
    else:
        # Local development configuration
        SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Sukla%40123@localhost/farmer_warehouse_db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 1800,
    }
