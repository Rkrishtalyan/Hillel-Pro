"""
Завдання 8: Зберігання налаштувань користувача.

Реалізувати систему зберігання налаштувань користувача за допомогою замикань.

1.  Створити функцію create_user_settings, яка повертає функцію для зберігання
    і отримання налаштувань.
2.  Налаштування можуть включати такі параметри, як theme, language і notifications.
3.  Додати можливість зберігати, змінювати та переглядати налаштування.
"""


# ---- Define user settings function ----
def create_user_settings(user_name):
    """
    Create a settings manager for a specific user.

    Initializes a settings dictionary for a user with default values of None
    for theme, language, and notifications. Returns a function to save or
    display the user's settings.

    :param user_name: Name of the user for whom settings are being managed.
    :type user_name: str
    :return: Function to manage and save settings for the user.
    :rtype: function
    """
    user_settings = {
        "theme": None,
        "language": None,
        "notifications": None  # не False або 'disabled' щоб можна було зафіксувати фактичну відмову
    }

    def save_setting(**kwargs):
        """
        Update and display user settings.

        Accepts any number of keyword arguments to update settings for the
        user. If called without arguments, prints the current settings.

        :param kwargs: Key-value pairs of settings to update.
        :type kwargs: dict
        """
        if kwargs:
            for key, value in kwargs.items():
                user_settings[key] = value
        else:
            print(f"{user_name}: {user_settings}")

    return save_setting


# ---- Example usage of user settings manager ----
settings_for_john = create_user_settings("John")
settings_for_john(theme="dark", language="English", notifications=False)
settings_for_john()

settings_for_jane = create_user_settings("Jane")
settings_for_jane()
settings_for_jane(theme="light", language="French", notifications=True)
settings_for_jane()
