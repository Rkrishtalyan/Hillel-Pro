"""
Розробіть консольний застосунок для керування базою даних "Кінобаза",
що містить інформацію про фільми та акторів, які в них знімалися.
"""

# from movie_database_functions import *
from movie_db_funcs import *

# ---- Initialize the database ----

init_database()


# ---- Display the menu ----

def display_menu():
    """
    Display the main menu for interacting with the movie database.
    """
    print("\n1. Add an actor")
    print("2. Add a movie")
    print("3. Show the list of all movies with the cast")
    print("4. Show unique genres")
    print("5. Show number of movies in each genre")
    print("6. Show average age of actors in each genre")
    print("7. Search a movie by keyword")
    print("8. Show movies page by page")
    print("9. Show a list of all actors and movies")
    print("10. Show a list of movies and how old are they")
    print("0. Exit\n")


# ---- Define the action map ----

functions = {
    '1': add_actor,
    '2': add_movie,
    '3': show_entire_library,
    '4': show_unique_genres,
    '5': count_movies_by_genre,
    '6': avg_actor_age_in_genre,
    '7': find_movie_by_keyword,
    '8': show_movies_page_by_page,
    '9': list_everything,
    '10': list_movies_and_age
}

# ---- Main program execution ----

print("-" * 39)
print("---- Welcome to the movie database ----")
print("-" * 39)

print("\nChoose one of the desired actions:", end='')
display_menu()

print("Enter your choice: ")
user_input = input(">>> ")

while True:
    if user_input.lower() == 'm':
        display_menu()
        print("Enter your choice: ")
        user_input = input(">>> ")
    else:
        if user_input == '0':
            print("\nThank you for using this program! Have a great day!")
            break

        selected_function = functions.get(user_input)

        if selected_function:
            selected_function()
        else:
            print("\nInvalid input, please try again.")
            print("Enter your choice: ")
            user_input = input(">>> ")
            continue

        print("\nWould you like to perform another action?")
        print("Enter 'm' to view menu again.")
        user_input = input(">>> ")
