# Author: Thomas Wunz
# GitHub username: wunzt
# Date: 7/02/2022
# Description: A collection of classes representing a library, its items, and its patrons.
#               Functions include checking out, holding, and returning items and tracking fines.

class LibraryItem:
    """Represents a library item with an id and title."""

    def __init__(self, id, title):
        """Initializes a LibraryItem object with an id and title, as well as additional information."""
        self._library_item_id = id
        self._title = title
        self._location = "ON_SHELF"
        self._checked_out_by = None
        self._requested_by = None
        self._date_checked_out = 0

    def get_library_item_id(self):
        """Returns the item id."""
        return self._library_item_id

    def set_location(self, location):
        """Sets the location to the given input."""
        self._location = location

    def get_location(self):
        """Returns the location."""
        return self._location

    def set_checked_out_by(self, patron):
        """Sets the patron who checked out the item."""
        self._checked_out_by = patron

    def get_checked_out_by(self):
        """Returns the patron who checked out the item."""
        return self._checked_out_by

    def set_requested_by(self, patron):
        """Sets the patron who requested the item."""
        self._requested_by = patron

    def get_requested_by(self):
        """Returns the patron who requested the item."""
        return self._requested_by

    def set_date_checked_out(self, date):
        """Sets the date the item was checked out."""
        self._date_checked_out = date

    def get_date_checked_out(self):
        """Returns the date the item was checked out."""
        return self._date_checked_out

class Book(LibraryItem):
    """Represents a Book LibraryItem type, adding the author."""

    def __init__(self, id, title, author):
        """Initializes the Book object with the LibraryItem information and the author."""
        super().__init__(id, title)
        self._author = author
        self._check_out_length = 21

    def get_check_out_length(self):
        """Returns the check out length of the Book."""
        return self._check_out_length

    def get_author(self):
        """Returns the author of the Book."""
        return self._author

class Album(LibraryItem):
    """Represents an Album LibraryItem type, adding the artist."""

    def __init__(self, id, title, artist):
        """Initializes the Album object with the LibraryItem information and the artist."""
        super().__init__(id, title)
        self._artist = artist
        self._check_out_length = 14

    def get_check_out_length(self):
        """Return the check out length."""
        return self._check_out_length

    def get_artist(self):
        """Returns the artist."""
        return self._artist

class Movie(LibraryItem):
    """Represents a Movie LibraryItem type, adding the director."""

    def __init__(self, id, title, director):
        """Initializes the Movie object with the LibraryItem information and the director."""
        super().__init__(id, title)
        self._director = director
        self._check_out_length = 7

    def get_check_out_length(self):
        """Returns the check out length."""
        return self._check_out_length

    def get_director(self):
        """Returns the director."""
        return self._director

class Patron:
    """Represents a Patron with an id and name."""

    def __init__(self, id, name):
        """Initializes a Patrom with an id, name, dictionary of checked items, and fine amount."""
        self._patron_id = id
        self._name = name
        self._checked_out_items = {}
        self._fine_amount = 0

    def get_patron_id(self):
        """Returns the patron id."""
        return self._patron_id

    def get_fine_amount(self):
        """Returns the patron's fine amount."""
        return self._fine_amount

    def add_library_item(self, item):
        """Adds an item to their checked out list."""
        self._checked_out_items[item.get_library_item_id()] = item

    def remove_library_item(self, item):
        """Removes an item from their checked out list."""
        self._checked_out_items.pop(item.get_library_item_id())

    def get_checked_out_items(self):
        """Returns their checked out list."""
        return self._checked_out_items

    def amend_fine(self, fine):
        """Amends the patron's fine."""
        self._fine_amount += fine


class Library:
    """Represents the library with its holdings, members, and the date."""

    def __init__(self):
        """Initializes a library object with its holdings, members, and the date."""
        self._holdings = {}
        self._members = {}
        self._current_date = 0

    def add_library_item(self, item):
        """Adds an item to the holdings."""
        self._holdings[item.get_library_item_id()] = item

    def add_patron(self, patron):
        """Adds a patron to the members."""
        self._members[patron.get_patron_id()] = patron

    def lookup_library_item_from_id(self, id):
        """Finds an item in holdings given an id."""
        if id in self._holdings:
            return self._holdings[id]
        else:
            return "None"

    def lookup_patron_from_id(self, id):
        """Finds a patron in members given an id."""
        if id in self._members:
            return self._members[id]
        else:
            return "None"

    def check_out_library_item(self, patron_id, item_id):
        """Checks an item out to a patron or informs of why it cannot be."""
        patron = self.lookup_patron_from_id(patron_id)

        item = self.lookup_library_item_from_id(item_id)

        if patron == "None":
            return "patron not found"

        if item == "None":
            return "item not found"

        if item.get_location() == "ON_SHELF":
            item.set_checked_out_by(patron)

            item.set_date_checked_out(self._current_date)

            item.set_location("CHECKED_OUT")

            patron.add_library_item(item)

        elif item.get_location(item_id) == "CHECKED_OUT":
            return "item already checked out"

        elif item.get_location(item_id) == "ON_HOLD_SHELF":
            if patron is not item.get_requested_by():
                return "item on hold by other patron"

            else:
                item.set_checked_out_by(patron)

                item.set_location("CHECKED_OUT")

        return "check out successful"

    def return_library_item(self, id):
        """Returns an item from a patron to the library."""
        item = self.lookup_library_item_from_id(id)

        if item not in self._holdings:
            return "item not found"

        if item.get_location == "ON_SHELF":
            return "item already in library"

        patron = item.get_checked_out_by()

        patron.remove_library_item(id)

        if item.get_requested_by() is not None:
            item.set_location("ON_HOLD_SHELF")

        item.checked_out_by(None)

        return "return successful"

    def request_library_item(self, patron_id, item_id):
        """Adds an item to the hold shelf for a patron or returns why it cannot be added."""
        patron = self.lookup_patron_from_id(patron_id)

        item = self.lookup_library_item_from_id(item_id)

        if patron not in self._members:
            return "patron not found"

        if item not in self._holdings:
            return "item not found"

        if item.get_location(item_id) == "ON_HOLD":
            return "item already on hold"

        else:
            item.set_requested_by(patron)

        if item.get_location(item_id) == "ON_SHELF":
            item.set_location("ON_HOLD_SHELF")

        return "request successful"

    def pay_fine(self, id, amount):
        """Pays a fine for a given amount for a given patron's id."""
        payment = -abs(amount)

        patron = self.lookup_patron_from_id(id)

        if id not in self._members:
            return "patron not found"

        patron.amend_fine(payment)

        return "payment successful"

    def increment_current_date(self):
        """Increments the date and adds daily fines to patrons for overdue items."""
        self._current_date += 1

        for patron_key in self._members:
            patron = self._members[patron_key]

            for item_key in patron.get_checked_out_items():
                item = patron.get_checked_out_items()[item_key]

                days_out = self._current_date - item.get_date_checked_out()

                overdue = days_out - item.get_check_out_length()

                if overdue > 0:
                    patron.amend_fine(0.10)