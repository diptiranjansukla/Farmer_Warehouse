class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Sukla%40123@localhost/farmer_warehouse_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 1800,
    }