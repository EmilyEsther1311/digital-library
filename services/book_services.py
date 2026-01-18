from classes.rental import BookRental

def display_available_books():
    print("List of Available Books:")

    print("Fiction Books: ")
    fiction_available = False
    for book in BookRental.fiction_books:
        if book.available:
            fiction_available = True
            print(f"    {book.title} by {book.author} (Book ID: {book.book_id}, Price per day: £{book.price_per_day})")
    if not fiction_available:
        print("No fiction books are currently available")

    print("Non-Fiction Books: ")
    non_fiction_available = False
    for book in BookRental.nonfiction_books:
        if book.available:
            non_fiction_available = True
            print(f"    {book.title} by {book.author} (Book ID: {book.book_id}, Price per day: £{book.price_per_day})")
    if not non_fiction_available:
        print("No non-fiction books are currently available")

    print("Children Books: ")
    child_available = False
    for book in BookRental.children_books:
        if book.available:
            child_available = True
            print(f"    {book.title} by {book.author} (Book ID: {book.book_id}, Price per day: £{book.price_per_day})")
    if not child_available:
        print("No children books are currently available")

def find_book_from_id(book_id):
    # Identifying the chosen book in the appropriate BookRental list using the book_id
    chosen_book = None
    if book_id[0] == "F":
        for book in BookRental.fiction_books:
            if book.book_id == book_id:
                chosen_book = book
    elif book_id[0:2] == "NF":
        for book in BookRental.nonfiction_books:
            if book.book_id == book_id:
                chosen_book = book
    elif book_id[0] == "C":
        for book in BookRental.children_books:
            if book.book_id == book_id:
                chosen_book = book
    return chosen_book