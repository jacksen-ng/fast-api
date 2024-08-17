# FastAPI

## About This File
- In this file, I will use FastAPI to create a website API utilizing a deep learning model.

- This was created during the summer vacation of my second year at university.

- All of the code files will be placed in the **app** folder.

## Installation

>[!NOTE]
>Please use a Linux environment to proceed.

1. First, download the **app** folder and follow the process below:
    ```bash
    cd
    mkdir fastapi
    mv ~/Downloads/app ~/fastapi/app
    cd fastapi/app
    ```

2. Create a Python virtual environment and activate it:
    ```bash
    python -m venv fastapivenv
    ```

    ```bash
    source fastapivenv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Finally, start the FastAPI server:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```


## About **app** folder

