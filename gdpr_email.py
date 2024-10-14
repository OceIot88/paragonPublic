import hashlib
import nltk
from nltk.corpus import words
import tkinter as tk
from tkinter import messagebox
import re

# Загрузка словаря NLTK (если он еще не загружен)
nltk.download('words')

# Используем только английские слова
word_list = [word for word in words.words() if word.isalpha() and word.islower()]

def email_to_gdpr_english_only(email: str) -> str:
    # Приводим email к нижнему регистру
    email = email.lower()
    
    # Преобразуем email в хеш с помощью SHA-256
    email_hash = hashlib.sha256(email.encode('utf-8')).hexdigest()
    
    # Используем части хеша, чтобы выбирать два слова из словаря
    word1_index = int(email_hash[:8], 16) % len(word_list)
    word2_index = int(email_hash[8:16], 16) % len(word_list)
    
    # Собираем человеко-читаемый идентификатор из двух слов
    human_readable_id = word_list[word1_index].capitalize() + word_list[word2_index].capitalize()
    
    # Возвращаем email в формате GDPR
    return f"{human_readable_id}.gdpr@paragon-software.com"

# Проверка валидности email с использованием регулярного выражения
def is_valid_email(email: str) -> bool:
    # Регулярное выражение для проверки email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(regex, email)) and len(email) <= 254

# Создание функции для кнопки конвертации
def convert_email():
    email = entry.get()  # Получаем email из поля ввода
    if email:
        if is_valid_email(email):
            result = email_to_gdpr_english_only(email)
            result_entry.delete(0, tk.END)  # Очищаем поле вывода
            result_entry.insert(0, result)  # Вставляем результат
        else:
            messagebox.showerror("Ошибка", "Некорректный email. Проверьте формат.")
    else:
        messagebox.showerror("Ошибка", "Введите email!")

# Функция для копирования результата в буфер обмена
def copy_to_clipboard():
    result = result_entry.get()
    if result:
        root.clipboard_clear()
        root.clipboard_append(result)
        messagebox.showinfo("Успех", "Email скопирован в буфер обмена!")

# Создание графического интерфейса
root = tk.Tk()
root.title("GDPR Email Converter")

# Поле ввода email
entry_label = tk.Label(root, text="Введите email:")
entry_label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Кнопка для конвертации
convert_button = tk.Button(root, text="Конвертировать", command=convert_email)
convert_button.pack(pady=10)

# Поле для отображения результата
result_entry = tk.Entry(root, width=50)
result_entry.pack(pady=10)

# Кнопка для копирования в буфер обмена с символом юникода
copy_button = tk.Button(root, text="📋 Копировать", command=copy_to_clipboard)  # Используем символ юникода
copy_button.pack(pady=10)

# Запуск графического интерфейса
root.mainloop()
