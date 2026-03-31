# FastAPI Calculator Application

## Overview
This project is a FastAPI-based calculator application that performs basic arithmetic operations such as addition, subtraction, multiplication, and division. It includes a web interface, automated testing, and continuous integration.

## Features
- Arithmetic operations: Add, Subtract, Multiply, Divide
- Input validation using Pydantic
- Error handling for invalid inputs and division by zero
- Logging for operations and errors
- Simple web interface

## Testing

### Unit Tests
All functions in the operations module are tested.

### Integration Tests
All API endpoints are tested for correct behavior.

### End-to-End Tests
Playwright is used to simulate user interaction with the application.

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/bt326/fastapi-calculator.git  
cd fastapi-calculator  

### 2. Create virtual environment
python -m venv venv  
source venv/bin/activate  

### 3. Install dependencies
pip install -r requirements.txt  

### 4. Install Playwright browsers
playwright install  

### 5. Run the application
uvicorn main:app --reload  

### 6. Open in browser
http://127.0.0.1:8000  

## Logging
Logging is implemented across the application:
- API-level logging in main.py  
- Operation-level logging in operations.py  
- Error handling logs  

## Continuous Integration
GitHub Actions is configured to automatically run all tests on each push.

## Project Structure
app/  
  operations.py  
templates/  
tests/  
  unit/  
  integration/  
  e2e/  
main.py  
requirements.txt  
.github/workflows/  

