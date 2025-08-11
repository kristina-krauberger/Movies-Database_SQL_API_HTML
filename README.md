# Movies 3  SQL, API & HTML

##  Project Description
Movies 3  SQL, API & HTML is a Python application for managing a movie database. 
It retrieves movie data from both a local SQLite database and the OMDB API, and generates an HTML website displaying movie information.

##  Features
-  Display all movies
-  Add new movies
-  Delete movies
-  Load and save data in a local SQLite database
-  Fetch movie data from the OMDB API
-  Generate an HTML page with a movie overview (poster, title, year)

##  Project Structure
```plaintext
Movies 3 - SQL, API & HTML/

├── config/                        # Configuration files
│   ├── init.py
│   └── settings.py
│
├── data/                          # Data files and API client
│   ├── init.py
│   ├── movies.db
│   └── ombd_client.py
│
├── static/                        # Static website assets
│   ├── index.html
│   ├── index_template.html
│   └── style.css
│
├── storage/                       # Data storage logic
│   ├── init.py
│   └── movie_storage_sql.py
│
├── tests/                         # Test files
│   └── test_storage_sql.py
│
├── main.py                        # Main program entry point
├── requirements.txt               # Python dependencies
├── website_generator.py            # HTML website generator
└── README.md                       # Project documentation
```

##  Requirements
- Python 3.10 or higher
- pip (Python package installer)
- Dependencies listed in `requirements.txt`

##  Installation
1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/movies-sql-api-html.git
cd movies-sql-api-html
```
2. **Create a virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate    # Windows
```
3. **Install dependencies:**
```bash
pip install -r requirements.txt
```
4. **Set up environment variables:**
Create a `.env` file in the `config` folder with:
```env
OMDB_API_KEY=your_api_key_here
```

##  Usage
Run the program:
```bash
python main.py
```
Follow the menu prompts to:
- View all movies
- Add a new movie (from OMDB API or manually)
- Delete movies
- Generate an HTML page with movie details

##  License
This project is licensed under the MIT License.
