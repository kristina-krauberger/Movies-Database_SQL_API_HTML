"""
Generate a static HTML page for the Movie app.

This module reads movie data, renders per-movie HTML snippets, replaces
placeholders in the template, and writes the final page to
`_static/index.html`.
"""

from movie_storage_sql import list_movies

HOMEPAGE_TITLE = "MY MOVIE APP"

def replace_template_placeholder(template, placeholder, replaced_text):
    """
    Replace a single placeholder in a template string.
    :param template: The original template HTML/text.
    :param placeholder: The placeholder token to replace (e.g., "__FOO__").
    :param replaced_text: The text that should replace the placeholder.
    :return: The updated template with the placeholder replaced.
    """
    return template.replace(placeholder, replaced_text)


def load_html_template(file_name):
    """
    Loads and returns the contents of an HTML template file.
    :param file_name: The path to the HTML template file to load.
    :return: The contents of the HTML template file as a string.
    """
    with open(file_name, "r", encoding="utf-8") as fileobj:
        return fileobj.read()


def serialize_one_movie(title, data):
    """
    Serialize a single movie into an HTML list item.
    :param title: Movie title.
    :param data: Dictionary with at least keys "year" and "poster_image_url".
    :return: An HTML `<li>` snippet representing the movie.
    """
    output = "<li>"
    output += "<div class='movie'>"
    output += (f"<img class='movie-poster' src='{data.get('poster_image_url', '--')}' "
               f"alt= 'Poster image not available.'/>")
    output += f"<div class='movie-title'>{title}</div>"
    output += f"<div class='movie-year'>{data.get('year')}</div>"
    output += "</div>"
    output += "</li>"
    return output


def show_all_movies(movies_data):
    """
    Serialize all movies into one HTML block.
    :param movies_data: Mapping of title to movie data dictionaries.
    :return: Concatenated `<li>` snippets for all movies.
    """
    output = ""
    for title, data in movies_data.items():
        output += serialize_one_movie(title, data)
    return output


def safe_to_file(text, file_name):
    """
    Write text to a file using UTF-8 encoding.
    :param text: The content to write.
    :param file_name: Output file path.
    :return: None
    """
    with open(file_name, "w", encoding="utf-8") as fileobj:
        fileobj.write(text)


def main():
    """
    Build and write the final HTML page.
    Reads movie data, fills the template placeholders, and writes the
    rendered page to the output path.
    """
    movies_data = list_movies()
    movie_info = show_all_movies(movies_data)
    html = load_html_template("_static/index_template.html")
    html_with_title = replace_template_placeholder(html,"__TEMPLATE_TITLE__", HOMEPAGE_TITLE)
    final_html = replace_template_placeholder(html_with_title, "__TEMPLATE_MOVIE_GRID__", movie_info)
    safe_to_file(final_html, "_static/index.html")
    print("Website was successfully generated.")

if __name__ == "__main__":
    main()