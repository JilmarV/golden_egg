# 🥚 Golden_Egg - ERP Lite for Poultry Companies

*Golden_Egg* is a Lite ERP system developed to digitize and optimize key processes of a poultry company dedicated to the commercialization and distribution of eggs. It is built with a microservices architecture using FastAPI for the backend and Angular for the frontend, deployed with Docker containers and CI/CD through GitHub Actions.


## 🚀 General Objective

Develop a Lite ERP system with a microservices architecture in Python (FastAPI) that allows for comprehensive management of business processes such as: customers, inventory, billing, users, and financial reports.


## 🎯 Specific Objectives

- Manage users with authentication and role control (admin, employee).
- Control egg inventory by supplier, including entries and exits.
- Manage orders, invoicing, and payments.
- Automatically generate financial reports.
- Provide a modern and responsive web interface using Angular.


## ⚙️ Technologies Used

| Technology       | Description                                |
|------------------|---------------------------------------------|
| FastAPI          | RESTful Backend                            |
| Angular          | Modern Frontend                            |
| MySQL            | Relational Database                        |
| Docker           | Containers and Orchestration               |
| GitHub Actions   | Continuous Integration and Deployment (CI/CD) |
| JWT              | Secure Authentication                     |


## 🧱 System Architecture

The system is divided into the following microservices:

- *Authentication Service*
- *Customer and Order Service*
- *Product and Inventory Service*
- *Payments and Billing Service*
- *Reports Service*
- *Angular Frontend* (Deployed independently)


## 🧪 Testing

- Tests conducted with *Postman*.
- Collections organized by microservice.
- Endpoint validation: login, create order, check stock, etc.


## 🔐 Security

- Authentication using *JWT*.
- Role-based access control (admin, employee) enforced on both backend and frontend.


## 📦 Deployment

- Orchestration with *Docker Compose*.
- CI/CD with *GitHub Actions*.
- Backend and frontend deployed as independent services.


## 📈 Development Methodology

*SCRUM* was used as the agile methodology:

- Weekly sprints.
- Daily standups, planning, review, and retrospective meetings.
- Task management with *Trello*.
- User stories prioritized in the product backlog.


## 🧑‍💻 Development Team

| Role              | Full Name                   |
|------------------|------------------------------|
| Backend           | Joan Sebastián Sosa Bedoya  |
| DevOps            | Jilmar Said Veloza          |
| DBA               | Pablo Garcés                |
| QA                | Juan Diego Rojas            |
| Frontend          | Esteban Pineda              |
| Analyst           | Felipe López                |


## 📂 System Diagrams

Included in the /docs folder:

- UML Class Diagram.
- Main Use Case Diagram.
- Individual Use Cases: Login, Register, Create Order, Generate Report, Make Payment.
