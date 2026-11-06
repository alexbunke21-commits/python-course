from getpass import getpass


def check_password_strength(password):
    if len(password) < 8:
        return "слабкий"
    if (
        any(char.islower() for char in password)
        and any(char.isupper() for char in password)
        and any(char.isdecimal() for char in password)
    ):
        return "сильний"
    return "середній"


def login_gate(master_password):
    for attempt in range(1, 4):
        if getpass("Введіть головний пароль: ") == master_password:
            print("Вітаємо! Доступ дозволено.")
            return True
        print(f"Невірний пароль! Залишилося спроб: {3 - attempt}")

    print("Доступ заблоковано через підозрілу активність!")
    return False


def show_tasks(tasks):
    if not tasks:
        print("Список завдань порожній.")
    for number, task in enumerate(tasks, start=1):
        print(f"{number}. {task}")


def delete_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return

    number = int(input("Введіть номер завдання: "))
    if not 1 <= number <= len(tasks):
        print("Завдання з таким номером немає.")
        return

    tasks.pop(number - 1)
    print("Завдання видалено.")


def change_master_password(master_password):
    for attempt in range(1, 3):
        if getpass("Підтвердьте поточний головний пароль: ") == master_password:
            break
        print(f"Невірний пароль! Залишилося спроб: {2 - attempt}")
    else:
        print("Зміну пароля скасовано.")
        return master_password

    new_password = getpass("Введіть новий головний пароль: ")
    if check_password_strength(new_password) == "слабкий":
        print("Помилка: новий пароль слабкий. Пароль не змінено.")
        return master_password

    print("Головний пароль змінено.")
    return new_password


def main():
    master_password = getpass("Задайте головний пароль для цього сеансу: ")
    access_granted = login_gate(master_password)
    if not access_granted:
        return

    tasks = []
    while True:
        print("\nМеню менеджера задач")
        print("1. Показати завдання")
        print("2. Додати завдання")
        print("3. Видалити завдання")
        print("4. Перевірити надійність пароля")
        print("5. Змінити головний пароль")
        print("0. Вийти")
        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            task = input("Введіть текст завдання: ").strip()
            if task:
                tasks.append(task)
                print("Завдання додано.")
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            password = getpass("Введіть пароль для перевірки: ")
            print(f"Надійність пароля: {check_password_strength(password)}.")
        elif choice == "5":
            master_password = change_master_password(master_password)
        elif choice == "0":
            return
        else:
            print("Оберіть пункт із меню.")


if __name__ == "__main__":
    main()
