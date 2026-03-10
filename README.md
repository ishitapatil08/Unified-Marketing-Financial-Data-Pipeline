# Integrated Financial & Marketing Intelligence Platform

This project consists of a Python backend (FastAPI + DuckDB) and a React frontend (Vite + Chart.js).

## Prerequisites
- Python 3.8+
- Node.js & npm
- Git

---

## 🚀 How to Push to GitHub

To upload this project to your GitHub repository, follow these steps in your terminal:

**Step 1: Initialize Git and Add Files**
Open a terminal in the root of your project (`intelligence_platform`) and run:
```bash
git init
git add .
git commit -m "Initial commit: Integrated Intelligence Platform setup"
```

**Step 2: Link to your GitHub Repository**
Create a new, empty repository on GitHub. Then, run the following commands (replace `<YOUR_USERNAME>` and `<YOUR_REPO_NAME>` with your actual details):
```bash
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git
```

**Step 3: Push the Code**
```bash
git push -u origin main
```

*(Note: Ensure you have a `.gitignore` file to prevent uploading large folders like `node_modules/` or `venv/`)*

---

## 1. Setting up the Backend (Python)

The backend handles the data generation, ETL pipeline, DuckDB data warehouse, anomaly detection, report generation, and the FastAPI REST interface.

**Step 1: Navigate to the backend directory**
```bash
cd backend
```

**Step 2: Create a virtual environment (Optional but Recommended)**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

**Step 3: Install Requirements**
Download and install all required Python packages:
```bash
pip install -r requirements.txt
```

**Step 4: Run the Data Pipeline**
Generate the mock data, process it, load it into the warehouse, run anomaly detection, and generate a PDF report:
```bash
python src/data_generator.py
python src/etl_pipeline.py
python src/data_warehouse.py
python -m src.anomaly_detection
python -m src.report_generator
```

**Step 5: Start the API Server**
Start the FastAPI server that serves data to the frontend:
```bash
python -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```
*The API will be running at http://127.0.0.1:8000*

---

## 2. Setting up the Frontend (React / Vite)

The frontend is a modern, glassmorphic React dashboard displaying the KPIs.

**Step 1: Open a NEW terminal window and navigate to the frontend directory**
```bash
cd frontend
```

**Step 2: Install Node Dependencies**
Download and install all required JS packages (React, Chart.js, etc.). Make sure to include the Vite dev dependencies required to run the server:
```bash
npm install
npm install --save-dev vite @vitejs/plugin-react
```

**Step 3: Start the Development Server**
```bash
npm run dev
```
*The Dashboard will be running at http://127.0.0.1:5173*
