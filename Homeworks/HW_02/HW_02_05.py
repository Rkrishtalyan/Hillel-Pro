from datetime import date

calendar = []


def calendar_actions():
    def add_event_to_calendar(event_name, event_date):
        calendar.append({"event_name": event_name, "event_date": event_date})
        print(f"\nДодано подію \"{event_name}\" на {event_date}")

    def remove_event_from_calendar(event_name):
        event_found = False
        for event in calendar:
            if event["event_name"] == event_name:
                event_found = True
                calendar.remove(event)
                print(f"\nПодію {event_name} видалено")
        if not event_found:
            print(f"\nТакої події немає")

    def view_upcoming_events_in_calendar():
        upcoming_events = []
        today = str(date.today())
        if calendar:
            for event in calendar:
                if event["event_date"] > today:
                    upcoming_events.append(event)

        def get_event_date(event):
            return event["event_date"]

        if upcoming_events:
            upcoming_events = sorted(upcoming_events, key=get_event_date)
            print("\nМайбутні події:")
            for event in upcoming_events:
                event_name, event_date = event.values()
                print(f"- {event_name}, дата {event_date}")
        else:
            print(f"\nУ каленадрі немає майбутніх подій")

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

print(calendar)
