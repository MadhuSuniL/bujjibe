# Bujji's Cosmic Insights Backend System

This project is centered around creating a robust backend system using the **Django** framework and **Django Channels**, designed to power **Bujji's Cosmic Insights**—a dynamic chat platform focused on space and the universe.

## Getting Started

Follow these instructions to set up and run the Django server locally.

### Prerequisites

Ensure you have the following installed:

- **Python**: [Download Python](https://www.python.org/downloads/) (v3.7+ recommended)
- **pip**: Package installer for Python
- **Redis**: A message broker required for Django Channels

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/MadhuSuniL/bujjibe.git
   ```
2. **Navigate to the project directory**:

   ```bash
   cd bujjibe
   ```
3. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
5. **Install Django Channels**:

   You must install Django Channels using the following command to ensure the built-in `runserver` command will run the server as ASGI:

   ```bash
   python -m pip install -U 'channels[daphne]'
   ```
6. **Install Redis**:

   - **Windows**: Follow the instructions from [this link](https://github.com/tporadowski/redis/releases) to download and install Redis on Windows.
   - **Linux and macOS**: You can install Redis using your package manager. For example, on Ubuntu:

     ```bash
     sudo apt update
     sudo apt install redis-server
     ```

   For other distributions and OS, follow the respective Redis installation methods.

### Running the Server

Once you have installed the required dependencies and Redis:

1. **Run Redis** (if not already running):

   ```bash
   redis-server
   ```
2. **Run Django development server**:

   ```bash
   python manage.py runserver
   ```

### WebSocket URL for Real-Time Chat

The WebSocket connection for real-time chat can be established using the following WebSocket URL:

```bash
ws://localhost:8000/ws/chat?token={{token}}
```

- **token**: Replace `{{token}}` with a valid JWT (JSON Web Token) or session token obtained after user authentication.
- This token is required to authenticate the user and establish a secure WebSocket connection.

This WebSocket endpoint allows users to engage in real-time chat within the application.
