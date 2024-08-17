# FastAPI

## About This File
- In this file, I will use FastAPI to create a website API utilizing a deep learning model.

- This was created during the summer vacation of my second year at university.

- All of the code files will be placed in the **app** folder.

## Installation

>[!NOTE]
>Please use a Linux environment to proceed.

- First, download all the files and change the directory:
```bash
cd
mkdir fastapi
cd app
```

- After that create a python virtual environment and activate it
```
python -m venv fastapivenv
```

```
source fastapivenv/bin/activate
```

- Then, install the required packages:
```
pip install -r requirements
```

-  Finally, start the FastAPI server:
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
