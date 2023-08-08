from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbol = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_letters + password_symbol
    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    data = [web_input.get().lower(), email_input.get(), password_input.get()]
    dict_to_save = {
        data[0]: {
                            "email": data[1],
                            "password": data[2],
        }
    }

    if len(data[0]) == 0 or len(data[1]) == 0 or len(data[2]) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any field empty!")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(dict_to_save, file, indent=4)
        else:
            data.update(dict_to_save)

            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            web_input.delete(0, END)
            password_input.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #


def find_password():
    website = web_input.get().lower()
    try:
        with open("data.json", "r") as file:
            saved_data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="No Data File Found")
    else:
        if website in saved_data:
            data = saved_data.get(website)
            messagebox.showinfo(title=f"{website}", message=f"email: {data['Email']}\n"
                                                            f"Password: {data['password']}")
            pyperclip.copy(data['password'])
        else:
            messagebox.showinfo(title=f"Error", message=f"No detail for the {website} exist.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

web_label = Label(text="Website:", font=("Courier", 14))
web_label.grid(row=1, column=0)

web_input = Entry(width=21)
web_input.grid(row=1, column=1)
web_input.focus()

search = Button(text="Search", font=("Courier", 14), width=17, command=find_password)
search.grid(row=1, column=2)

email_label = Label(text="Email/Username:", font=("Courier", 14))
email_label.grid(row=2, column=0)

email_input = Entry(width=40)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(END, "max.chylij@gmail.com")

password_label = Label(text="Password:", font=("Courier", 14))
password_label.grid(row=3, column=0)

password_input = Entry(width=21)
password_input.grid(row=3, column=1)

gen_pass = Button(text="Generate Password", font=("Courier", 14), command=generate_password)
gen_pass.grid(row=3, column=2)

add_button = Button(text="Add", width=42, font=("Courier", 14), command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
