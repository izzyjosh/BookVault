# Library Management System (LMS)

This Library Management System is designed to automate and streamline the operations of a library, providing a user-friendly interface for managing books, users, and library transactions.

---

## Features

- [x] **User Management**
  - [x] User Registration
  - [x] Login/Logout with Role-based Access Control (Admin, Librarian, Member)
  - [x] Profile Management (Update personal information, borrowing history)
  - [x] Role-based Access Control (RBAC)

- [ ] **Book Management**
  - [x] Add/Update/Delete Books
  - [x] Book Search (Title, Author, Genre, ISBN)
  - [x] Book Details (Author, Publisher, Year, Genre)
  - [x] Category Management (Organize books by category)
  - [ ] ISBN Validation

- [ ] **Inventory and Catalog Management**
  - [ ] Inventory Tracking (Track number of copies)
  - [ ] Book Status (Available, Checked Out, Reserved)
  - [ ] Barcode/QR Code Generation

- [ ] **Borrowing and Returning Books**
  - [ ] Borrow Books (Limit based on user role)
  - [ ] Return Books
  - [ ] Due Date Management
  - [ ] Renewal
  - [ ] Late Fee Calculations

- [ ] **Reservation System**
  - [ ] Book Reservation (Reserve books currently checked out)
  - [ ] Reservation Queue
  - [ ] Notification for Availability

- [ ] **Fines and Fees Management**
  - [ ] Automatic Late Fee Calculation
  - [ ] Fine Payment Tracking
  - [ ] Waive/Adjust Fines

- [ ] **Notifications**
  - [ ] Email/SMS Notifications (Due dates, reservations, new books)
  - [ ] Overdue Reminders
  - [ ] Library Event Notifications

- [ ] **Reporting and Analytics**
  - [ ] User Activity Reports (Borrowing history, overdue books)
  - [ ] Book Popularity Reports
  - [ ] Fine Collection Summary
  - [ ] Inventory Reports

- [ ] **Search and Filtering**
  - [ ] Advanced Search (Filters by title, author, genre, etc.)
  - [ ] Book Filtering by Availability, Category
  - [ ] Sorting by Title, Popularity, Author

- [ ] **Digital Library Features (Optional)**
  - [ ] E-Books Integration
  - [ ] Download or Read Digital Materials
  - [ ] Digital Content Management

- [ ] **Admin and Librarian Features**
  - [ ] Admin Dashboard
  - [ ] User Management (Add, update, or remove users)
  - [ ] Book Inventory Management
  - [ ] Transaction Logs (View borrowing/return history)
  - [ ] System Configuration

- [ ] **Security Features**
  - [ ] Role-based Authentication
  - [ ] Data Encryption for Sensitive Information
  - [ ] Audit Trail for Transactions

- [ ] **Backup and Restore**
  - [ ] Regular Data Backup
  - [ ] Restore System from Backup

- [ ] **Library Events and News**
  - [ ] Event Management (Workshops, author meet-and-greets)
  - [ ] Announcements (New books, events)

- [ ] **Multi-Branch Library Support (Optional)**
  - [ ] Branch Management
  - [ ] Inter-branch Book Transfer

- [ ] **Audit and History Tracking**
  - [ ] Transaction History for Users
  - [ ] Book History Tracking (Borrowing, reservations)

--- 

## Optional Features
- [ ] **Mobile App Integration**
  - [ ] Mobile Search and Account Management
- [ ] **Self-Checkout Kiosk Integration**
- [ ] **Third-Party API Integration (e.g., Google Books API)**
- [ ] **Recommendation System Based on User Borrowing History**

---

## Technologies to be Used

### Backend
- **FastAPI**: For building a high-performance, asynchronous API backend.
- **PostgreSQL**: Relational database for managing library data.
- **SQLAlchemy**: ORM for database interactions (alternatively, **Tortoise ORM**).
- **Pydantic**: Data validation and settings management.
- **Alembic**: Database migrations.
- **WebSockets**: Real-time features (2-way).
- **SSE**: Real-time features (1-way).
- **OAuth2 + JWT**: For secure user authentication and role-based access control.
- **Redis** (Optional): For caching data to improve system performance.
  
### Frontend
- **React.js** or **Vue.js**: To build a responsive web interface.
- **HTML/CSS** (with **TailwindCSS**): For styling the frontend interface.

### API Documentation
- **Swagger**: Automatically generated API documentation via FastAPI.

### Testing
- **Pytest**: For unit testing and integration testing of the API.
- **FastAPI TestClient**: For testing API endpoints.

### Deployment
- **Docker**: To containerize the application for consistent deployment across environments.
- **GitHub Actions**: For Continuous Integration (CI) and Continuous Deployment (CD) automation.

### Security
- **HTTPS**: Secure communication between client and server.
- **JWT (JSON Web Tokens)**: For secure user authentication.

### Optional
- **Celery**: For handling background tasks such as sending email notifications.
- **RabbitMQ/Kafka**: For message queues in a microservices architecture.

---

## Optional Technologies

### Mobile App (Optional)
- **React Native**: To build a cross-platform mobile app for the library system.

### Message Broker (Optional)
- **RabbitMQ** or **Kafka**: For managing asynchronous tasks and messages across services.

### Monitoring and Logging
- **Prometheus + Grafana**: For real-time monitoring and visualizing system performance.
- **ELK Stack (Elasticsearch, Logstash, Kibana)**: For centralized logging and analysis.

---


## Starting the project
---

Follow the steps below to get the project up and running          
```shell
cd BookVault/
copy .env.sample .env
```

At this point, you should update the values in the created .env file
Now, let's setup our environment

```shell
pip -m venv venv # create virtual environment
pip install -r requirements.txt # install dependencies
```
Everything should run successfully. Next is to setup our database.

```shell
# create postgresql database
CREATE DATABASE fastapi-social-media-api;
# let's make migrations to our database
alembic upgrade head
```

We are now set up. Now, let's start our project server

```shell
python3 main.py
```
<br />
<br />

## Testing
---
To run your tests using `pytest`, follow the steps below
```shell
pytest --disable-warnings -vv -s api/v1/tests
```
