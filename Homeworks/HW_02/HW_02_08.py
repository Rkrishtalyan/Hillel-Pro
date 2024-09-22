def create_user_settings(user_name):
    user_settings = {
        "theme": None,
        "language": None,
        "notifications": None  # не False або 'disabled' щоб можна було зафіксувати фактичну відмову
    }

    def save_setting(**kwargs):
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
