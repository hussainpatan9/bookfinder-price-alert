# Book Price Alert Script

This script automates the process of checking the lowest available prices for books listed in an Excel file on BookFinder.com and sends an email notification if the prices fall below a specified threshold. It is built using Python, SeleniumBase, and other libraries to facilitate web automation, data processing, and email communication.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Error Handling](#error-handling)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Automated Web Scraping**: Utilizes SeleniumBase to search for book prices on BookFinder.com.
- **Excel Integration**: Loads book data (ISBN, price limit, title) from an Excel file.
- **Email Notifications**: Sends a single email summarizing all books found below the price limit.
- **Error Handling**: Continues processing even if an error occurs for a specific book.
- **Configurable**: Easily configurable email and scraping settings.

## Requirements

- Python 3.7+
- An internet connection
- Access to an SMTP server for sending emails

### Python Libraries

The following Python libraries are required:

- `pandas`: For reading and processing the Excel file.
- `seleniumbase`: For web automation and scraping.
- `smtplib`: For sending emails.
- `email.mime`: For constructing email messages.

These can be installed via `pip`:

```bash
pip install pandas seleniumbase
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/book-price-alert.git
   cd book-price-alert
   ```
2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
3. **Prepare the Excel file**:

   Ensure you have an Excel file named `books.xlsx` with the following columns:

   - `ISBN `: The ISBN of the book.
   - `Price limit in euro`: The maximum price you are willing to pay.
   - `Book title`: The title of the book.

   The script will use this data to perform searches.

## Configuration

1. **SMTP Email Settings**:

   Open the script file and configure your email settings:

   ```python
   SMTP_SERVER = 'smtp.example.com'  # Replace with your SMTP server
   SMTP_PORT = 587
   EMAIL_ADDRESS = 'your_email@example.com'  # Replace with your email address
   EMAIL_PASSWORD = 'your_password'  # Replace with your email password
   RECIPIENT_EMAIL = 'recipient@example.com'  # Replace with the recipient's email address
   ```
2. **Excel File Path**:

   Ensure that the `EXCEL_FILE_PATH` variable points to the correct location of your Excel file:

   ```python
   EXCEL_FILE_PATH = 'books.xlsx'
   ```
3. **Delay Between Searches**:

   You can adjust the delay between searches to avoid being flagged as a bot:

   ```python
   SLEEP_DURATION = 5  # Time in seconds
   ```

## Usage

To run the script, simply execute the following command in your terminal:

```bash
python book_price_alert.py
```

The script will:

1. Load book data from `books.xlsx`.
2. Search for each book on BookFinder.com.
3. Compare the lowest price found with the specified price limit.
4. Collect notifications for books priced below the limit.
5. Send a single email summarizing all relevant books.

## How It Works

- **Loading Data**: The script reads the ISBN, price limit, and book title from an Excel file using `pandas`.
- **Scraping**: SeleniumBase is used to automate a web browser that searches for each book by ISBN on BookFinder.com, selects the appropriate options (e.g., destination, currency), and scrapes the lowest price for used books.
- **Price Comparison**: The lowest price is compared against the user-defined price limit.
- **Email Notification**: If any books are found below the price limit, the script sends an email with the details.

## Error Handling

- The script includes error handling to ensure that even if an error occurs while processing a specific book (e.g., network issues, incorrect data), the script will continue to the next book.
- All errors are logged to the console, and if no books meet the criteria, the script will notify you accordingly.

## Customization

You can customize the script to meet your needs:

- **Email Content**: Modify the `send_notification` function to change the format and content of the email.
- **Scraping Logic**: Adjust the `search_book_on_bookfinder` function to change how prices are extracted or to scrape additional information.
- **Error Handling**: Enhance the error handling mechanisms to include more specific scenarios or to log errors to a file.

## Contributing

If you'd like to contribute to this project, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
