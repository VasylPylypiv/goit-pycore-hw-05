def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid input format. Please check your data."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Missing argument. Please provide all required details."
        except Exception as e:
            # Загальний обробник для інших неочікуваних помилок
            return f"An unexpected error occurred: {e}"

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args



# Хендлер для додавання контакту
@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

# Хендлер для зміни контакту
@input_error
def change_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact changed."

# Модифікована функція для обробки команди phone
@input_error
def show_phone(args, contacts):
    if args:  # Перевіряємо, чи є аргумент (ім'я)
        name = args[0]  # Тільки перший аргумент, ім'я
        if name in contacts:
            return contacts[name]
        else:
            return f"Contact with name '{name}' not found."
    else:
        return "Please provide a name after 'phone'." # Якщо аргументів немає

# Хендлер для виведення всіх контактів
@input_error
def show_all(contacts):
    if contacts:
        contact_list = []
        for name, phone in contacts.items():
            contact_list.append(f"Name: {name}, Phone: {phone}")
        return "\n".join(contact_list)  # Повертаємо форматований рядок
    else:
        return "No contacts found."

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))  # Викликаємо show_phone для обробки команди
        elif command == "all":
            print(show_all(contacts))  # Виводимо через main
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()