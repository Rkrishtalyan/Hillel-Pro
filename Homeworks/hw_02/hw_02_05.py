"""
Завдання 5: Календар подій.

Розробити простий календар подій.

1.  Використовуючи замикання, створити функції для додавання подій,
    видалення подій та перегляду майбутніх подій.
2.  Зберігати події у списку за допомогою глобальної змінної.
"""

from datetime import date

# ---- Initialize calendar ----
calendar = []


# ---- Define calendar action functions ----
def calendar_actions():
    """
    Return a set of functions to manage calendar events, including adding,
    removing, and viewing upcoming events.

    The functions interact with the global `calendar` list, modifying or
    displaying events as specified.
    """

    def add_event_to_calendar(event_name, event_date):
        """
        Add an event to the calendar.

        :param event_name: Name of the event to add.
        :type event_name: str
        :param event_date: Date of the event in 'YYYY-MM-DD' format.
        :type event_date: str
        """
        calendar.append({"event_name": event_name, "event_date": event_date})
        print(f"\nДодано подію \"{event_name}\" на {event_date}.")

    def remove_event_from_calendar(event_name):
        """
        Remove an event from the calendar by name.

        Searches the calendar for an event with the specified name and removes
        it if found. If the event is not found, prints a message indicating this.

        :param event_name: Name of the event to remove.
        :type event_name: str
        """
        event_found = False
        for event in calendar:
            if event["event_name"] == event_name:
                event_found = True
                calendar.remove(event)
                print(f"\nПодію {event_name} видалено.")
        if not event_found:
            print(f"\nТакої події немає.")

    def view_upcoming_events_in_calendar():
        """
        Display upcoming events in the calendar.

        Filters events to include only those with dates later than the current date.
        If any upcoming events are found, they are printed in order of their date.

        :return: List of upcoming events.
        :rtype: list of dict
        """
        upcoming_events = []
        today = str(date.today())
        if calendar:
            for event in calendar:
                if event["event_date"] > today:
                    upcoming_events.append(event)

        def get_event_date(event):
            """
            Retrieve the date from an event for sorting.

            :param event: Event dictionary containing an event name and date.
            :type event: dict
            :return: The date of the event.
            :rtype: str
            """
            return event["event_date"]

        if upcoming_events:
            upcoming_events = sorted(upcoming_events, key=get_event_date)
            print("\nМайбутні події:")
            for event in upcoming_events:
                event_name, event_date = event.values()
                print(f"- {event_name}, дата {event_date}.")
        else:
            print(f"\nУ каленадрі немає майбутніх подій.")

        return upcoming_events

    return add_event_to_calendar, remove_event_from_calendar, view_upcoming_events_in_calendar


# ---- Retrieve calendar action functions ----
add_event, remove_event, view_upcoming_events = calendar_actions()

# ---- Execute calendar actions for demonstration ----
add_event("Зустріч з клієнтом", "2024-09-25")
add_event("День народження", "2024-10-01")
add_event("Кінець світу", "2012-12-21")
view_upcoming_events()

remove_event("Зустріч з клієнтом")
view_upcoming_events()

remove_event("День народження")
view_upcoming_events()

print(f"\n{calendar}")
