# Backend
This directory contains the backend server implementation for the bike-sharing data visualization project. It is built using FastAPI, a modern web framework for building APIs with Python.

It offers endpoints to retrieve real-time and historical data about bike stations, including their locations, available bikes, and docks.

## Setup Instructions
1. **Navigate to the backend directory:**
   ```bash
   cd src/backend
   ```
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Starting the Server
To start the backend server, run the following command in your terminal:

```bash
uvicorn main:app --reload
```
This will launch the FastAPI server with hot-reloading enabled, allowing you to see changes in real-time as you edit the code.

## API Documentation
Once the server is running, you can access the automatically generated API documentation by navigating to:
```
http://localhost:8000/docs
```
This interactive documentation provides details about the available endpoints, request/response formats, and allows you to test the API directly from your browser.

## Project structure
```src/backend/
├── main.py                       # Main application entry point
├── models/                       # Contains the model definitions for API responses
│
├── services/                     # Contains the logic for data retrieval and processing
├── routes/                       # Contains the API route definitions
```