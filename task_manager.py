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
    while True:
        if getpass("Введіть головний пароль: ") == master_password:
            print("Вітаємо! Доступ дозволено.")
            return True
        print("Невірний пароль!")


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


def main():
    master_password = getpass("Задайте головний пароль для цього сеансу: ")
    login_gate(master_password)

    tasks = []
    while True:
        print("\nМеню менеджера задач")
        print("1. Показати завдання")
        print("2. Додати завдання")
        print("3. Видалити завдання")
        print("4. Перевірити надійність пароля")
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
        elif choice == "0":
            return
        else:
            print("Оберіть пункт із меню.")


if __name__ == "__main__":
    main()
