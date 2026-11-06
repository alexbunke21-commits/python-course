import json
import random
from getpass import getpass
from pathlib import Path
from tempfile import NamedTemporaryFile

TASKS_FILE = Path(__file__).with_name("tasks.json")
STATS_FILE = Path(__file__).with_name("stats.json")


def load_tasks():
    try:
        with TASKS_FILE.open(encoding="utf-8-sig") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Попередження: файл даних пошкоджено. Створюємо новий список.")
        return []
    except OSError as error:
        print(f"Не вдалося прочитати завдання: {error}")
        return None

    tasks = []
    if not isinstance(data, list):
        print("Попередження: у файлі завдань має бути список.")
        return None
    for task in data:
        if isinstance(task, str):
            tasks.append({"text": task, "done": False})
        elif (
            isinstance(task, dict)
            and isinstance(task.get("text"), str)
            and type(task.get("done")) is bool
        ):
            tasks.append(task)
        else:
            print("Попередження: файл містить запис невідомого формату.")
            return None
    return tasks


def write_json(path, data):
    temp_path = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False
        ) as file:
            temp_path = Path(file.name)
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")
        temp_path.replace(path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def save_tasks(tasks, updated_tasks):
    try:
        write_json(TASKS_FILE, updated_tasks)
    except OSError as error:
        print(f"Зміни не збережено: {error}")
        return False
    tasks[:] = updated_tasks
    return True


def load_stats():
    try:
        with STATS_FILE.open(encoding="utf-8-sig") as file:
            stats = json.load(file)
    except FileNotFoundError:
        return 0
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Попередження: статистику пошкоджено. Починаємо відлік заново.")
        return 0
    except OSError as error:
        print(f"Не вдалося прочитати статистику: {error}")
        return None

    sessions = stats.get("sessions") if isinstance(stats, dict) else None
    if type(sessions) is not int or sessions < 0:
        print("Попередження: статистику пошкоджено. Починаємо відлік заново.")
        return 0
    return sessions


def save_stats(sessions):
    try:
        write_json(STATS_FILE, {"sessions": sessions})
    except OSError as error:
        print(f"Не вдалося зберегти статистику: {error}")
        return False
    return True


def set_master_password():
    while True:
        password = getpass("Задайте головний пароль для цього сеансу: ")
        if password.strip():
            return password
        print("Головний пароль не може бути порожнім.")


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
        return
    for number, task in enumerate(tasks, start=1):
        status = "[x]" if task["done"] else "[ ]"
        print(f"{number}. {status} {task['text']}")


def select_task_index(tasks):
    show_tasks(tasks)
    if not tasks:
        return None

    entered_number = input("Введіть номер завдання: ").strip()
    if not entered_number.isdecimal():
        print("Введіть номер завдання цифрами.")
        return None

    try:
        number = int(entered_number)
    except ValueError:
        print("Неприпустимий номер завдання.")
        return None
    if not 1 <= number <= len(tasks):
        print("Завдання з таким номером немає.")
        return None
    return number - 1


def add_task(tasks):
    text = input("Введіть текст завдання: ").strip()
    if not text:
        print("Текст завдання не може бути порожнім.")
        return

    updated_tasks = [*tasks, {"text": text, "done": False}]
    if save_tasks(tasks, updated_tasks):
        print("Завдання додано.")


def delete_task(tasks):
    index = select_task_index(tasks)
    if index is None:
        return

    task_text = tasks[index]["text"]
    confirmation = input(f'Ви дійсно бажаєте видалити завдання "{task_text}"? (так/ні) ')
    if confirmation.strip().lower() != "так":
        print("Видалення скасовано.")
        return

    updated_tasks = tasks.copy()
    updated_tasks.pop(index)
    if save_tasks(tasks, updated_tasks):
        print("Завдання видалено.")


def complete_task(tasks):
    index = select_task_index(tasks)
    if index is None:
        return
    if tasks[index]["done"]:
        print("Це завдання вже виконано.")
        return

    updated_tasks = tasks.copy()
    updated_tasks[index] = {**tasks[index], "done": True}
    if save_tasks(tasks, updated_tasks):
        print("Завдання позначено виконаним.")


def suggest_task(tasks):
    pending = [task["text"] for task in tasks if not task["done"]]
    if not pending:
        print("Немає невиконаних завдань.")
        return
    print(f"Спробуйте виконати: {random.choice(pending)}")


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
    tasks = load_tasks()
    if tasks is None:
        return

    master_password = set_master_password()
    if not login_gate(master_password):
        return

    sessions = load_stats()
    if sessions is not None:
        sessions += 1
        if save_stats(sessions):
            print(f"Вітаємо! Це ваш {sessions}-й сеанс роботи з Менеджером задач")

    while True:
        print("\nМеню менеджера задач")
        print("1. Показати завдання")
        print("2. Додати завдання")
        print("3. Видалити завдання")
        print("4. Перевірити надійність пароля")
        print("5. Змінити головний пароль")
        print("6. Позначити завдання виконаним")
        print("7. Запропонувати випадкове невиконане завдання")
        print("0. Вийти")
        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            password = getpass("Введіть пароль для перевірки: ")
            print(f"Надійність пароля: {check_password_strength(password)}.")
        elif choice == "5":
            master_password = change_master_password(master_password)
        elif choice == "6":
            complete_task(tasks)
        elif choice == "7":
            suggest_task(tasks)
        elif choice == "0":
            return
        else:
            print("Невідомий пункт. Оберіть дію з меню.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nСеанс завершено.")
