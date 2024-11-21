# PulseSMS ⚡ - Google Messages API: Seamlessly Send & Manage Messages at Scale 🚀 

A FastAPI-based service that enables programmatic interaction with Google Messages Web, allowing automated message sending and management through a REST API and WebSocket interface.

## 🌟 Features

- WebSocket-based QR code authentication
- REST API for sending messages
- Celery-based asynchronous message processing
- Selenium-powered browser automation
- Session persistence and credential management
- Docker containerization with multi-service architecture
- Real-time message status tracking
- Scalable worker configuration

## 🏗️ Architecture

The application is built using:
- FastAPI for the REST API and WebSocket server
- Selenium for browser automation
- Celery for asynchronous task processing
- Redis for message queuing
- Docker for containerization
- Flower for task monitoring

## 🚧 Roadmap
- [✅] Add support for sending messages to contacts
- [✅] WebSocket authentication
- [✅] Celery integration
- [✅] Docker containerization
- [✅] Flower dashboard
- [ ] Sending concurrent messages

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Redis server
- Firefox browser (for Selenium)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gmessages-server
```

2. Create a virtual environment (optional):
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```


### 🐳 Docker Deployment

1. Build and start the services:
```bash
docker compose up -d --build
```

This will start:
- Selenium standalone Firefox server
- FastAPI application
- Celery workers
- Redis server
- Flower dashboard

## 🔧 Configuration

Environment variables can be configured in `docker-compose.yaml`:

- `SELENIUM_HOST`: Selenium server host
- `SELENIUM_PORT`: Selenium server port
- `HEADLESS`: Run browser in headless mode
- `DEBUG`: Enable debug mode
- `CELERY_BROKER_URL`: Redis broker URL
- `CELERY_RESULT_BACKEND`: Redis result backend URL

## 📡 API Endpoints

### WebSocket Authentication
`ws://localhost:8000/ws/auth`

### Send Message
`POST http://localhost:8000/api/messages/send`
```json
{
    "to": "1234567890",
    "message": "Hello, world!"
}
```

### Check Message Status
`GET http://localhost:8000/api/messages/task/{task_id}`



## 🔍 Monitoring

Access the Flower dashboard for task monitoring:
`http://localhost:5555`


## 📝 Logging

The application uses structured logging with emoji indicators:
- 📁 File name
- 📍 Line number
- ⚡️ Function name
- 🔄 Status updates
- ❌ Errors
- ✅ Success

## 🛡️ Security

- Credentials are stored securely in `credentials.json`
- Session persistence for authenticated sessions
- Automatic cleanup of browser sessions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.