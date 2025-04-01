# Outfast
Website which delivers clothes in under 15mins
# Flask App Setup Guide

This guide explains how to set up and run a Flask application using a `requirements.txt` file.

---

## Prerequisites

Ensure you have Python installed (preferably Python 3.8+). Check using:

```bash
python --version
```

or  

```bash
python3 --version
```

If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/).

---

## 1. Create a Virtual Environment (Recommended)

Navigate to your project directory and create a virtual environment:

```bash
cd /path/to/your/project
python -m venv venv
```

Activate the virtual environment:

- **Windows (Command Prompt)**  
  ```bash
  venv\Scripts\activate
  ```
- **Windows (PowerShell)**  
  ```powershell
  venv\Scripts\Activate.ps1
  ```
- **Mac/Linux**  
  ```bash
  source venv/bin/activate
  ```

---

## 2. Install Dependencies

Once the virtual environment is active, install all required dependencies:

```bash
pip install -r requirements.txt
```



## 4. Run the Flask App

Start the Flask development server:

```bash
python app.py
```

## 5. Access the App

Once running, open your browser and visit:

```
http://127.0.0.1:5000/
```

---

## 6. Deactivating Virtual Environment

When you're done, deactivate the virtual environment:

```bash
deactivate
```

---

## 7. Additional Information

- Ensure `requirements.txt` is up to date by running:
  ```bash
  pip freeze > requirements.txt
  ```
- To install additional dependencies, use:
  ```bash
  pip install package_name
  ```

---

## 8. License

This project is licensed under the MIT License.

---

## 9. Author

Created by Varad Rane
