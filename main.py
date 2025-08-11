"""
Main entry point and CLI for the Movie database app.
Provides a text-based menu to list, add, delete, update and search movies,
show basic statistics, and generate a static website from the stored data.
"""

import random
import statistics
from ombd_client import fetch_movie_data
import movie_storage_sql as storage
from datetime import datetime
from website_generator import main as generate_website

MIN_YEAR = 1895
CURRENT_YEAR = datetime.now().year
RUN_PROGRAM = True

MENU_OPTIONS = [
    "Exit",
    "List movies",
    "Add movie",
    "Delete movie",
    "Update movie",
    "Stats",
    "Random movie",
    "Search movie",
    "Movies sorted by rating",
    "Generate website"
]


def command_menu_listing(menu_options):
    """
    Display the menu with all available options and return it as a formatted string.
    :param menu_options: List of menu option labels.
    :return: The formatted menu body as a single string.
    """
    print("\n *********** WELCOME TO MY FILM DATABASE *********** \n")

    menu_body = ""
    print("MENU:")
    for index, options in enumerate(menu_options):
        menu_body += f"{index}. {options} \n"
    return menu_body


def command_list_movies():
    """
    Print all movies stored in the database along with their details.
    :return: None
    """
    movies_data = get_movie_data()

    if not movies_data:
        print("⚠️ No movies in the database to list.")
        return

    print("")
    print(f"*********** {len(movies_data)} MOVIES IN TOTAL ***********\n")

    for title, stats in movies_data.items():
        print(title)
        print(f"Title: {title} \nRating: {stats['rating']} \nYear: {stats['year']}")
        print("")


def command_add_movie():
    """
    Prompt the user to add a new movie (title, year, rating) and save it to storage.
    :return: None
    """
    print("\n *********** ADD MOVIE *********** \n")

    # Keep asking for movie title until input is valid or user quits
    while True:
        input_new_film = input("Enter new movie name: ").strip()
        result = fetch_movie_data(title=input_new_film)
        if result is None:
            return
        year, rating, poster_image_url, title = result

        movies_data = get_movie_data()
        print(f"Test: {movies_data}")
        print(f"Test title: {title}")
        print(f"Test result: {result}")

        if movies_data:
            if any(title in movie for movie in movies_data):
                print(f"⚠️ Movie '{input_new_film}' already exists")
            elif input_new_film == "":
                print("\n⚠️ Movie title cannot be empty - Please try again.\n")
            else:
                break
        else:
            break
    storage.add_movie(title, year, rating, poster_image_url)


def command_delete_movie():
    """
    Delete an existing movie from the database after prompting for its title.
    :return: None
    """
    print("\n *********** DELETE MOVIES *********** \n")

    # Asks until valid input is provided or user quits
    while True:
        delete_movie_input = input(
            "Enter movie name to delete or 'q' to return to menu: ").strip()
        if delete_movie_input == "":
            print("\n⚠️ No movie title was given to delete.\n")
            continue
        elif delete_movie_input.lower() in ("q", "quit"):
            print("Returning to main menu...\n")
            return
        else:
            break

    storage.delete_movie(delete_movie_input)


def command_update_movie():
    """
    Updates the rating of an existing movie in the film database.
    Prompts the user for the movie title and the new rating.
    Allows user to return to the main menu by entering 'q' or 'quit'.
    :return: None
    """
    print("\n *********** UPDATE MOVIE RATINGS *********** \n")

    # Prompt until valid movie title is entered or user quits
    while True:
        update_movie_name_input = input("Enter movie name: ").strip().lower()
        if update_movie_name_input.lower() in ("q", "quit"):
            print("Returning to main menu...\n")
            return
        elif update_movie_name_input == "":
            print("\n⚠️ Movie title cannot be empty - Please try again.\n")
            continue
        else:
            break

    # Prompt until a valid rating is entered
    while True:
        try:
            update_movie_rating_input_float = float(input("Enter new movie rating (0-10): "))

            if not 0 <= update_movie_rating_input_float <= 10:
                print("\n ⚠️ INVALID INPUT - Please try again.\n")
                continue
            break
        except ValueError:
            print("\n ⚠️ INVALID INPUT - Only numbers are allowed.\n")

    storage.update_movie(update_movie_name_input, update_movie_rating_input_float)


def command_show_all_stats():
    """
    Calls functions to show average, median, best and worst rated movies.
    :return: None
    """
    print("\n *********** STATISTICS MOVIES *********** \n")

    movies_data = get_movie_data()

    if not movies_data:
        print("⚠️ No movies in the database to list.")
        return

    movie_stats_average(movies_data)
    movie_stats_median(movies_data)
    movie_stats_best_movie(movies_data)
    movie_stats_worst_movie(movies_data)


def movie_stats_average(movies):
    """
    Calculates and displays the average rating of all movies.
    :param movies: list of movie dictionaries
    :return: None
    """
    count_all_ratings = 0
    count_all_movies = len(movies)
    for stats in movies.values():
        count_all_ratings += stats["rating"]
    average_rating = count_all_ratings / count_all_movies
    print(f"Average rating: {average_rating:.1f}")


