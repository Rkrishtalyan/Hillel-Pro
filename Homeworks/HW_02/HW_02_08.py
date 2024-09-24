"""
Завдання 8: Зберігання налаштувань користувача.

Реалізувати систему зберігання налаштувань користувача за допомогою замикань.

1.	Створити функцію create_user_settings, яка повертає функцію для зберігання і отримання налаштувань.
2.	Налаштування можуть включати такі параметри, як theme, language і notifications.
3.	Додати можливість зберігати, змінювати та переглядати налаштування.
"""


def create_user_settings(user_name):
    """Create user_settings dict with default values. Return function to re-define, add new or view existing values."""
    user_settings = {
        "theme": None,
        "language": None,
        "notifications": None  # не False або 'disabled' щоб можна було зафіксувати фактичну відмову
    }

    def save_setting(**kwargs):
        """Update user_settings dict with defined values. Print current settings if no arguments provided."""
        if kwargs:
            for key, value in kwargs.items():
                user_settings[key] = value
        else:
            print(f"{user_name}: {user_settings}")

    return save_setting


settings_for_john = create_user_settings("John")
settings_for_john(theme="dark", language="English", notifications=False)
settings_for_john()

settings_for_jane = create_user_settings("Jane")
settings_for_jane()
settings_for_jane(theme="light", language="French", notifications=True)
settings_for_jane()
