import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import requests

class DesktopNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Note App")
        self.notes = {}
        self.load_notes()

        self.text = tk.Text(self.root, height=20, width=50)
        self.text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a frame at the bottom for the buttons
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, pady=10)

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(side=tk.BOTTOM, fill=tk.X)
        self.refresh_note_list()

        # Place the Backup Notes button in the bottom frame, aligned to the left
        backup_button = tk.Button(bottom_frame, text="Backup / Restore Notes", command=self.backup_or_restore_notes)
        backup_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(self.root, text="Save Note", command=self.save_note)
        save_button.pack(side=tk.LEFT)

        load_button = tk.Button(self.root, text="Load Note", command=self.load_note)
        load_button.pack(side=tk.LEFT)

        delete_button = tk.Button(self.root, text="Delete Note", command=self.delete_note)
        delete_button.pack(side=tk.LEFT)

    def save_note(self):
        note_title = simpledialog.askstring("Note Title", "Enter a title for your note:")
        note_text = self.text.get("1.0", tk.END).strip()
        if note_title and note_text:
            self.notes[note_title] = note_text
            self.refresh_note_list()
            self.text.delete("1.0", tk.END)
            messagebox.showinfo("Success", "Note saved successfully!")
        elif not note_text:
            messagebox.showerror("Error", "Note text cannot be empty.")

    def load_note(self):
        try:
            note_title = self.listbox.get(self.listbox.curselection())
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, self.notes[note_title])
        except tk.TclError:
            messagebox.showerror("Error", "Please select a note to load.")

    def delete_note(self):
        try:
            note_title = self.listbox.get(self.listbox.curselection())
            # Confirmation dialog before deleting a note
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{note_title}'?"):
                del self.notes[note_title]
                self.refresh_note_list()
                messagebox.showinfo("Success", "Note deleted successfully!")
        except tk.TclError:
            messagebox.showerror("Error", "Please select a note to delete.")

    def refresh_note_list(self):
        self.listbox.delete(0, tk.END)
        for title in self.notes.keys():
            self.listbox.insert(tk.END, title)

    def load_notes(self):
        if os.path.exists("notes.dat"):
            with open("notes.dat", "r") as file:
                self.notes = eval(file.read())

    def save_notes_to_file(self):
        with open("notes.dat", "w") as file:
            file.write(str(self.notes))
        self.root.destroy()

    def backup_or_restore_notes(self):
        # Create a Toplevel window
        popup = tk.Toplevel(self.root)
        popup.title("Backup or Restore")
        popup.geometry("300x100")  # Width x Height

        # Add a label
        label = tk.Label(popup, text="Choose an action:")
        label.pack(pady=10)

        # Add a Backup button
        backup_button = tk.Button(popup, text="Backup", command=lambda: [self.backup_notes(), popup.destroy()])
        backup_button.pack(side=tk.LEFT, padx=(20, 10), pady=10)

        # Add a Restore button
        restore_button = tk.Button(popup, text="Restore", command=lambda: [self.restore_notes_from_backup(), popup.destroy()])
        restore_button.pack(side=tk.RIGHT, padx=(10, 20), pady=10)
            
    def backup_notes(self):
        try:
            response = requests.post('http://localhost:5001/backup', json=self.notes)
            if response.status_code == 200:
                messagebox.showinfo("Backup", "Notes backed up successfully.")
            else:
                messagebox.showerror("Backup", "Failed to back up notes.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Backup", "Backup service is not running.")

    def restore_notes_from_backup(self):
        try:
            response = requests.get('http://localhost:5001/restore')
            if response.status_code == 200:
                self.notes = response.json()
                self.refresh_note_list()
                messagebox.showinfo("Restore", "Notes restored successfully from backup.")
            else:
                messagebox.showerror("Restore", "Failed to restore notes from backup.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Restore", "Restore service is not running.")

    def create_search_bar(self, frame):
        # Create a label for the search bar
        search_label = tk.Label(frame, text="Search Notes:")
        search_label.pack(side=tk.LEFT, padx=(0, 5))

        # Create an entry widget for the search bar
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        # Create a search button
        search_button = tk.Button(frame, text="Search", command=self.search_notes)
        search_button.pack(side=tk.LEFT, padx=(5, 0))

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.save_notes_to_file)
        
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopNoteApp(root)
    app.run()
