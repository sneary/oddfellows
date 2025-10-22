from pytz import timezone
import schedule
import time
import datetime
import requests


ODDFELLOWS_WEBHOOK_URL = 'SECRET PLEASE ASK ME AND I WILL SEND IT TO YOU'


def is_nth_weekday(date_obj, weekday, n):
    """
    Checks if a given date is the nth occurrence of a specific weekday in its month.

    Args:
        date_obj (datetime.date): The date to check.
        weekday (int): The day of the week (0=Monday, 6=Sunday).
        n (int): The occurrence number (e.g., 1 for 1st, 2 for 2nd, etc.).

    Returns:
        bool: True if the date is the nth occurrence of the weekday, False otherwise.
    """
    if date_obj.weekday() != weekday:
        return False

    first_day_of_month = datetime.date(date_obj.year, date_obj.month, 1)
    # Calculate days until the first occurrence of the target weekday in the month
    days_until_first_occurrence = (weekday - first_day_of_month.weekday() + 7) % 7
    first_occurrence_date = first_day_of_month + datetime.timedelta(days=days_until_first_occurrence)

    # Calculate the expected date for the nth occurrence
    expected_date = first_occurrence_date + datetime.timedelta(weeks=n - 1)

    return date_obj == expected_date


def send_to_discord(webhook_url, message):
    """Sends a message to a Discord webhook."""
    try:
        response = requests.post(webhook_url, json={'content': message})
        response.raise_for_status()  # Raise an exception for non-200 status codes
        print("Message sent to Discord successfully!")
    except requests.exceptions.RequestException as error:
        print(f"Error sending message to Discord: {error}")


def send_monday_messages():
    current_date = datetime.date.today()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if current_date.weekday() == 0:  # Check if it's Monday (0=Monday)
        # Check specifically for the 4th Monday first
        if is_nth_weekday(current_date, 0, 4):
            print(f"[{current_time}] It's the **4th Monday**! Sending a *special* 4th Monday message.")
            current_month = current_date.strftime('%B')
            message = "Hello <@&1353765726284152957> and <@&1283059450273468482>! Today is the 4th Monday of " + current_month + ", so it is time for our joint social meeting night! It would bring me great joy to know of your attendance at our social gathering this evening. In our traditional fashion, please indicate your intention to attend by reacting to this message with a white sphere :white_circle: for yes or a black cube :black_large_square: for no, so that the proper amount of aliments may be prepared."
            send_to_discord(ODDFELLOWS_WEBHOOK_URL, message)
        else:
            # If it's a Monday but not the 4th, send the regular Monday message
            print(f"[{current_time}] It's a **regular Monday**! Sending the standard weekly message.")
            message = "Hello fellow <@&1283059450273468482>, it would bring me great joy to know of your attendance at our pre-meeting dinner this evening. In our traditional fashion, please indicate your intention to attend by reacting to this message with a white sphere :white_circle: for yes or a black cube :black_large_square: for no, so that the proper amount of aliments may be prepared."
            send_to_discord(ODDFELLOWS_WEBHOOK_URL, message)


def send_first_wednesday_message():
    current_date = datetime.date.today()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_month = current_date.strftime('%B')

    # Check if it's the first Wednesday of the current month
    if is_nth_weekday(current_date, 2, 1): # 2 for Wednesday, 1 for the first occurrence
        print(f"[{current_time}] It's the **First Wednesday of the month**! Sending a unique message.")
        message = "Hello <@&1353765726284152957>. Today is the first Wednesday of " + current_month + ", so it is time for our monthly business meeting. It would bring me great joy to know of your attendance at our pre-meeting dinner this evening. In our traditional fashion, please indicate your intention to attend by reacting to this message with a white sphere :white_circle: for yes or a black cube :black_large_square: for no, so that the proper amount of aliments may be prepared."
        send_to_discord(ODDFELLOWS_WEBHOOK_URL, message)
    else:
        # This else block should ideally not be hit if scheduled correctly,
        # but is good for robust function design.
        print(f"[{current_time}] Not the first Wednesday. Skipping First Wednesday message.")


# --- Scheduling the tasks ---

# 1. Schedule the Monday messages
schedule.every().monday.at("10:00", timezone("America/New_York")).do(send_monday_messages)
print("Scheduled 'Monday Messages' to run every Monday at 09:00.")

# 2. Schedule the First Wednesday message
schedule.every().wednesday.at("10:00", timezone("America/New_York")).do(send_first_wednesday_message)
print("Scheduled 'First Wednesday Message' to run every Wednesday at 10:00.")


print("\nScheduler started. Press Ctrl+C to stop.\n")

# --- Keep the script running to allow the scheduler to operate ---
while True:
    schedule.run_pending()
    time.sleep(60) # Wait for 1 min before checking again
