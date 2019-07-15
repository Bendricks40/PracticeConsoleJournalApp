from peewee import *
import datetime
from collections import OrderedDict
import sys
import os


db = SqliteDatabase('journal.db')


class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    """create table and db if don't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('clear')



def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    """Add an Entry"""

    print("Enter your entry. Write <quit> when finished.")
    final_data = ''

    while True:
        data = sys.stdin.readline().strip()
        if data == 'quit':
            if input('Save entry? [Yn] ').lower() != 'n':
                Entry.create(content=final_data)
                print("Saved successfully!")
                break
            else:
                break
        else:
            final_data += data + '\n'


def view_entries(search_query=None):
    """view previous entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        clear()
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print('='*len(timestamp))
        print(entry.content)
        print('\n\n' + '='*len(timestamp) + '\n\n')
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [ndq] ').lower().strip()

        if next_action == 'q':
            break
        if next_action == 'd':
            delete_entry(entry)


def search_entries():
    """Search entries for a string"""
    view_entries(input('Search query: '))


def delete_entry(entry):
    """Delete an entry"""
    if input("Are you sure? [yn] ").lower() == 'y':
        entry.delete_instance()
        print("Entry deleted! \n")


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
])



if __name__ == '__main__':
    initialize()
    menu_loop()
