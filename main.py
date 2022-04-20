"""
    Learn how to use tkinter - Password Manager GUI

    https://tkdocs.com/tutorial/canvas.html
    https://pypi.org/project/pyperclip/
"""
from tkinter import *
from tkinter import messagebox
import password_generator
import pyperclip

PASSWORD_FILE = "password.txt"
USER_NAME = "myemail@mail.com"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    random_password = password_generator.random_password()
    password_entry.insert(0, random_password)

    # put into clipboard
    pyperclip.copy(random_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    # Validation 1
    if 0 == len(website_entry.get().strip()) or \
            0 == len(email_entry.get().strip()) or \
            0 == len(password_entry.get().strip()):
        messagebox.showerror(title="Field Empty", message="Please fill all value")
        return

    # Validation 2
    try:
        with open(PASSWORD_FILE, mode="r") as password_file:
            password_text = password_file.readlines()
            password_lines = [line.split("|")[0].strip().lower() for line in password_text]
            if website_entry.get() in password_lines:
                messagebox.showerror(title="Duplicate Entry Found",
                                     message=f"Website {website_entry.get()} is exists please try other website")
                return
    except Exception as ex:
        print(ex)

    # Confirmation
    if not messagebox.askokcancel(title="Please Confirm", message=f"These are the the detail entered : \n"
                                                                  f"Website : {website_entry.get()} \n"
                                                                  f"Email : {email_entry.get()}\n"
                                                                  f"Password : {password_entry.get()}\n"
                                                                  f"Ok to Confirm"):
        return

    # Saving Entry
    with open(PASSWORD_FILE, mode="a") as password_file:
        password_file.write(
            f"{website_entry.get().strip()}|{email_entry.get().strip()}|{password_entry.get().strip()}\n")
        messagebox.showinfo(title="Success Save Password", message="Password is successfully Saved")

    # Clear Entry
    website_entry.delete(0, END)
    password_entry.delete(0, END)
    website_entry.insert(END, "https://")

    # Set Focus
    website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

logo = PhotoImage(file="logo.png")

canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

Label(text="Website:").grid(row=1, column=0)
Label(text="Email/username:").grid(row=2, column=0)
Label(text="Password:").grid(row=3, column=0)

website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

button_generate = Button(text="Generate Password", command=generate_password)
button_generate.grid(row=3, column=2)

button_add = Button(text="Add", width=36, command=save_password)
button_add.grid(row=4, column=1, columnspan=2)

website_entry.insert(END, "https://")
website_entry.focus()
email_entry.insert(0, USER_NAME)

window.mainloop()
