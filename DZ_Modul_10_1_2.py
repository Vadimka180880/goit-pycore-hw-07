def input_error(func):                                                                               # Декоратор, що обробляє помилки введення
    
    def wrapper(*args, **kwargs):                                                  
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            return "Invalid command or argument. Please try again."
    return wrapper

@input_error
def parse_input(user_input):                                                                        # Розбиває введене користувачем рядок на команду та аргументи
    parts = user_input.split()                                                      
    cmd = parts[0].lower()                                                          
    args = parts[1:]                                                            
    if cmd == "add_birthday":                                                      
        name = args[0]
        birthday = " ".join(args[1:])                                               
        return cmd, [name, birthday]                                                
    else:
        return cmd, args

import re

@input_error
def add_contact(args, contacts):                                                                     # Додає новий контакт до списку контактів
    if len(args) != 2:
        return "Give me name and phone, please."
    name, phone = args
    if not re.match(r'^\d+$', phone):                                               
        return "Phone number must contain only digits."
    contacts[name] = phone
    return "Contact added."

@input_error
def search_records(args, address_book):                                                             # Шукає контакти за іменем або номером телефону                                               
    if len(args) != 1:
        return "Invalid command. Please provide a name or phone number to search for."
    search_term = args[0]
    matching_contacts = []
    for name, record in address_book.data.items():
        if re.search(search_term, name):
            matching_contacts.append((name, record.phones))
        else:
            for phone in record.phones:
                if re.search(search_term, phone):
                    matching_contacts.append((name, phone))
                    break  
    if matching_contacts:
        result = "Matching contacts:\n"
        for contact in matching_contacts:
            if isinstance(contact[1], list):  
                phones = ", ".join(contact[1])
                result += f"{contact[0]}: {phones}\n"
            else:
                result += f"{contact[0]}: {contact[1]}\n"
        return result
    else:
        return "No matching contacts found."

@input_error
def add_record(args, address_book):                                                                 # Додає новий запис до адресної книги
    if len(args) < 2:
        return "Invalid command. Please provide a name and a phone number for the new record."
    name, phone = args[0], args[1]
    if not re.match(r'^\d+$', phone):                                              
        return "Phone number must contain only digits."
    return address_book.add_record(name, phone)  


@input_error
def change_contact(args, address_book):                                                             # Змінює номер телефону існуючого контакту 
    if len(args) != 2:                                                             
        return "Invalid command. Please provide both username and new phone number."    
    name, new_value = args                                                             
    if name in address_book.data:                                                            
        if re.match(r'^\d+$', new_value):                                          
            address_book.data[name].phones = [new_value]                                                     
            return "Contact updated."
        else:
            return "Invalid phone number. Please provide a valid phone number for the contact."
    else:
        return f"Contact '{name}' not found."

@input_error
def get_phone(args, contacts):                                                                       # Повертає номер телефону для заданого контакту
    if len(args) != 1:                                                              
        return "Invalid command. Please provide username."    
    name = args[0]                                                                  
    if name in contacts:                                                            
        return f"Phone number for {name}: {contacts[name]}"                         
    else:
        return f"Contact '{name}' not found."
    
@input_error
def update_phone(args, contacts):                                                                    # Оновлює номер телефону для заданного контакту
    if len(args) != 2:                                                              
        return "Invalid command. Please provide both username and new phone number."    
    name, new_phone = args                                                              
    if name in contacts:   
        if len(new_phone) == 10 and new_phone.isdigit():  
            contacts[name] = new_phone                                                     
            return "Contact updated."
        else:
            return "Invalid phone number. Please provide a valid 10-digit phone number for the contact."
    else:
        return f"Contact '{name}' not found."
    
def show_all_contacts(address_book):                                                    
    if address_book.data:                                                                           # Виводить всі контакти, збережені в адресній книзі
        print("All contacts:")
        for name, record in address_book.data.items():
            phones = ", ".join(record.phones)
            birthday = record.get_birthday() if record.birthday else "No birthday specified"
            print(f"Name: {name}, Phones: {phones}, Birthday: {birthday}")
    else:
        print("No contacts found.")

@input_error
def get_all_contacts(contacts):                                                                     # Повертає рядок, що містить всі контакти
    if not contacts:                                                                
        return "No contacts found."    
    result = "Contacts:\n"                                                          
    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"
    return result

@input_error
def delete_contact_by_name(args, address_book):                                                     # Видаляє контакт з адресної книги за ім'ям
    if len(args) != 1:
        return "Invalid command. Please provide the name of the contact to delete."
    name = args[0]
    if name in address_book.data:
        del address_book.data[name]
        return "Contact deleted."
    else:
        return f"Contact '{name}' not found."

@input_error
def delete_contact_by_phone(args, address_book):                                                    # Видаляє контакт з адресної книги за номером телефону
    if len(args) != 1:
            return "Invalid command. Please provide the phone number of the contact to delete."
    phone = args[0]
    for name, record in address_book.data.items():
        if phone in record.phones:
            del address_book.data[name]
            return "Contact deleted."
    return f"Contact with phone number '{phone}' not found."

