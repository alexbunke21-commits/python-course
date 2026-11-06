from getpass import getpass


def verify_pin(pin):
    for attempt in range(1, 3):
        if getpass("Введіть PIN-код: ") == pin:
            return True
        print(f"Невірний PIN-код! Залишилося спроб: {2 - attempt}")

    print("Доступ до терміналу заблоковано.")
    return False


if __name__ == "__main__":
    demo_pin = getpass("Задайте PIN-код для демонстрації: ")
    if verify_pin(demo_pin):
        print("Доступ до терміналу дозволено.")
