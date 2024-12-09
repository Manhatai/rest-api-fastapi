import os 

__DB_BASE_HOST = f"{os.getenv('REST_API_DB_HOST')}:{os.getenv('REST_API_DB_PORT')}"
__DB_CREDENTIALS = f"{os.getenv('REST_API_DB_LOGIN')}:{os.getenv('REST_API_DB_PASSWORD')}"
SQLALCHEMY_DATABASE_URI = f'postgresql://{__DB_CREDENTIALS}@{__DB_BASE_HOST}/{os.getenv("REST_API_DB_NAME")}'
SECRET_KEY = os.getenv("REST_API_SECRET_KEY")