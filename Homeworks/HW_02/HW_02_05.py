"""
Завдання 5: Календар подій.

Розробити простий календар подій.

1.	Використовуючи замикання, створити функції для додавання подій, видалення подій та перегляду майбутніх подій.
2.	Зберігати події у списку за допомогою глобальної змінної.
"""

from datetime import date

calendar = []


def calendar_actions():
    """Create and return functions to manage a calendar of events."""
    """
    The returned functions allow adding events, removing events, and viewing upcoming events.
    These functions operate on a global list called calendar.
    """
    def add_event_to_calendar(event_name, event_date):
        """Add an event to the global calendar."""
        calendar.append({"event_name": event_name, "event_date": event_date})
        print(f"\nДодано подію \"{event_name}\" на {event_date}.")

    def remove_event_from_calendar(event_name):
        """Remove an event from the global calendar by its name."""
        event_found = False
        for event in calendar:
            if event["event_name"] == event_name:
                event_found = True
                calendar.remove(event)
                print(f"\nПодію {event_name} видалено.")
        if not event_found:
            print(f"\nТакої події немає.")

    def view_upcoming_events_in_calendar():
        """Display all upcoming events in the global calendar sorted by date."""
        upcoming_events = []
        today = str(date.today())
        if calendar:
            for event in calendar:
                if event["event_date"] > today:
                    upcoming_events.append(event)

        def get_event_date(event):
            """Return the event date."""
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


add_event, remove_event, view_upcoming_events = calendar_actions()

add_event("Зустріч з клієнтом", "2024-09-25")
add_event("День народження", "2024-10-01")
add_event("Кінець світу", "2012-12-21")
view_upcoming_events()

remove_event("Зустріч з клієнтом")
view_upcoming_events()

remove_event("День народження")
view_upcoming_events()

print(f"\n{calendar}")
