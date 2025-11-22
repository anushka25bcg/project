#transactions
import csv
from datetime import datetime
import uuid
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import os

filename = 'transactions.csv'

heading = ['ID', 'Date', 'Category', 'Amount']

if not os.path.exists(filename):
    with open(filename, 'w', newline='') as file:
        write = csv.writer(file, delimiter=',')
        write.writerow(heading)

def add_entry(filename):
    today = datetime.today().strftime("%b %d, %Y")
    entry_id = simpledialog.askstring("ID", "Enter ID:")  
    if entry_id is None:
        return
    category = simpledialog.askstring("Category", "Enter category:")
    if category is None:
        return
    amount = simpledialog.askfloat("Amount", "Enter amount:")
    if amount is None:
        return

    entry = [entry_id, today, category, amount]

    with open(filename, 'a', newline='') as file:
        write = csv.writer(file, delimiter=',')
        write.writerow(entry)

    messagebox.showinfo("Done", f"Entry added.\nID:{entry_id}")

def search_entry(filename):
    entry_id = simpledialog.askstring("Search", "Enter ID:")
    if entry_id is None:
        return
    
    with open(filename, 'r', newline='') as file:
        read = csv.reader(file, delimiter=',')
        for i in read:
            if i[0] == entry_id:
                msg = f"ID: {i[0]}\nDate: {i[1]}\nCategory: {i[2]}\nAmount: {i[3]}"
                messagebox.showinfo("Found", msg)
                return 
    messagebox.showwarning("Not found", "No entry with that ID.")
        
def modify_entry(filename):
    entry_id = simpledialog.askstring("Modify", "Enter ID to modify:")
    if entry_id is None:
        return
    rows = []
    updated = False
    with open(filename, 'r', newline='') as file:
        read = csv.reader(file, delimiter=',')
        for i in read:
            if i[0] == entry_id:
                new_category = simpledialog.askstring("Update category", "Enter new category:")
                if new_category is None:
                    rows.append(i)
                    continue
                new_amount = simpledialog.askfloat("Update amount", "Enter new amount:")
                if new_amount is None:
                    rows.append(i)
                    continue
                i[2] = new_category
                i[3] = str(new_amount)
                updated = True
            rows.append(i)
    if not updated:
        messagebox.showwarning("Not found", "Entry not found.")
        return
    
    with open(filename, 'w', newline='') as file:
        write = csv.writer(file, delimiter=',')
        write.writerows(rows)

    messagebox.showinfo("Done", "Entry updated.")
    
        
def delete_entry(filename):
    entry_id = simpledialog.askstring("Delete", "Enter ID to delete:")
    if entry_id is None:
        return
    rows = []
    found_row = None

    with open(filename, 'r', newline='') as file:
        read = csv.reader(file, delimiter=',')
        for i in read:
            if i[0] == entry_id:
                found_row = i
                continue
            rows.append(i)

        if not found_row:
            messagebox.showwarning("Not found", "Entry not found.")
            return
        
        with open(filename, 'w', newline='') as file:
            write = csv.writer(file, delimiter=',')
            write.writerows(rows)
        messagebox.showinfo("Deleted", "Entry deleted.")
        
def all_entry(filename):
    top = tk.Toplevel(root)
    top.title("All Entries")
    top.geometry("600x400")

    # Treeview for a nicer table view
    cols = heading
    tree = ttk.Treeview(top, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='center')

    vsb = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(top, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    top.grid_rowconfigure(0, weight=1)
    top.grid_columnconfigure(0, weight=1)

    # Insert rows
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 0:
                continue
            tree.insert('', 'end', values=row)
          
root = tk.Tk()
root.title("Transactions")

tk.Button(root, text="Add Entry", width=20, command=lambda: add_entry(filename)).pack(pady=5)
tk.Button(root, text="Search Entry", width=20, command=lambda: search_entry(filename)).pack(pady=5)
tk.Button(root, text="Modify Entry", width=25, command=lambda: modify_entry(filename)).pack(pady=5)
tk.Button(root, text="Delete Entry", width=25, command=lambda: delete_entry(filename)).pack(pady=5)
tk.Button(root, text="Show All Entries", width=25, command=lambda: all_entry(filename)).pack(pady=5)


root.mainloop()
