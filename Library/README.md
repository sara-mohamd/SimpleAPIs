# Library Management API

### Simple API Course Project: Library Management API

This project involves creating a Library Management API using Python Flask and MySQL. The API manages books, authors, and borrow records. It includes features like ORM using SQLAlchemy, Swagger documentation for API endpoints, and security measures for authentication, authorization, and rate limiting. API versioning is also implemented to maintain backward compatibility.

## Objectives

1. **RESTful APIs:** Create endpoints to handle CRUD operations for books, authors, and borrow records.
2. **MySQL Integration:** Set up and manage a MySQL database to store library data.
3. **ORM with SQLAlchemy:** Interact with the MySQL database in an object-oriented manner.
4. **API Documentation:** Utilize Swagger to document the API endpoints.
5. **Security:** Add authentication, authorization, and rate limiting to secure the API.
6. **API Versioning:** Implement versioning to manage changes and maintain compatibility.

## Requirements

### 1. Endpoints

- **Books:**
  - Create a new book (admin only)
  - Retrieve details of a book
  - Update book information (admin only)
  - Delete a book (admin only)
  
- **Authors:**
  - Create a new author (admin only)
  - Retrieve details of an author
  - Update author information (admin only)
  - Delete an author (admin only)
  
- **Borrow Records:**
  - Create a new borrow record (admin only)
  - Retrieve details of a borrow record
  - Update borrow record information (admin only)
  - Delete a borrow record (admin only)
  
- **Users:**
  - Register a new user
  - Login a user
  - Get user details (authenticated users only)

### 2. Database Schema

- **Book Table:**
  - `id`: Integer, primary key
  - `title`: String, not null
  - `author_id`: Integer, foreign key (references Author.id)
  - `published_date`: Date
  - `isbn`: String, unique
  
- **Author Table:**
  - `id`: Integer, primary key
  - `name`: String, not null
  - `bio`: Text
  
- **BorrowRecord Table:**
  - `id`: Integer, primary key
  - `book_id`: Integer, foreign key (references Book.id)
  - `borrower_name`: String, not null
  - `borrow_date`: Date
  - `return_date`: Date
  
- **User Table:**
  - `id`: Integer, primary key
  - `username`: String, unique, not null
  - `password`: String, not null
  - `role`: String, not null (e.g., 'admin', 'user')
  - `token`: String
  - `request_count`: Integer, default 0
  - `last_request_time`: DateTime

### 3. Authentication and Authorization

- Implement user registration and login.
- Use custom token generation to secure endpoints.
- Protect certain endpoints to allow only authenticated users to perform actions.
- Restrict certain endpoints to admin users based on the `role` attribute.

### 4. Rate Limiting

- Limit users to 100 requests per day.
- Track the count of requests and the last request time in the User table.
- Reset the request count every 24 hours.

### 5. Swagger Documentation

- Document all endpoints with Swagger.
- Include details about request and response formats.

### 6. API Versioning

- Implement versioning (e.g., `/api/v1/`) to allow future enhancements without breaking existing clients.

## Custom Token Generation and Rate Limiting

### 1. Token Generation

- Upon successful login, generate a token.
- Store the token in the database associated with the user.

### 2. Token Validation

- For each authenticated request, validate the token by checking it against the stored token in the database.
- Ensure the token has not expired by validating the timestamp.

### 3. Rate Limiting

- Before processing a request, check the user's `request_count` and `last_request_time`.
- If the `request_count` is 100 and the `last_request_time` is within the same day, reject the request.
- If the `last_request_time` is from the previous day, reset the `request_count` to 0.
- Increment the `request_count` and update the `last_request_time` for each request.

## Milestones

### 1. Setup and Initialization

- Set up the Flask project and configure the MySQL database.
- Create the initial database schema using SQLAlchemy.

### 2. CRUD Operations

- Implement CRUD endpoints for books, authors, and borrow records.
- Test endpoints using Postman or a similar tool.

### 3. User Authentication and Token Generation

- Implement user registration and login.
- Create custom token generation and validation methods.
- Protect endpoints that require user authentication.
- Restrict specific endpoints to admin users.

### 4. Rate Limiting

- Implement rate limiting logic.
- Test rate limiting by making multiple requests.

### 5. Documentation

- Add Swagger documentation for all API endpoints.
- Ensure that all endpoints are well-documented with request and response details.

### 6. Versioning

- Implement API versioning.
- Create a versioned endpoint and test its functionality.

---

**Note:** This project is a part of the Simple API Course Project by شركة تسابق للتدريب والتطوير.
