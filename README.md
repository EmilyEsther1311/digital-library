# Digital Library Management System

This project is a Python-based command-line interface application designed to manage a library's book catalog, user accounts, and rental transactions. It features a tiered fee system based on book categories, automated cost calculations, and a reservation queue system.

## Features
* **User Authentication**: A secure system for logging in and signing up. Passwords must be at least 8 characters long and contain at least one capital letter.
* **Dynamic Catalog**: Browse a library of books categorized into Fiction, Non-Fiction, and Children's sections.
* **Rental Management**: Borrow and return books with automated calculation of total costs, including late fees and damage penalties.
* **Reservation System**: If a book is unavailable, users can join a reservation queue. The system notifies the user when their reserved book becomes available.
* **Data Persistence**: User accounts, rental histories, and book statuses are automatically saved to JSON and CSV files upon logout.

## Project Structure
```
├── main.py
├── classes/
│   ├── book.py
│   ├── rental.py
│   └── user.py
├── services/
│   ├── auth.py
│   └── book_services.py
├── data/
│   ├── books.csv
│   ├── rental_history.json
│   └── users.json
└── README.md
```

* `main.py`: The entry point of the application; handles the main menu, user sessions, and data persistence.
* **classes/**:
    * `book.py`: Defines the `Book` base class and specialised subclasses (`FictionBook`, `NonFictionBook`, `ChildrenBook`) with unique fee calculation logic.
    * `user.py`: Manages the `LibraryUser` object, including their rental and reservation status.
    * `rental.py`: Logic for the `BookRental` class, which tracks borrow dates, return dates, and costs.
* **services/**:
    * `auth.py`: Handles user login, account creation, and password validation.
    * `book_services.py`: Provides helper functions to display available books and locate books by their unique ID.
* **data/**:
    * `books.csv`: The master list of library books.
    * `users.json`: Stores user credentials and active rental/reservation data.
    * `rental_history.json`: Archives completed rental records.

## Installation
1. Ensure you have **Python 3.13** or later installed.
2. Install the required `pandas` library:
   ```bash
   pip install pandas