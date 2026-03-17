BOLTTRIP

"Where journeys begin with just one click!"
A Django-based web application to manage travel packages, bookings, and more.

🚀 Quick Start (Single Terminal)
# Clone the repo
git clone <https://github.com/ahmadsaif12/BoltTrip.git> && cd <bolttrip>

# Create virtual env
python -m venv venv && source venv/bin/activate  # Linux
python -m venv venv && venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

# Build and start containers
docker-compose up --build
docker-compose exec web python manage.py migrate

🛠 Tech Stack

Backend: Django (Python)
Frontend: HTML, CSS
Database: MySQL / PostgreSQL (via Docker)
Containerization: Docker & Docker Compose

✨ Features

🧳 Travel package management
🏨 Hotel booking system
💰 Expense tracking
👤 User & admin dashboards
📍 Location-based features

👥 Contributors
@ahmadsaif12

📌 Notes

Ensure .env file is configured (DB credentials, secret key, etc.)
Default app runs on: http://127.0.0.1:8000/
