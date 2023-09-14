# Lotto

This application is written in Python 3. Ensure you have Python 3 installed to use this app.

## Dependencies
To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```
## Configuration
Before running the application, make sure to set the BASE_DIR and USER_DATA_DIR variable in the .env file.

## Building and Running
To build and run the application, follow these steps:

1. Build the .exe File
Use PyInstaller to create an executable (.exe) file for the application:
```bash
cd src
pyinstaller lotto_ui.py
```

2. Run the Application
You can run the application in one of two ways:

a. Using the .exe File
After building the executable, navigate to the dist/ui directory and execute ui.exe:
```bash
cd src/dist/lotto_ui
```
double click on `lotto_ui.exe`

b. Running the Python Script
Alternatively, you can run the application using the Python script directly:
```bash
python src/lotto_ui.py
```

