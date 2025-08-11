# Database connection URL (relative SQLite file in the project root)
DB_URL = "sqlite:///data/movies.db"

# Website generation settings
HOMEPAGE_TITLE = "MY MOVIE APP"
TEMPLATE_PATH = "static/index_template.html"  # was _static/
OUTPUT_PATH = "static/index.html"
PH_TITLE = "__TEMPLATE_TITLE__"
PH_MOVIE_GRID = "__TEMPLATE_MOVIE_GRID__"