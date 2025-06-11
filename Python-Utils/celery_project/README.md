# 📨 Celery Email Task Project

A Python project using **Celery** for background email processing with **Brevo (Sendinblue)** and **Redis in Docker**.

## 🚀 Features

- **Asynchronous Email Sending**: Background email processing without blocking
- **Docker Redis Integration**: Redis running in Docker container
- **Brevo API Integration**: Professional email delivery service
- **Environment Configuration**: Secure credential management
- **Task Result Tracking**: JSON-serializable results for monitoring

## 📋 Prerequisites

- Python 3.7+
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Brevo (Sendinblue)](https://app.brevo.com/) account with API key

## 🛠 Installation & Setup

### 1. Start Redis in Docker

```bash
docker run -d --name redis-server -p 6379:6379 redis
```

### 2. Install Python Dependencies

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install celery redis python-dotenv sib-api-v3-sdk
```

### 3. Configure Environment Variables

Create `config.env` in the parent directory (`Python-Utils/`):

```env
BREVO_API_KEY=your_actual_api_key_here
SENDER_EMAIL=your.email@domain.com
SENDER_NAME=Your Name
```

## 📁 Project Structure

```
celery_project/
├── README.md              # This documentation
├── celery_config.py       # Celery application configuration
├── email_tasks.py         # Email-related Celery tasks
├── tasks.py              # General purpose tasks
├── send_test_email.py    # Test script
└── run_task.py           # Task execution script
```

## 🐳 Docker Integration

### Why Docker for Redis?

- **Cross-platform compatibility**: Works on Windows, macOS, and Linux
- **Quick setup**: Single command deployment
- **Production-like environment**: Mirrors real-world deployments
- **Easy management**: Start/stop/restart with simple commands

### Redis Management Commands

```bash
# Container management
docker stop redis-server     # Stop Redis
docker start redis-server    # Start Redis
docker restart redis-server  # Restart Redis
docker rm redis-server       # Remove container

# Monitor Redis
docker logs redis-server     # View logs
docker exec -it redis-server redis-cli  # Access Redis CLI
```

## 🚀 Usage

### 1. Start Celery Worker

```bash
celery -A celery_config worker --loglevel=info --pool=solo
```

### 2. Send Test Email

```bash
python send_test_email.py
```

### 3. Programmatic Usage

```python
from email_tasks import send_email_task

# Send email asynchronously
result = send_email_task.delay(
    recipient_email="recipient@example.com",
    subject="Test Subject",
    html_content="<h1>Hello World!</h1>"
)

# Get result with timeout
task_result = result.get(timeout=30)
print(f"Email status: {task_result}")
```

## 📊 Monitoring

### Basic Monitoring

```bash
# View active tasks
celery -A celery_config inspect active

# Monitor task events
celery -A celery_config events

# Check worker status
celery -A celery_config inspect stats
```

### Web Monitoring with Flower

```bash
pip install flower
celery -A celery_config flower
```

Access at: http://localhost:5555

## 🔧 Configuration

### Redis Configuration

Default settings in `celery_config.py`:

```python
app = Celery(
    'my_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['email_tasks']
)
```

### Environment Variables

Required in `config.env`:
- `BREVO_API_KEY`: Your Brevo API key
- `SENDER_EMAIL`: Verified sender email address
- `SENDER_NAME`: Display name for emails

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Redis connection failed | Ensure Docker container is running |
| API key not found | Check `config.env` file exists and has correct variables |
| Task not executing | Verify Celery worker is running and task is imported |
| Email sending fails | Confirm Brevo API key is valid and sender email is verified |

## 🔮 Future Enhancements

- [ ] Email templates
- [ ] Retry mechanisms
- [ ] Task scheduling
- [ ] Email analytics
- [ ] REST API integration
- [ ] Docker Compose deployment

## 📚 Resources

- [Celery Documentation](https://docs.celeryq.dev/)
- [Redis Documentation](https://redis.io/docs/)
- [Brevo API Documentation](https://developers.brevo.com/)

## 📝 License

This project is for educational and development purposes.