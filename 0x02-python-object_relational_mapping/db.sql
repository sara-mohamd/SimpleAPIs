CREATE DATABASE IF NOT EXISTS EmployeeManagement;
USE EmployeeManagement;

CREATE TABLE Employees (
  id INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(255) NOT NULL,
  Gender VARCHAR(10) NOT NULL,
  Salary DECIMAL(10, 2) NOT NULL
);