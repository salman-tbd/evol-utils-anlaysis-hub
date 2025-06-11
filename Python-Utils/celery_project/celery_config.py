from celery import Celery
from dotenv import load_dotenv
import os

# Load environment variables for Celery process
env_path = os.path.join(os.path.dirname(__file__), '..', 'config.env')
load_dotenv(dotenv_path=env_path)

app = Celery(
    'my_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['email_tasks']  # now using email task
)