@input_error
def add_birthday(args, address_book):                                                                # Додаємо контакту день народження
    if len(args) != 2:
        return "Invalid command. Please provide both username and birthday in the format 'DD-MM-YYYY'."
    name, birthday = args
    if name in address_book.data:
        try:
            if address_book.data[name].birthday:
                return "Birthday already exists for this contact. If you want to update it, please use the 'change_birthday' command."
            else:
                address_book.data[name].add_birthday(birthday)
                return "Birthday added."
        except ValueError as e:
            return str(e)
    else:
        return f"Contact '{name}' not found."
        
@input_error
def show_birthday(args, address_book):                                                              # Показує день народження для вказаного контакту
    if len(args) != 1:
        return "Invalid command. Please provide the name of the contact."
    name = args[0]
    if name in address_book.data:
        if address_book.data[name].birthday:
            birthday_date = address_book.data[name].birthday.get_value().strftime('%d-%m-%Y')
            return f"{name}'s birthday: {birthday_date}"
        else:
            return f"No birthday specified for {name}."
    else:
        return f"Contact '{name}' not found."

from datetime import datetime, timedelta

@input_error
def birthdays(args, address_book):                                                                  # Повертає список майбутніх днів народження наступного тижня
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    upcoming_birthdays = []

    for name, record in address_book.data.items():
        if record.birthday:
            birthday_date = record.birthday.get_value()
            if birthday_date.month == next_week.month and birthday_date.day in range(next_week.day - 6, next_week.day + 1):
                upcoming_birthdays.append((name, birthday_date.strftime('%d-%m-%Y')))

    if upcoming_birthdays:
        result = "Upcoming birthdays:\n"
        for name, birthday in upcoming_birthdays:
            result += f"{name}: {birthday}\n"
        return result
    else:
        return "No upcoming birthdays."
    
@input_error
def show_birthday(args, address_book):                                                              # Показує день народження для вказаного контакту
    if len(args) != 1:
        return "Invalid command. Please provide the name of the contact."
    name = args[0]
    if name in address_book.data:
        if address_book.data[name].birthday:
            return f"{name}'s birthday: {address_book.data[name].birthday.get_value().strftime('%d-%m-%Y')}"
        else:
            return f"No birthday specified for {name}."
    else:
        return f"Contact '{name}' not found."

def show_available_commands():                                                                       # Виводить список доступних команд                                          
    print("Available commands:")
    print("hello - Greet the bot")
    print("add <name> <phone> - Add a new contact")
    print("change <name> <phone> - Change the phone number of an existing contact")
    print("phone <name> - Get the phone number of a contact")
    print("all_contacts - Show all saved contacts")
    print("close/exit - Close the bot")
    print("search_records - Search contacts name or phone number")
    print("add_record - Add contacts")
    print("add_birthday <name> <DD-MM-YYYY> - Add birthday for a contact")
    print("delete_contact_by_name <name> - Delete a contact by name")
    print("delete_contact_by_phone <phone> - Delete a contact by phone number")
    print("show_birthday <name> - Show birthday for a contact")
    print("get_upcoming_birthdays - Show upcoming birthdays for the next week")

def main():    
    address_book = AddressBook()  
    print("Welcome to the assistant bot!")
    while True:        
        user_input = input("Enter a command: ")  
        command, args = parse_input(user_input)  
        
        if command in ["close", "exit"]:
            print("Good bye!")  
            break
        elif command == "hello":
            print("How can I help you?")  
        elif command == "add":                                                     
            print(add_record(args, address_book))
        elif command == "change":  
            print(change_contact(args, address_book))
        elif command == "phone":  
            print(get_phone(args, address_book))
        elif command == "all_contacts":  
            show_all_contacts(address_book)
        elif command == "add_birthday":
            print(add_birthday(args, address_book))
        elif command == "search_records":  
            print(search_records(args, address_book))
        elif command == "add_record":  
            print(add_record(args, address_book))
        elif command == "show_birthday":
            print(show_birthday(args, address_book))
        elif command == "delete_contact_by_name":
            print(delete_contact_by_name(args, address_book))
        elif command == "delete_contact_by_phone":
            print(delete_contact_by_phone(args, address_book))
        elif command == "get_upcoming_birthdays":
            address_book.show_upcoming_birthdays()
        elif command == "help":  
            show_available_commands()
        else:            
            print("Invalid command.")  


class Field:                                                                                         # Базовий клас для полів запису контакту
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def set_value(self, value):                                                    
        self.value = value

    def get_value(self):                                                           
        return self.value


class Name(Field):                                                                                  # Клас для зберігання імені контакту
    def __init__(self, name):
        super().__init__("Name", name)


