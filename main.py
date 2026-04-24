import tkinter as tk
from tkinter import ttk, messagebox
import json

# Основное окно
root = tk.Tk()
root.title("Book Tracker")
root.geometry("700x600")  # Размер окна

# Глобальный список книг
books = []

# --- Поля для ввода данных ---
label_title = tk.Label(root, text="Название книги")
entry_title = tk.Entry(root)

label_author = tk.Label(root, text="Автор")
entry_author = tk.Entry(root)

label_genre = tk.Label(root, text="Жанр")
entry_genre = tk.Entry(root)

label_pages = tk.Label(root, text="Количество страниц")
entry_pages = tk.Entry(root)

# Размещение в сетке
label_title.grid(row=0, column=0, padx=5, pady=5, sticky='w')
entry_title.grid(row=0, column=1, padx=5, pady=5, sticky='we')

label_author.grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_author.grid(row=1, column=1, padx=5, pady=5, sticky='we')

label_genre.grid(row=2, column=0, padx=5, pady=5, sticky='w')
entry_genre.grid(row=2, column=1, padx=5, pady=5, sticky='we')

label_pages.grid(row=3, column=0, padx=5, pady=5, sticky='w')
entry_pages.grid(row=3, column=1, padx=5, pady=5, sticky='we')

# --- Функции ---
def clear_entries():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_pages.delete(0, tk.END)

def update_table(display_books=None):
    """
    Обновляет таблицу книг.
    Если передать display_books, отображает именно их.
    Иначе — все книги из глобального списка.
    """
    for row in tree.get_children():
        tree.delete(row)
    list_to_display = display_books if display_books is not None else books
    for book in list_to_display:
        tree.insert('', tk.END, values=(book['title'], book['author'], book['genre'], book['pages']))

def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = entry_genre.get().strip()
    pages = entry_pages.get().strip()

    # Проверка заполненности
    if not title or not author or not genre or not pages:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
        return

    # Проверка на число для страниц
    if not pages.isdigit():
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
        return

    book = {
        "title": title,
        "author": author,
        "genre": genre,
        "pages": int(pages)
    }
    books.append(book)
    update_table()
    clear_entries()

def save_to_json():
    try:
        with open('books.json', 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в books.json")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

def load_from_json():
    global books
    try:
        with open('books.json', 'r', encoding='utf-8') as f:
            books = json.load(f)
        update_table()
    except FileNotFoundError:
        # файл еще не создан — ничего не делаем
        pass
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")

def apply_filter():
    genre_filter = genre_filter_var.get().strip().lower()
    pages_filter = pages_filter_var.get().strip()

    filtered_books = []

    # Проверка
    if pages_filter and not pages_filter.isdigit():
        messagebox.showerror("Ошибка", "Больше страниц должно быть числом")
        return

    for book in books:
        if genre_filter and genre_filter not in book['genre'].lower():
            continue
        if pages_filter:
            if book['pages'] <= int(pages_filter):
                continue
        filtered_books.append(book)

    update_table(display_books=filtered_books)

# --- Кнопки и фильтр ---
add_button = tk.Button(root, text="Добавить книгу", command=add_book)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Таблица (Treeview)
columns = ("title", "author", "genre", "pages")
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col.title())

tree.grid(row=5, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

# Настройка расширения
root.rowconfigure(5, weight=1)
root.columnconfigure(1, weight=1)

# Фильтр
filter_frame = tk.Frame(root)
filter_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky='ew')

tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=5)
genre_filter_var = tk.StringVar()
genre_filter_entry = tk.Entry(filter_frame, textvariable=genre_filter_var)
genre_filter_entry.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Больше страниц:").grid(row=0, column=2, padx=5)
pages_filter_var = tk.StringVar()
pages_filter_entry = tk.Entry(filter_frame, textvariable=pages_filter_var)
pages_filter_entry.grid(row=0, column=3, padx=5)

filter_button = tk.Button(filter_frame, text="Применить фильтр", command=apply_filter)
filter_button.grid(row=0, column=4, padx=5)

# --- Кнопки сохранения/загрузки ---
save_button = tk.Button(root, text="Сохранить в JSON", command=save_to_json)
save_button.grid(row=7, column=0, pady=10)

load_button = tk.Button(root, text="Загрузить из JSON", command=load_from_json)
load_button.grid(row=7, column=1, pady=10)

# --- Загрузка данных при запуске ---
load_from_json()

# Запуск главного цикла
root.mainloop()
