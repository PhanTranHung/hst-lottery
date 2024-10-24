# MongoDB Config
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

SYSTEM_HOST = os.getenv('SYSTEM_HOST', '0.0.0.0')
SYSTEM_PORT = int(os.getenv('SYSTEM_PORT', 8801))