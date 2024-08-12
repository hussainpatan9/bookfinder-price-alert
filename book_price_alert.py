import pandas as pd
import time
from seleniumbase import SB
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email settings
SMTP_SERVER = 'smtp.example.com'  # Replace with your SMTP server
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@example.com'  # Replace with your email address
EMAIL_PASSWORD = 'your_password'  # Replace with your email password
RECIPIENT_EMAIL = 'recipient@example.com'  # Replace with the recipient's email address

# Excel file path
EXCEL_FILE_PATH = 'books.xlsx'

# Time to wait between searches (in seconds)
SLEEP_DURATION = 5

def load_data_from_excel(file_path):
    """Load the ISBN, price limit, and book title from an Excel file."""
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Failed to load data from Excel: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if the file cannot be loaded

def search_book_on_bookfinder(isbn):
    """Search for a book by ISBN on BookFinder and return the lowest price for used books."""
    try:
        with SB() as sb:
            sb.open("https://www.bookfinder.com/")
            sb.type('input[name="isbn"]', isbn)
            sb.select_option_by_text('select[name="destination"]', 'Netherlands')
            sb.select_option_by_text('select[name="currency"]', 'Euro')
            sb.click('//label[normalize-space()="Used"]')
            sb.click('button[type="submit"]')

            sb.sleep(10)  # Wait for search results to load
            sb.wait_for_element_visible('div#double-column-results', timeout=20)

            # Locate the container for used book results
            price_elements = sb.find_elements('div.bf-search-result-col-actions a.clickout-logger')

            # Extract and process prices
            prices = []
            for price_element in price_elements:
                price_text = price_element.text.strip('€ ').replace(',', '.')
                try:
                    price = float(price_text)
                    prices.append(price)
                except ValueError:
                    print(f"Skipping invalid price: {price_text}")
                    continue

            return min(prices) if prices else None
    except Exception as e:
        print(f"An error occurred while searching for ISBN {isbn}: {e}")
        return None

def send_notification(notifications):
    """Send a single email notification with details of all books that met the price criteria."""
    if not notifications:
        print("No notifications to send.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = 'Price Alert Summary for Your Books'

        body = "The following books are available below your price limit:\n\n"
        for notification in notifications:
            body += f"- {notification['book_title']} (ISBN: {notification['isbn']}): €{notification['lowest_price']}\n"

        msg.attach(MIMEText(body, 'plain'))

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("Notification email sent successfully.")
    except Exception as e:
        print(f"Failed to send notification email: {e}")

def check_prices_and_notify():
    """Main function to check book prices and send notifications if necessary."""
    data = load_data_from_excel(EXCEL_FILE_PATH)
    if data.empty:
        print("No data to process.")
        return

    notifications = []

    for index, row in data.iterrows():
        try:
            isbn = str(row['ISBN ']).strip()
            price_limit = float(str(row['Price limit in euro']).strip('€ ').replace(',', '.'))
            book_title = row['Book title']

            # Search for the book and get the lowest price
            lowest_price = search_book_on_bookfinder(isbn)

            # Compare with the price limit and collect notification if the price is lower
            if lowest_price is not None and lowest_price < price_limit:
                print(f"Book Title: {book_title}, ISBN: {isbn}, Lowest Price: €{lowest_price}")
                notifications.append({
                    'book_title': book_title,
                    'isbn': isbn,
                    'lowest_price': lowest_price
                })
            else:
                print(f"Book Title: {book_title}, ISBN: {isbn}, No price below limit found.")

        except Exception as e:
            print(f"Error processing book '{book_title}' (ISBN: {isbn}): {e}")

        finally:
            # Introduce delay between searches to avoid being flagged as a bot
            time.sleep(SLEEP_DURATION)

    # Send a single notification email with all the results
    send_notification(notifications)

if __name__ == "__main__":
    check_prices_and_notify()
