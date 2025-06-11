from celery_config import app

@app.task
def greet(name):
    return f"Hello, {name}!"
