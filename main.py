#Imports
import json
import ast
import pandas as pd
from datetime import datetime

from classes.book import FictionBook, NonFictionBook, ChildrenBook
from classes.user import LibraryUser
from classes.rental import BookRental

from services.auth import log_in, sign_up
from services.book_services import display_available_books, find_book_from_id

def main():

    #Read rental history dictionary from json file
    try:
        with open("./data/rental_history.json", "r") as f:
            rentals_dct = json.load(f)
    except FileNotFoundError:
        rentals_dct = {}

    #Read books from csv file and append Book objects to correct list in BookRental
    df = pd.read_csv("./data/books.csv", converters={"Reservations": ast.literal_eval})
    len_df = df.shape[0]
    for i in range(len_df):
        if df.loc[i, "Type"] == "Fiction":
            BookRental.fiction_books.append(FictionBook(df.loc[i, "ID"], df.loc[i, "Title"], df.loc[i, "Author"], df.loc[i, "Price"], df.loc[i, "Available"], df.loc[i, "Reservations"]))
        elif df.loc[i, "Type"] == "NonFiction":
            BookRental.nonfiction_books.append(NonFictionBook(df.loc[i, "ID"], df.loc[i, "Title"], df.loc[i, "Author"], df.loc[i, "Price"], df.loc[i, "Available"], df.loc[i, "Reservations"]))
        elif df.loc[i, "Type"] == "Children":
            BookRental.children_books.append(ChildrenBook(df.loc[i, "ID"], df.loc[i, "Title"], df.loc[i, "Author"], df.loc[i, "Price"], df.loc[i, "Available"], df.loc[i, "Reservations"]))

    #Read users dictionary from json file
    try:
        with open("./data/users.json", "r") as f:
            temp_users = json.load(f)
    except FileNotFoundError:
        temp_users = {}

    #Create new `users` dictionary which stores the users as LibraryUser objects
    users = {}
    for username, info in temp_users.items():
        #Returns a dictionary of info about the user's current rental or None if the user isn't currently renting a book
        user_rental_dct = info.setdefault("Rental")
        #Returns the Book ID of the book the user is currently reserving or None if the user is not reserving a book
        user_reservation = info.setdefault("Reservation")

        #Converting Book ID's to Book objects, if necessary
        if user_rental_dct is not None:
            user_rental = BookRental(find_book_from_id(user_rental_dct["Book ID"]), datetime.strptime(user_rental_dct["Borrow Date"],"%Y-%m-%d %H:%M"), user_rental_dct["Damage"])
        else:
            user_rental = None
        if user_reservation is not None:
            user_reservation = find_book_from_id(user_reservation)

        users[username] = LibraryUser(username, info["Password"], user_rental, user_reservation)

    #Loop to log in or sign up
    while True:
        try:
            choice = int(input(f"1. Log in\n"
                               "2. Sign up\n"
                               "Enter choice: "))
        except ValueError:
            print("Invalid choice (must be the number 1 or 3)")
            continue

        #Log in
        if choice == 1:
            current_user = log_in(users)
            break
        #Sign up
        elif choice == 2:
            current_user = sign_up(users)
            break
        else:
            print("Invalid choice (must be the number 1 or 3)")
            continue

    #Loop to run menu until user logs out
    while True:

        #Checking if user\s reserved book has become available
        if current_user.current_reservation is not None:
            if current_user.current_reservation.available and current_user.current_reservation.reservation_queue[0] == current_user.username:
                print(f"NOTIFICATION: Your reserved book, {current_user.current_reservation.title} by {current_user.current_reservation.author} (Book ID: {current_user.current_reservation.book_id}), has become available")
                print("You can now borrow the book (If you choose not to borrow it, your reservation will be cancelled)")
                while True:
                    borrow = input(f"Would you like to borrow book {current_user.current_reservation.book_id}? (y/n): ")
                    if borrow == "y":
                        current_user.borrow_book(current_user.current_reservation)
                        break
                    elif borrow == "n":
                        current_user.cancel_reservation()
                        break
                    else:
                        print("Invalid choice (must be y/n)")

        try:
            choice = int(input(f"\nLibrary Rental System\n"
                               "1. Display available books\n"
                               "2. Borrow a book\n"
                               "3. Return a book\n"
                               "4. Reserve a book\n"
                               "5. Cancel book reservation\n"
                               "6. Report damage to borrowed book\n"
                               "7. Display rental history\n"
                               "8. Log out\n"
                               "Enter choice: "))
        except ValueError:
            print("Invalid choice (must be a number between 1 and 8)")
            continue

        # Displaying available books
        if choice == 1:
            display_available_books()

        #Borrowing a book
        elif choice == 2:
            # Checking if user already has a book borrowed before allowing them to borrow
            if current_user.current_rental is None:
                book_id = input("Please enter the book ID of the book you would like to borrow: ")
                #Identifing the chosen book in the appropriate BookRental list using the input book_id
                chosen_book = find_book_from_id(book_id)

                if not chosen_book:
                    print(f"No book exists with ID {book_id}")
                    continue

                #Checking if the chosen book is available before allowing the user to borrow
                if chosen_book.available:
                    current_user.borrow_book(chosen_book)
                    df.loc[df["ID"] == chosen_book.book_id, "Available"] = False
                else:
                    print(f"Book {book_id} is currently unavailable")
                    #Allowing the user to reserve the currently unavailable book
                    while True:
                        reserve = input(f"Would you like to reserve book {book_id}? (y/n): ")
                        if reserve == "y":
                            if not current_user.current_reservation:
                                current_user.reserve_book(chosen_book)
                                break
                            else:
                                print(f"You are currently reserving {current_user.current_reservation.title} by {current_user.current_reservation.author} (Book ID: {current_user.current_reservation.book_id})")
                                print(f"Please cancel your reservation before reserving another book")
                                break
                        elif reserve == "n":
                            print("No worries! There will be another time")
                            break
                        else:
                            print("Invalid choice (must be y/n)")
            else:
                print(f"You are currently borrowing {current_user.current_rental.book.title} by {current_user.current_rental.book.author} (Book ID: {current_user.current_rental.book.book_id})")
                print(f"You will need to return this book before borrowing another")

        #Returning a book
        elif choice == 3:
            #Checking the user has a book on rent before allowing them to return
            if current_user.current_rental:
                df.loc[df["ID"] == current_user.current_rental.book.book_id, "Available"] = True
                current_user.return_book(rentals_dct)
            else:
                print("You have no borrowed book to return")

        #Reserving a book
        elif choice == 4:
            #Checking that the user is not already reserving a different book
            if not current_user.current_reservation:
                book_id = input("Please enter the ID of the book you would like to reserve: ")
                chosen_book = find_book_from_id(book_id)

                if not chosen_book:
                    print(f"No book exists with ID {book_id}")
                    continue

                if chosen_book.available:
                    print(f"{chosen_book.title} by {chosen_book.author} (Book ID: {chosen_book.book_id}) is available to borrow now")
                    while True:
                        borrow = input(f"Would you like to borrow book {chosen_book.book_id} now? (y/n): ")
                        if borrow == "y":
                            if current_user.current_rental:
                                print(f"You need to return book {current_user.current_rental.book.book_id} before you can borrow another book")
                                break
                            else:
                                current_user.borrow_book(chosen_book)
                                break
                        elif borrow == "n":
                            print("No worries! There will be another time")
                            break
                        else:
                            print("Invalid choice (must be y/n)")
                #Book exists but isn't currently available (therefore, go ahead with reservation)
                else:
                    current_user.reserve_book(chosen_book)
            else:
                print(f"You are currently reserving {current_user.current_reservation.title} by {current_user.current_reservation.author} (Book ID: {current_user.current_reservation.book_id})")
                print(f"Please cancel your reservation before reserving another book")

        #Cancelling a reservation
        elif choice == 5:
            if not current_user.current_reservation:
                print("You have no book reserved in order to cancel")
            else:
                current_user.cancel_reservation()

        #Reporting damage
        elif choice == 6:
            if current_user.current_rental:
                current_user.current_rental.report_damage()
            else:
                print("You have no borrowed book to report damage for")

        #Display rental history
        elif choice == 7:
            current_user.display_rental_history(rentals_dct)

        #Log out
        elif choice == 8:
            print("Thank you for using the Library Rental System")

            #Updating the rental history dictionary stored in the json file using overwriting
            with open("./data/rental_history.json", "w") as f:
                json.dump(rentals_dct, f, indent=4)

            #Updating the entry for the current user in the temp_users dictionary
            #Remove entry, if necessary
            if temp_users.get(current_user.username):
                temp_users.pop(current_user.username)
            #Replace entry with updated values
            temp_users[current_user.username] = {"Password":current_user.password}
            if current_user.current_rental is not None:
                temp_users[current_user.username]["Rental"] = {"Book ID" : current_user.current_rental.book.book_id , "Borrow Date" : current_user.current_rental.borrow_date.strftime("%Y-%m-%d %H:%M") , "Damage" : current_user.current_rental.damage}
            if current_user.current_reservation is not None:
                temp_users[current_user.username]["Reservation"] = current_user.current_reservation.book_id

            #Updating the users dictionary stored in the json file using overwriting
            with open("./data/users.json", "w") as f:
                json.dump(temp_users, f, indent=4)

            #Updating the books.csv file to the current pandas data frame
            df.to_csv("./data/books.csv", index=False)

            break

        else:
            print("Invalid choice (must be a number between 1 and 8)")
            continue

if __name__ == "__main__":
    main()
