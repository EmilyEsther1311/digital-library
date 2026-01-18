from classes.rental import BookRental
from services.book_services import find_book_from_id

class LibraryUser:
    def __init__(self, username, password, rental = None, reservation = None):
        self.username = username
        self.password = password
        self.current_rental = rental
        self.current_reservation = reservation

    def borrow_book(self, book):
        #If borrowing reserved book, cancel reservation
        if self.current_reservation == book:
            self.cancel_reservation()

        self.current_rental = BookRental()
        self.current_rental.borrow(book)

    def return_book(self, rentals_dct):
        self.current_rental.return_book()
        self.update_rental_history(rentals_dct)
        self.current_rental = None

    def reserve_book(self, book):
        self.current_reservation = book
        book.add_reservation(self)

    def cancel_reservation(self):
        self.current_reservation.cancel_reservation(self)
        self.current_reservation = None

    def update_rental_history(self, rentals_dct):
        rentals_dct.setdefault(self.username, []).append({"Book ID": self.current_rental.book.book_id, "Borrow date" : self.current_rental.borrow_date.strftime("%Y-%m-%d %H:%M"), "Return date": self.current_rental.return_date.strftime("%Y-%m-%d %H:%M"), "Damage" : self.current_rental.damage, "Cost": self.current_rental.cost})

    def display_rental_history(self, rentals_dct):
        print(f"Rental history for {self.username}:")
        if rentals_dct.get(self.username):
            for rental in rentals_dct[self.username]:
                rental_book = find_book_from_id(rental["Book ID"])
                print(f"{rental_book.title} by {rental_book.author} (Book ID: {rental_book.book_id})")
                print(f"   Borrow date: {rental["Borrow date"]}")
                print(f"   Return date: {rental["Return date"]}")
                print(f"   Total cost: £{rental["Cost"]}")