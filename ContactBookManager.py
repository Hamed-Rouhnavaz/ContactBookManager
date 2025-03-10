import tkinter as tk
from tkinter import ttk, messagebox
import json

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("600x400")
        
        self.contacts = []
        self.load_contacts()
        
        self.create_widgets()
        
    def load_contacts(self):
        try:
            with open("contacts.json", "r") as f:
                self.contacts = json.load(f)
        except FileNotFoundError:
            self.contacts = []

    def save_contacts(self):
        with open("contacts.json", "w") as f:
            json.dump(self.contacts, f)

    def create_widgets(self):
        # Left Frame - List
        list_frame = ttk.Frame(self.root)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.contact_list = tk.Listbox(list_frame, width=30)
        self.contact_list.pack(fill=tk.BOTH, expand=True)
        self.contact_list.bind("<<ListboxSelect>>", self.show_contact)
        
        # Right Frame - Details
        detail_frame = ttk.Frame(self.root)
        detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(detail_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(detail_frame, width=25)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(detail_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W)
        self.phone_entry = ttk.Entry(detail_frame, width=25)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(detail_frame, text="Email:").grid(row=2, column=0, sticky=tk.W)
        self.email_entry = ttk.Entry(detail_frame, width=25)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(detail_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add", command=self.add_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_contact).pack(side=tk.LEFT, padx=5)
        
        self.update_list()

    def update_list(self):
        self.contact_list.delete(0, tk.END)
        for contact in self.contacts:
            self.contact_list.insert(tk.END, contact["name"])

    def show_contact(self, event):
        selected = self.contact_list.curselection()
        if selected:
            index = selected[0]
            contact = self.contacts[index]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, contact["name"])
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, contact["phone"])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, contact["email"])

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        
        if name and phone:
            contact = {"name": name, "phone": phone, "email": email}
            self.contacts.append(contact)
            self.save_contacts()
            self.update_list()
            self.clear_entries()
        else:
            messagebox.showwarning("Warning", "Name and Phone are required!")

    def update_contact(self):
        selected = self.contact_list.curselection()
        if selected:
            index = selected[0]
            self.contacts[index] = {
                "name": self.name_entry.get(),
                "phone": self.phone_entry.get(),
                "email": self.email_entry.get()
            }
            self.save_contacts()
            self.update_list()

    def delete_contact(self):
        selected = self.contact_list.curselection()
        if selected:
            index = selected[0]
            del self.contacts[index]
            self.save_contacts()
            self.update_list()
            self.clear_entries()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()