import asyncio
import time
from datetime import datetime
from threading import Thread, Event
from playwright_crawler import fetch_page_content
from discord_notify import send_discord_notification
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Shared variable to indicate if tickets are available
tickets_available = Event()

async def check_tickets():
    global tickets_available
    while not tickets_available.is_set():
        start_time = time.time()
        result = await fetch_page_content()

        if isinstance(result, str) and result.startswith("Error:"):
            send_discord_notification(f"Error detected: {result}")
            logging.error(f"Error detected: {result}")
        elif result:
            send_discord_notification("Academic tickets are now available! Visit https://ghc.anitab.org/pricing to register.")
            tickets_available.set()  # Indicate that tickets are available
            logging.info("Tickets are available")
            break
        else:
            logging.info("Tickets are not available")

        end_time = time.time()
        elapsed_time = end_time - start_time
        sleep_time = max(60 - elapsed_time, 0)  # Adjust sleep time to maintain approximately 1-minute intervals
        time.sleep(sleep_time)

def daily_check():
    global tickets_available
    while not tickets_available.is_set():
        now = datetime.now()
        if now.hour == 23 and now.minute == 59:
            send_discord_notification("No tickets available today.")
            logging.info("Daily notification sent: No tickets available today")
            time.sleep(60)  # Ensure it doesn't send multiple notifications within the same minute
        time.sleep(30)  # Check every 30 seconds

def main():
    # Start the ticket checking in a separate thread
    ticket_thread = Thread(target=lambda: asyncio.run(check_tickets()))
    ticket_thread.start()

    # Start the daily check in the main thread
    daily_check()

if __name__ == "__main__":
    main()
