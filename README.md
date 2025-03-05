
# E-Grocery

## Overview
E-Grocery is a multi-user e-commerce application designed for grocery shopping. This project leverages modern web technologies to provide a responsive, reliable, and feature-rich platform. The application follows the **Model-View-Controller (MVC)** architecture and includes role-based access control, email notifications, and report generation capabilities.

### Key Features
- **Multi-User Support**: Different user roles with tailored permissions.
- **Role-Based Access Control (RBAC)**: Secure access management for admins, customers, and other roles.
- **Email Notifications**: Automated emails for order confirmations, updates, and more.
- **Report Generation**: Tools to generate insights and summaries for users.
- **Responsive Design**: Optimized for seamless use across devices.

## Tech Stack
- **Frontend**: [Vue.js](https://vuejs.org/) - A progressive JavaScript framework for building interactive UIs.
- **Backend**: [Flask](https://flask.palletsprojects.com/) - A lightweight Python web framework for the server-side logic.
- **Database**: [SQLite](https://www.sqlite.org/) - A lightweight, serverless database for data storage.
- **Task Queue**: [Celery](https://docs.celeryproject.org/) - Asynchronous task processing for background jobs.
- **Caching**: [Redis](https://redis.io/) - In-memory data store for improved performance and responsiveness.

## Architecture
The application adheres to the **MVC architecture**:
- **Model**: Manages data and business logic (SQLite, Redis).
- **View**: Handles the user interface (Vue.js).
- **Controller**: Processes user inputs and connects the Model and View (Flask).

Additionally, **Celery** and **Redis** enhance the system by:
- Offloading time-consuming tasks (e.g., email sending, report generation) to the background.
- Caching frequently accessed data for faster response times.

## Installation & Setup

### Prerequisites
- [Python 3.8+](https://www.python.org/)
- [Node.js](https://nodejs.org/) (for Vue.js)
- [Redis](https://redis.io/docs/getting-started/)
- [Git](https://git-scm.com/)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/aniket21715/grocery_app.git
   cd e-grocery
