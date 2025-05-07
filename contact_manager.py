import json
import os
import re

CONTACTS_FILE = "contacts.json"

class Contact:
    def __init__(self, contact_id, name, phone, email):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            "id": self.contact_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }

class ContactManager:
    def __init__(self, filename):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                try:
                    data = json.load(file)
                    return {int(k): Contact(**v) for k, v in data.items()}
                except json.JSONDecodeError:
                    print("Error: Could not decode JSON data.")
                    return {}
        return {}

    def save_contacts(self):
        with open(self.filename, 'w') as file:
            json.dump({k: v.to_dict() for k, v in self.contacts.items()}, file, indent=4)

    def get_next_id(self):
        return max(self.contacts.keys(), default=0) + 1

    def validate_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def validate_phone(self, phone):
        return re.match(r"^\+?\d{7,15}$", phone)

    def add_contact(self):
        name = input("Enter name: ").strip()
        phone = input("Enter phone: ").strip()
        email = input("Enter email: ").strip()

        if not self.validate_phone(phone):
            print("Invalid phone number.")
            return

        if not self.validate_email(email):
            print("Invalid email address.")
            return

        contact_id = self.get_next_id()
        self.contacts[contact_id] = Contact(contact_id, name, phone, email)
        print("Contact added successfully.")

    def view_contacts(self):
        if not self.contacts:
            print("No contacts found.")
            return
        for contact in self.contacts.values():
            self.display_contact(contact)

    def search_contact(self):
        name = input("Enter name to search: ").strip().lower()
        found = False
        for contact in self.contacts.values():
            if name in contact.name.lower():
                self.display_contact(contact)
                found = True
        if not found:
            print("No matching contacts found.")

    def update_contact(self):
        try:
            contact_id = int(input("Enter contact ID to update: "))
            contact = self.contacts.get(contact_id)
            if not contact:
                print("Contact not found.")
                return

            print("Leave fields empty to keep current values.")
            name = input(f"New name ({contact.name}): ").strip()
            phone = input(f"New phone ({contact.phone}): ").strip()
            email = input(f"New email ({contact.email}): ").strip()

            if phone and not self.validate_phone(phone):
                print("Invalid phone number.")
                return

            if email and not self.validate_email(email):
                print("Invalid email address.")
                return

            contact.name = name or contact.name
            contact.phone = phone or contact.phone
            contact.email = email or contact.email

            print("Contact updated successfully.")
        except ValueError:
            print("Invalid ID entered.")

    def display_contact(self, contact):
        print(f"\nID: {contact.contact_id}")
        print(f"Name: {contact.name}")
        print(f"Phone: {contact.phone}")
        print(f"Email: {contact.email}")

    def run(self):
        while True:
            print("\n=== Contact Management System ===")
            print("1. Add Contact")
            print("2. View All Contacts")
            print("3. Search Contact by Name")
            print("4. Update Contact")
            print("5. Exit")
            choice = input("Enter your choice (1-5): ").strip()

            if choice == '1':
                self.add_contact()
            elif choice == '2':
                self.view_contacts()
            elif choice == '3':
                self.search_contact()
            elif choice == '4':
                self.update_contact()
            elif choice == '5':
                self.save_contacts()
                print("Contacts saved. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    manager = ContactManager(CONTACTS_FILE)
    manager.run()