# FastAPI

## Index
- In this file, I will use FastAPI to create a website API utilizing a deep learning model.

- This was created during the summer vacation of my second year at university.

- All of the code files will be placed in the **app** folder.

## Installation

>[!NOTE]
>Please use MacOS environment to proceed.

1. First, download the *zip* file and follow the process below:
    ```bash
    cd
    cd Downloads
    unzip fast-api-main.zip
    cd fast-api-main
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

4. Before starting the server:
    ```bash
    cd app
    cd db
    python database.py
    ```

    ```bash
    cd .. 
    ```

5. Finally, start the FastAPI server:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```


## About the **app** Folder

1. This folder contains six main components: *db*, *model*, *static*, *templates*, *main.py*, and *requirements.txt*.

2. The **db** folder contains the database settings.

3. The **model** folder contains the functions used in this website.

4. The **static** folder stores JavaScript files.

5. The **templates** folder stores HTML files.

6. The **main.py** file is the main entry point of the FastAPI application.

7. The **requirements.txt** file lists all the dependencies required to run the project.

© 2024 Jacksen. All rights reserved.