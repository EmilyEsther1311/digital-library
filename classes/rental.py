from datetime import datetime

class BookRental:
    fiction_books = []
    nonfiction_books = []
    children_books = []

    def __init__(self, book = None, borrow_date = None, damage = False):
        self.book = book
        self.borrow_date = borrow_date
        self.return_date = None
        self.days_kept = 0
        self.damage = damage
        self.cost = 0 #Total cost of the rental

    def borrow(self, book):
        self.book = book
        self.book.available = False
        self.borrow_date = datetime.now()
        print(f"{self.book.title} by {self.book.author} (Book ID: {self.book.book_id}) successfully borrowed at {self.borrow_date.strftime("%H:%M")} on {self.borrow_date.strftime("%d/%m/%Y")}")

    def return_book(self):
        self.return_date = datetime.now()

        #Calculating the length of the rental
        timedelta_diff = self.return_date - self.borrow_date
        diff_seconds = timedelta_diff.total_seconds()
        diff_days = diff_seconds // (60*60*24)
        #If length is less than a full day, set length to one day (as a pose to zero days)
        if diff_days < 1:
            self.days_kept = 1
        else:
            self.days_kept = diff_days

        self.book.available = True

        print(f"{self.book.title} by {self.book.author} (Book ID: {self.book.book_id}) successfully returned at {self.return_date.strftime("%H:%M")} on {self.return_date.strftime("%d/%m/%Y")}")

        self.cost = self.calculate_total_cost()

    def report_damage(self):
        self.damage = True
        print(f"Book {self.book.book_id} has been reported as damaged \nThank you for your honesty")

    def calculate_total_cost(self):
        base = float(self.book.price_per_day) * self.days_kept #Standard cost of rental
        late_fee = self.book.calculate_late_fee(self.days_kept)
        damage_fee = self.book.calculate_damage_fee(self.damage)
        total = base + late_fee + damage_fee
        print(f"Total cost of rental: £{total}")
        print(f"   Standard price of rental: £{base}")
        print(f"   Late fee: £{late_fee}")
        print(f"   Damage fee: £{damage_fee}")
        return total