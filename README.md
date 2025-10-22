#  Modeling Platform – Part 1: Environment Setup & File Upload Engine

##  Overview
This is *Part 1* of the Modeling Platform project — a modular system for managing and processing uploaded files in a data modeling environment.

The focus of this stage is on *setting up the environment, **building the file upload engine, and **configuring the database* using Streamlit and SQLAlchemy.

---

##  Features (Part 1)

✅ Initialized Python project and Git repository  
✅ Created .env configuration file for environment settings  
✅ Built Streamlit upload interface for CSV/XLSX files  
✅ Saved uploaded files with *timestamped filenames* in app/uploads/  
✅ Created UploadedFile table using *SQLAlchemy + SQLite*  
✅ Implemented clean project structure for scalability  

---

##  Tech Stack

| Component | Technology |
|------------|-------------|
| *Frontend (UI)* | Streamlit |
| *Backend ORM* | SQLAlchemy |
| *Database* | SQLite |
| *Environment Config* | python-dotenv |
| *Data Handling* | Pandas, OpenPyXL, PyArrow |
| *Python Version* | 3.12+ |

---

##  Setup Instructions

###  Clone the repository
bash
git clone https://github.com/<your-username>/modeling-platform.git
cd modeling-platform



### create and activate virtual environment.
python -m venv .venv
source .venv/bin/activate      # Linux / WSL
# or
.venv\Scripts\activate         # Windows

### Install dependencies
pip install -r requirements.txt

### run the streamlit app.
streamlit run run.py
