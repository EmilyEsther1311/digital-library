class Book:
    def __init__(self, book_id, title, author, price_per_day, available, reservation_queue):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.price_per_day = price_per_day
        self.available = available
        self.reservation_queue = reservation_queue

    #Adding a user to the book's reservation queue
    def add_reservation(self, user):
        self.reservation_queue.append(user.username)
        print(f"You have successfully been added to the reservation queue for {self.title} by {self.author} (Book ID: {self.book_id})")

    def cancel_reservation(self, user):
        self.reservation_queue.remove(user.username)
        print(f"You have successfully been removed from the reservation queue for {self.title} by {self.author} (Book ID: {self.book_id})")

class FictionBook(Book):
    def calculate_late_fee(self, days_kept):
        #Late fee: £1 per day after 14 days
        if days_kept > 14:
            days_late = int(days_kept - 14)
            if days_late == 1:
                print(f"Book is being returned 1 day late")
            else:
                print(f"Book is being returned {days_late} days late")
            print(f"   Late fee: £1 x {days_late} = £{days_late}")
            return days_late
        else:
            return 0

    def calculate_damage_fee(self, damaged):
        #Damage fee: £10
        if damaged:
            print("Book is being returned damaged")
            print("   Damage fee: £10")
            return 10
        else:
            return 0


class NonFictionBook(Book):
    def calculate_late_fee(self, days_kept):
        # Late fee: £2 per day after 21 days
        if days_kept > 21:
            days_late = int(days_kept - 21)
            if days_late == 1:
                print("Book is being returned 1 day late")
            else:
                print(f"Book is being returned {days_late} days late")
            print(f"   Late fee: £2 x {days_late} = £{2*days_late}")
            return 2*days_late
        else:
            return 0

    def calculate_damage_fee(self, damaged):
        #Damage fee: £20
        if damaged:
            print("Book is being returned damaged")
            print("   Damage fee: £20")
            return 20
        else:
            return 0


class ChildrenBook(Book):
    def calculate_late_fee(self, days_kept):
        #Late fee: £0.5 per day after 7 days
        if days_kept > 7:
            days_late = int(days_kept - 7)
            if days_late == 1:
                print("Book is being returned 1 day late")
            else:
                print(f"Book is being returned {days_late} days late")
            print(f"   Late fee: £0.50 x {days_late} = £{0.5 *days_late}")
            return 0.5*days_late
        else:
            return 0

    def calculate_damage_fee(self, damaged):
        #Damage fee £5
        if damaged:
            print("Book is being returned damaged")
            print("   Damage fee: £5")
            return 5
        else:
            return 0