def movie_stats_median(movies):
    """
    Calculates and displays the median rating of all movies.
    :param movies: list of movie dictionaries
    :return: None
    """
    all_ratings_list = []
    for stats in movies.values():
        all_ratings_list.append(stats["rating"])
    median_rating_not_equal_count = statistics.median(all_ratings_list)
    print(f"Median rating: {median_rating_not_equal_count} \n")


def movie_stats_best_movie(movies):
    """
    Finds and displays the movie(s) with the highest rating.
    :param movies: list of movie dictionaries
    :return: None
    """
    max_rating = 0
    max_title = []

    for stats in movies.values():
        if stats["rating"] > max_rating:
            max_rating = stats["rating"]

    for movie, stats in movies.items():
        if stats["rating"] == max_rating:
            max_title.append(movie)

    init_result = "Best movie(s): \n"
    for movie in max_title:
        init_result += f"{movie}, with rating {max_rating}\n"
    print(init_result)


def movie_stats_worst_movie(movies):
    """
    Finds and displays the movie(s) with the lowest rating.
    :param movies: list of movie dictionaries
    :return: None
    """
    min_rating = min([stats["rating"] for stats in movies.values()])
    min_title = [movie for movie, stats in movies.items() if stats["rating"] == min_rating]

    init_result = "Worst movie(s): \n"
    for movie in min_title:
        init_result += f"{movie}, with rating {min_rating}\n"
    print(init_result)


def command_random_movie():
    """
    Selects and displays a random movie from the film database, including its rating.
    :return: None
    """
    print("\n *********** RANDOM MOVIE *********** \n")

    movies_data = get_movie_data()

    if not movies_data:
        print("⚠️ No movies in the database to to select from.")
        return

    random_title, movie_data = random.choice(list(movies_data.items()))
    print(f"YOUR RANDOM MOVIE: {random_title}, rated {movie_data['rating']}.")


def command_search_movie():
    """
    Allows the user to search for a movie by partial title.
    All matching movies and their ratings will be displayed.
    :return: None
    """
    print("\n *********** SEARCH MOVIES *********** \n")

    movies_data = get_movie_data()

    if not movies_data:
        print("⚠️ No movies in the database to search.")
        return

    while True:
        search_input = input("Enter part of movie name: ").strip()
        if search_input == "":
            print("\n⚠️ Movie title cannot be empty - Please try again.\n")
            continue
        else:
            break

    movie_found = False

    for movie, stats in movies_data.items():
        if search_input.lower() in movie.lower():
            movie_found = True
            print(f"{movie}, {stats['rating']}")
    if not movie_found:
        print(f"Movie not found for search: '{search_input}'")


def command_movies_sorted_by_rating():
    """
    Display all movies sorted by rating in descending order.
    :return: None
    """
    print("\n *********** MOVIE RANKING - BY RATING *********** \n")

    movies_data = get_movie_data()

    if not movies_data:
        print("⚠️ No movies in the database to list.")
        return

    movies_sorted_list = sorted(movies_data.items(), key=lambda movie: movie[1]["rating"], reverse=True)

    for index, movie in enumerate(movies_sorted_list):
        print(f"{index + 1}.  {movie[1]['rating']} - {movie[0]}")


def command_exit_program():
    """
    End the program and set the global flag to False.
    :return: None
    """
    print("Bye!")
    print("\n *********** END OF PROGRAM *********** \n")
    global RUN_PROGRAM
    RUN_PROGRAM = False


def command_generate_website():
    """
    Generate the static website using the website generator module.
    :return: None
    """
    generate_website()


def get_movie_data():
    """
    Get all movies from the storage module.
    :return: Mapping of movie title to its data dictionary.
    """
    return storage.list_movies()


def main():
    """
    Main loop: handles user input and dispatches selected actions.
    :return: None
    """
    dispatcher = {
        0: command_exit_program,
        1: command_list_movies,
        2: command_add_movie,
        3: command_delete_movie,
        4: command_update_movie,
        5: command_show_all_stats,
        6: command_random_movie,
        7: command_search_movie,
        8: command_movies_sorted_by_rating,
        9: command_generate_website,
    }

    # Menu loop continues while RUN_PROGRAM is True, first
    count_run_program = 0  # Counter - In the first loop the menu is shown
    while RUN_PROGRAM:

        # After the first loop the menu was shown, programm needs [ENTER] action from user loop menu
        if count_run_program >= 1:
            input("\nPress [ENTER] to continue.\n")

        min_choice = "-"
        max_choice = "-"

        try:
            print(command_menu_listing(MENU_OPTIONS))

            min_choice = min(dispatcher)
            max_choice = max(dispatcher)

            user_choice = int(input(f"ENTER CHOICE ({min_choice} - {max_choice}): \n").strip())

            if user_choice < min_choice or user_choice > max_choice:
                print(f"\n ⚠️ INVALID CHOICE - Please type in a number between {min_choice} and {max_choice}.\n")
                continue

            action = dispatcher.get(user_choice)
            if action:
                action()
        except ValueError:
            print(f"\n ⚠️ INVALID CHOICE - Please type in valid number between {min_choice} - {max_choice}.")

        count_run_program += 1  # Counter - number of loops the menu was shown


if __name__ == "__main__":
    main()