class Phone:                                                                                        # Клас для зберігання номера телефону контакту
    def __init__(self, phone_number):
        self.value = phone_number
        self.validate_phone()

    def validate_phone(self):                                                                       # Перевіряє правильність формату номера телефону                                        
        if len(self.value) != 10 or not self.value.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")

    def set_value(self, phone_number):                                                              # Встановлює нове значення номера телефону
        self.value = phone_number        
        self.validate_phone()

    def get_value(self):                                                                            # Повертає поточне значення номера телефону                                               
        return self.value

from datetime import datetime

class Birthday(Field):                                                                              # Клас для зберігання дати народження контакту
    def __init__(self, value):
        try:
            self.set_value(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD-MM-YYYY")

    def set_value(self, value):
        try:
            self.value = datetime.strptime(value, '%d-%m-%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD-MM-YYYY")

    def get_value(self):
        return self.value

class Record:                                                                                       # Клас для зберігання запису контакту
    def __init__(self, name):                                                                       # Ініціалізує об'єкт запису контакту з ім'ям
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    @input_error
    def add_birthday(self, date):                                                                   # Додає дату народження до запису контакту
        if not date:
            return "Invalid birthday format. Please provide a valid date."
        try:
            self.birthday = Birthday(date)
            return "Birthday added."
        except ValueError as e:
            return str(e)
    
    def edit_birthday(self, date):                                                                  # Редагує дату народження в записі контакту                                                
        try:
            datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
            raise ValueError("Incorrect date format, should be DD-MM-YYYY.")
        self.birthday.set_date(date)

    def get_birthday(self):                                                                         # Повертає дату народження з запису контакту
        if self.birthday:
            return self.birthday.get_value().strftime('%d-%m-%Y')
        else:
            return None
        
    def add_phone(self, phone_number):                                                              # Додає номер телефону до запису контакту                                  
        if not re.match(r'^\d{10}$', phone_number):
            raise ValueError("Phone number must be a 10-digit number.")
        self.phones.append(phone_number)
    

    def remove_phone(self, phone_number):                                                           # Видаляє номер телефону з запису контакту                                      
        for phone in self.phones:
            if phone.get_value() == phone_number:
                self.phones.remove(phone)
                return "Phone number removed."
        return "Phone number not found."

    def edit_phone(self, old_phone_number, new_phone_number):                                       # Редагує номер телефону в запису контакту                  
        for phone in self.phones:
            if phone.get_value() == old_phone_number:
                try:
                    phone.set_value(new_phone_number)
                    return "Phone number updated."
                except ValueError as e:
                    return str(e)
        return "Phone number not found."

    def find_phone(self, phone_number):                                                             # Знаходить номер телефону в записі контакту                                      
        for phone in self.phones:
            if phone.get_value() == phone_number:
                return "Phone number found."
        return "Phone number not found."

from datetime import datetime, timedelta

class AddressBook:                                                                                  # Клас для зберігання адресної книги контактів.
    def __init__(self):                                                                             # Ініціалізує об'єкт адресної книги з порожнім словником контактів
        self.data = {}                                                             

    def add_record(self, name, phone, birthday=None):                                               # Додає новий запис контакту до адресної книги
        if name in self.data:
            return "Contact with this name already exists."
        record = Record(name)
        record.add_phone(phone)
        if birthday:
            record.add_birthday(birthday)
        self.data[name] = record
        return "Contact added."
    
    @input_error
    def add_birthday_to_record(self, args):                                                          # Додає дату народження до запису контакту у вказаній адресній книзі
        if len(args) != 2:
            return "Invalid command. Please provide both username and birthday in the format 'YYYY-MM-DD'."
        name, birthday = args
        if name in self.data:
            try:
                self.data[name].add_birthday(birthday)
                return "Birthday added."
            except ValueError as e:
                return str(e)
        else:
            return f"Contact '{name}' not found."
        
    def show_all_contacts(self):                                                                    # Виводить всі контакти, збережені в адресній книзі
        if self.data:
            print("All contacts:")
            for name, record in self.data.items():
                phones = ", ".join(record.phones)
                birthday = record.birthday.get_value().strftime('%d-%m-%Y') if record.birthday else "No birthday specified"
                print(f"Name: {name}, Phones: {phones}, Birthday: {birthday}")
        else:
            print("No contacts found.")
        
    def get_upcoming_birthdays(self):                                                               # Знаходить контакти з майбутніми днями народження наступного тижня
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                if record.birthday.get_value().date() < today:
                    birthday_this_year = datetime(today.year, record.birthday.get_value().month, record.birthday.get_value().day).date()
                    if birthday_this_year >= today and birthday_this_year < next_week:
                        upcoming_birthdays.append(record)

        return upcoming_birthdays

    def show_upcoming_birthdays(self):                                                              # Виводить на екран майбутні дні народження наступного тижня                                       
        upcoming_birthdays = self.get_upcoming_birthdays()
        if upcoming_birthdays:
            print("Upcoming birthdays:")
            for record in upcoming_birthdays:
                print(f"{record.name.get_value()}: {record.birthday.get_value().strftime('%d-%m-%Y')}")
        else:
            print("No upcoming birthdays")
if __name__ == "__main__":
    main()
