import tkinter as tk
from tkinter import messagebox
import json
import os

# Проверка наличия JSON-файла, если его нет, создаем новый
if not os.path.isfile('notes.json'):
    with open('notes.json', 'w') as file:
        json.dump([], file)

# Функции для работы с JSON-файлом
def read_notes():
    with open('notes.json', 'r') as file:
        return json.load(file)

def write_notes(data):
    with open('notes.json', 'w') as file:
        json.dump(data, file, indent=4)

# Функции для работы с записями
def add_note():
    title = entry_title.get()
    content = text_content.get("1.0", "end-1c")
    if title and content:
        notes = read_notes()
        notes.append({"title": title, "content": content})
        write_notes(notes)
        update_notes_list()
        clear_entries()
    else:
        messagebox.showwarning("Предупреждение", "Заголовок и содержание не могут быть пустыми.")

def delete_note():
    try:
        index = listbox.curselection()[0]
        notes = read_notes()
        del notes[index]
        write_notes(notes)
        update_notes_list()
    except IndexError:
        messagebox.showwarning("Предупреждение", "Выберите запись для удаления.")

def update_notes_list():
    notes = read_notes()
    listbox.delete(0, tk.END)
    for note in notes:
        listbox.insert(tk.END, note["title"])

def clear_entries():
    entry_title.delete(0, tk.END)
    text_content.delete("1.0", tk.END)

def view_selected_note(event):
    try:
        index = listbox.curselection()[0]
        notes = read_notes()
        selected_note = notes[index]
        entry_title.delete(0, tk.END)
        entry_title.insert(0, selected_note["title"])
        text_content.delete("1.0", tk.END)
        text_content.insert("1.0", selected_note["content"])
    except IndexError:
        pass

# Создание GUI
root = tk.Tk()
root.title("Записная книжка")

frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=10, anchor="w")

label_title = tk.Label(frame_input, text="Заголовок:")
label_title.grid(row=0, column=0, sticky="w")

entry_title = tk.Entry(frame_input, width=50)
entry_title.grid(row=0, column=1, padx=5, pady=5)

label_content = tk.Label(frame_input, text="Содержание:")
label_content.grid(row=1, column=0, sticky="w")

text_content = tk.Text(frame_input, width=50, height=10)
text_content.grid(row=1, column=1, padx=5, pady=5)

button_add = tk.Button(frame_input, text="Добавить запись", command=add_note)
button_add.grid(row=2, column=1, pady=10)

frame_notes = tk.Frame(root)
frame_notes.pack(padx=10, pady=10, anchor="w")

label_notes = tk.Label(frame_notes, text="Записи:")
label_notes.pack()

listbox = tk.Listbox(frame_notes, width=50, height=10)
listbox.pack(padx=5, pady=5)
listbox.bind("<<ListboxSelect>>", view_selected_note)

button_delete = tk.Button(frame_notes, text="Удалить запись", command=delete_note)
button_delete.pack()

update_notes_list()

if __name__ == "__main__":
    root.mainloop()
