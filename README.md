# Automated UTS Event Tracker

## Overview
A comprehensive backend service that ingests university society event data directly from the Activate UTS API, stores it in a PostgreSQL database, and serves the information about events with food to users.

## Features
* **Automated Data Ingestion:** Interfaces directly with the Activate UTS API to reliably fetch the latest society events.
* **AI Data Processing:** Integrates with the Google Gemini API to intelligently process and verify if the event has food.
* **Discord Integration:** A frontend bot interface that allows users to seamlessly browse upcoming events directly within Discord.
* **Persistent Storage:** Relational database management using PostgreSQL to track current and historical events.
* **Containerized Architecture:** Fully containerized with Docker and Docker Compose for easy deployment and cross-platform consistency.

## Tech Stack
* **Language:** Python 3
* **Infrastructure:** Docker, Docker Compose, Gemini API
* **Database:** PostgreSQL (with `psycopg`)
* **Key Libraries:** `discord.py` (or equivalent Discord wrapper), `Pydantic` (for structured outputs), `requests` (for API calls), `google-genai`

## Prerequisites
To run this project, you will need:
* **Docker** and **Docker Compose** installed on your machine or host server.
* A **Discord Bot Token** from the Discord Developer Portal.
* A **Google Gemini API Key** from Google AI Studio.

## Environment Variables
Create a `.env` file in the root directory of the project and configure the following variables:

```env
# Discord Configuration
DISCORD_TOKEN=your_discord_bot_token_here

# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# PostgreSQL Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=events_db
```

## Running the Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/FluffyDeer235/freefood.git
   cd freefood
   ```

2. **Set up your environment variables:**
   Create the `.env` file as described above.

3. **Build and start the containers:**
   Run the following command to build the images and start the database, ingestion service, and bot in the background:
   ```bash
   docker compose up -d --build
   ```

## Repository Structure

```text
freefood/
├── backend/
│   ├── main.py
│   ├── schema.py
│   ├── scrapper.py
│   ├── test_db.py
│   └── util.py
├── db_init/
│   └── init.sql
├── frontend/
│   └── bot.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── freefood_logo.png
├── README.md
└── requirements.txt
```

## Roadmap & Future Plans

This project is currently structured with a Discord bot as its primary interface, but it is built to support future expansion into multiple frontend clients. 

### Phase 1: API Gateway (Decoupling)
* **RESTful API:** Build a lightweight internal API (using FastAPI or Flask) on top of the PostgreSQL database.
* **Database Isolation:** Update the frontend clients to request data from this new API rather than querying the database directly.

### Phase 2: Web Interface
* **Event Dashboard:** Develop a responsive web application where students can filter, search, and browse society events.
* **Calendar Integration:** Add functionality to export events as `.ics` files or sync directly with Google/Apple Calendar.

### Phase 3: Notification Engine
* **Opt-In Subscriptions:** Create a background worker that allows users to subscribe to specific societies or event categories.
* **Multi-Channel Delivery:** Broadcast upcoming events via Email or push notifications.

## Contact
For any questions or suggestions:
* Contact the maintainer on Github
* Email: duytn27@gmail.com
