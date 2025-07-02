### Setup and Running Instructions

Follow these steps to set up your environment, fetch the data, and store it.

#### 1\. Create and Activate a Python Virtual Environment

```bash
# Navigate to your project directory
cd this_proyect/

# Create a virtual environment named '.venv'
python3 -m venv env
```

Your terminal prompt should now show `(env)` indicating the virtual environment is active.

#### 2\. Install Required Libraries

Install the `requests` library, which is used for making HTTP requests to fetch data from APIs.

```bash
pip install requests
```

#### 3\. Run the Data Fetching Script

Execute the `fetch.py` script to retrieve the data.

```bash
python fetch.py
```

#### 4\. Access the Fetched Data

Upon successful execution, the fetched raw data will be stored in a new folder named `raw/` within your project directory.
