# Time Traveler's Diary 🕰️

A Django-based web application that allows time travelers to document their journeys across different eras and dimensions. Keep track of the adventures, encounters, and discoveries throughout spacetime!

## Features

- 📝 Create, view, edit, and delete diary entries
- 🗺️ Log visited time periods and dimensions
- 👥 Document encounters with historical figures
- 🏺 Record discovered artifacts and their significance
- 🔍 Search and filter entries by era, location, or keywords
- 🔐 Secure authentication system for time travelers

## Prerequisites

- Python 3.10
- pip (Python package manager)
- conda (Python virtual environment manager)
- Git

## Installation

1. Clone the repository

```bash
git clone 
cd 
```

2. Install Anaconda or Miniconda

- Download and install either Anaconda or Miniconda
- Anaconda (full version): https://www.anaconda.com/download
- Miniconda (lightweight version): https://docs.conda.io/en/latest/miniconda.html

3. Verify Conda Installation
   Open a anaconda prompt  run:

```bash
conda --version
```

This should display the installed conda version.

4. Create a New Conda Environment
   Create a new environment with Python 3.10:

```bash
conda create -n timetravel python=3.10
```

Replace `timetravel` with any name you prefer for your environment.

5. Activate the Environment

```bash
conda activate timetravel
```

6. Install dependencies

```bash
pip install -r requirements.txt
```

7. Initialize the database

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (admin account)

```bash
python manage.py createsuperuser
```

6. Update the achievements

```bash
python seed_acheivements.py
```

## Running the Application

1. Start the development server

```bash
python manage.py runserver
```

2. Open browser and navigate to `http://localhost:8000`

### Code Style

This project follows PEP 8 guidelines. 

- Format the code using:

```bash
black .
```

- Lint the code using

```bash
ruff --check .
```
## License

This project is licensed under the MIT License - see the LICENSE file for details.
