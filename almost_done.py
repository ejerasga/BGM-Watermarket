from tkinter import *
from tkinter import messagebox
from logging import root
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import smtplib
from email.message import EmailMessage
import sqlite3
import csv
import tkinter.filedialog as filedialog
import sqlite3
#import xlsxwriter
from tkinter import filedialog
import datetime as dt




######################################################################################################

# Inventory

def invent():
    
    roots = tk.Tk()
    roots.title("Inventory")
    roots.config(bg="#1F375D")
    roots.state("zoomed")
    
    def back():
        update_frame()
        roots.destroy()
        

    conn = sqlite3.connect('water_market_quezon.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS inventory
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL);''')


    
    
    

    # create labels and entry widgets for input
    title = tk.Label(roots, text="Inventory", font=("Arial Rounded MT Bold", 25), bg="#1F375D", fg="white")
    name_label = tk.Label(roots, text="Name", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    name_entry = tk.Entry(roots, bg="#ADDFDE", font=("Arial Rounded MT Bold", 16))
    quantity_label = tk.Label(roots, text="Quantity", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    quantity_entry = tk.Entry(roots, bg="#ADDFDE", font=("Arial Rounded MT Bold", 16))
    price_label = tk.Label(roots, text="Price", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    price_entry = tk.Entry(roots, bg="#ADDFDE", font=("Arial Rounded MT Bold", 16))

    # create a function to add inventory items to the database
    def add_item():
        name = name_entry.get()
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())
        conn.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)",
                    (name, quantity, price))
        conn.commit()
        view_items()
        
        # clear the input fields
        name_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)

    # create a function to view all inventory items in the database
    def view_items():
        treeview.delete(*treeview.get_children())
        cursor = conn.execute("SELECT * FROM inventory")
        for row in cursor:
            treeview.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))

    # create a function to edit an inventory item in the database
    def edit_item():
        selected_item = treeview.selection()[0]
        item_id = treeview.item(selected_item)['values'][0]
        new_name = name_entry.get()
        new_quantity = quantity_entry.get()
        new_price = price_entry.get()
        conn.execute("UPDATE inventory SET name=?, quantity=?, price=? WHERE id=?",
                    (new_name, new_quantity, new_price, item_id))
        conn.commit()
        view_items()
        
        # clear the input fields
        name_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)

    # create a function to delete an inventory item from the database
    def delete_item():
        selected_item = treeview.selection()[0]
        item_id = treeview.item(selected_item)['values'][0]
        conn.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        conn.commit()
        view_items()
        
        # clear the input fields
        name_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)

    # create a function to display the selected item's details in a text box
    def display_selected_item(event):
        selected_item = treeview.selection()[0]
        item_id, item_name, item_quantity, item_price = treeview.item(selected_item)['values']
        name_entry.delete(0, tk.END)
        name_entry.insert(0, item_name)
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, item_quantity)
        price_entry.delete(0, tk.END)
        price_entry.insert(0, item_price)

    # create a Treeview widget to display inventory items
    treeview = ttk.Treeview(roots, columns=("id", "name", "quantity", "price"), show="headings")
    treeview.heading("id", text="ID")
    treeview.heading("name", text="Name")
    treeview.heading("quantity", text="Quantity")
    treeview.heading("price", text="Price")
    treeview.grid(row=6, column=2, columnspan=2)
    
    treeview.column("id", anchor="center")
    treeview.column("name", anchor="center")
    treeview.column("quantity", anchor="center")
    treeview.column("price", anchor="center")
    
    style = ttk.Style(roots)
    style.configure("Treeview", font=("Arial", 10))


    # bind the Treeview to display the selected item's details in a text box
    treeview.bind("<ButtonRelease-1>", display_selected_item)
    
    ##########################################################################################
    # EXport to CSV
    
    def export_data():
        # prompt user for filename and location to save the CSV file
        file_path = filedialog.asksaveasfilename(defaultextension=".csv")

        # execute SELECT query to get all data in inventory table
        cursor = conn.execute("SELECT * FROM inventory")
        rows = cursor.fetchall()

        # write data to CSV file
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # write header row
            writer.writerow(['ID', 'Name', 'Quantity', 'Price'])
            # write data rows
            for row in rows:
                writer.writerow(row)

        print(f"Data exported to {file_path}")
        
    export_button = tk.Button(roots, text="Export Data", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command=export_data)
    export_button.grid(row=7, column=3, pady=10)
    
##########################################################################################
    
    

    # create buttons for editing and deleting inventory items
    edit_button = tk.Button(roots, text="Edit Item", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command=edit_item)
    delete_button = tk.Button(roots, text="Delete Item", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command=delete_item)
    edit_button.grid(row=7, column=1, pady=10)
    delete_button.grid(row=7, column=2, pady=10)

    # create a button to add inventory items to the database
    add_button = tk.Button(roots, text="Add Item", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command=add_item)
    add_button.grid(row=5, column=3, padx=10, pady=10)
    
    back = tk.Button(roots, text="Back to Update", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command=back)
    back.grid(row=7, column=4, pady=10)

    # grid the widgets in the Tkinter window
    title.grid(row=0, column=3, pady=20)
    name_label.grid(row=1, column=2)
    name_entry.grid(row=1, column=3)
    quantity_label.grid(row=2, column=2)
    quantity_entry.grid(row=2, column=3)
    price_label.grid(row=3, column=2)
    price_entry.grid(row=3, column=3)

    # view all inventory items when the program starts
    view_items()


######################################################################################################
######################################################################################################
'''
# Database
# Create a Database
conn = sqlite3.connect('water_market.db')

# Create a Cursor
c = conn.cursor()

# Commit Changes
conn.commit()

# Close Connection
conn.close()
'''


######################################################################################################

# Login Frame
login = Tk()
login.title("Water Market Management System")
login.geometry('600x440')
login.configure(bg='#1F375D') # Window main Background

'''
p1 = PhotoImage(file = 'images\Logo.PNG')
  
# Setting icon of master window
login.iconphoto(False, p1)
'''
        
              
frame = Frame(bg='#1F375D')   # Frame Background

# Creating widgets
img = ImageTk.PhotoImage(Image.open('images\logo_with_name.png'))
imglbl = Label(frame, image = img, borderwidth=0)
imglbl.grid(row = 0, column = 1, pady = 40)

#login_label = Label(frame, text="Login", bg='#1F375D', fg="#FFFFFF", font=("Arial Rounded MT Bold", 30))
username_label = Label(frame, text="Username:", bg='#1F375D', fg="#FFFFFF", font=("Arial Rounded MT Bold", 16))
username_entry = Entry(frame, bg="#ADDFDE", font=("Arial Rounded MT Bold", 16))
password_entry = Entry(frame, bg="#ADDFDE", show="*", font=("Arial Rounded MT Bold", 16))
password_label = Label(frame, text="Password:", bg='#1F375D', fg="#FFFFFF", font=("Arial Rounded MT Bold", 16))
login_button = Button(frame, text="Login", bg="#ADDFDE", fg="#0f0f0f", font=("Arial Rounded MT Bold", 16), command = lambda:dashboard(username_entry.get(), password_entry.get()))


# Placing widgets on the screen
#login_label.grid(row = 0, column = 1, pady = 40)
username_label.grid(row = 1, column = 0)
username_entry.grid(row = 1, column = 1, pady = 20)
password_label.grid(row = 2, column = 0)
password_entry.grid(row = 2, column = 1, pady = 20)
login_button.grid(row = 3, column = 1, pady = 30)

frame.pack()

######################################################################################################
'''

# Email Frame
def send_email():
    

    
    
    main_frame = Frame(bg='#1F375D').pack()
    
    
    
    def send_emails():
        

            
        
        
        
        
    
        msg = EmailMessage()
        msg["Subject"] = subject.get()
        #msg["From"] = sender.get()
        msg["To"] = receiver.get()
        msg.set_content(t_text.get("1.0", "end-1c"))

        try:
            with smtplib.SMTP(msg["To"], 465) as smtp: #port must be modifyed by user
                smtp.send_message(msg)
                Label(main_frame, text="Email sent successfully", background="#1F375D", foreground="green", font=("Calibri", 25)).place(relx=0.6, rely=0.9, width=300, height=30)
        except:
            messagebox.showinfo(title="Success", message="Email Send Successfully")
            #Label(text="Email sent successfully", background="#1F375D", foreground="green", font=("Calibri", 25)).place(relx=0.6, rely=0.9, width=300, height=30)



        email = "ejerasga123@gmail.com"
        password = "glvpewmsdhbsnkkb"
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)
            
    
        


    # ---------  GUI(Graphic user interface)  --------- #
    

    #sender = StringVar()
    receiver = StringVar()
    subject = StringVar()

    

    w_lable = Label(main_frame, text="Send Email", background="#1F375D", foreground="white", font=("Arial Rounded MT Bold", 30))
    w_lable.place(relx=0.5, rely=0.05, anchor=CENTER)

    #s_lable = Label(main_frame, text="Your Email:", background="#1F375D", foreground="white", font=("Arial Rounded MT Bold", 12))
    #s_lable.place(relx=0.1, rely=0.1, width=200, height=30)

    #s_entry = Entry(main_frame, textvariable=sender)
    #s_entry.place(relx=0.3, rely=0.1, width=600, height=30)

    r_lable = Label(main_frame, text="Reciver Email:", background="#1F375D", foreground="white", font=("Arial Rounded MT Bold", 14))
    r_lable.place(relx=0.1, rely=0.17, width=200, height=30)

    r_entry = Entry(main_frame, textvariable=receiver, font=("Arial", 12))
    r_entry.place(relx=0.3, rely=0.17, width=530, height=30)

    sub_lable = Label(main_frame, text="Email Subject:", background="#1F375D", foreground="white", font=("Arial Rounded MT Bold", 14))
    sub_lable.place(relx=0.1, rely=0.25, width=200, height=30)

    sub_entry = Entry(main_frame, textvariable=subject, font=("Arial", 12))
    sub_entry.place(relx=0.3, rely=0.25, width=530, height=30)

    t_lable = Label(main_frame, text="Message:", background="#1F375D", foreground="white", font=("Arial Rounded MT Bold", 14))
    t_lable.place(relx=0.1, rely=0.33, width=90, height=30)

    t_text = Text(main_frame, font=("Arial", 12))
    t_text.place(relx=0.11, rely=0.37, width=790, height=300)

    s_button = Button(main_frame, text="SEND EMAIL", font=("Arial Rounded MT Bold", 14), fg="black", bg="#ADDFDE" , command=lambda:send_emails())
    s_button.place(relx=0.11, rely=0.85, width=180, height=40)
    
    back_button = Button(main_frame, text="Update", font=("Arial Rounded MT Bold", 14), fg="black", bg="#ADDFDE", command=update_frame)
    back_button.place(relx=0.30, rely=0.85, width=180, height=40)
    
    add_button = Button(main_frame, text="Add", font=("Arial Rounded MT Bold", 14), fg="black", bg="#ADDFDE", command=add_frame)
    add_button.place(relx=0.50, rely=0.85, width=180, height=40)
    
   
    

'''   
    
    
    


######################################################################################################

# Add Frame
def add_frame():
    #login.destroy()
    
    root = Tk()
    
    root.title("Water Market Management System")
    root.geometry("1920x1080+0+0") # Try 1700x800
    root.config(bg="#1F375D")
    root.state("zoomed")
    
    
    def destroy():
        update_frame()
        root.destroy()
    
    
    


    # Entries Frame
    entries_frame = Frame(root, bg="#1F375D")
    entries_frame.pack(side=TOP, fill=X)
    
    customer_title = Label(entries_frame, text="Customer", font=("Arial Rounded MT Bold", 30),fg='white', bg="#1F375D")
    customer_title.grid(row=0, column=1, pady=40)

    menu_title = Label(entries_frame, text="Menu", font=("Arial Rounded MT Bold", 30),fg='white', bg="#1F375D")
    menu_title.grid(row=0, column=3, pady=20)
    
######################################################################################################

    # Left Side
            
    lblName = Label(entries_frame, text="Name:", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    lblName.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    #lblName.place(relx = 0.0, rely = 1.0, anchor ='sw')
    txtName = Entry(entries_frame, font=("Arial Rounded MT Bold", 16), width=30, bg="#ADDFDE")
    txtName.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    #txtName.place(relx = 0.0, rely = 2.0, anchor ='sw')


    lbl_Email = Label(entries_frame, text="Email:", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    lbl_Email.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    txt_Email = Entry(entries_frame, font=("Arial Rounded MT Bold", 16), width=30, bg="#ADDFDE")
    txt_Email.grid(row=2, column=1, padx=10, pady=10, sticky="w")


    lblContact = Label(entries_frame, text="Contact No:", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    lblContact.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    txt_Contact = Entry(entries_frame, font=("Arial Rounded MT Bold", 16), width=30, bg="#ADDFDE")
    txt_Contact.grid(row=3, column=1, padx=10, sticky="w")
    
    
    lblAddress = Label(entries_frame, text="Address:", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    lblAddress.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    txtAddress = Entry(entries_frame, font=("Arial Rounded MT Bold", 16), width=30, bg="#ADDFDE")
    txtAddress.grid(row=4, column=1, columnspan=4, padx=10, pady=10, sticky="w")
    
    
    lblID = Label(entries_frame, text="ID:", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    lblID.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    txt_ID = Entry(entries_frame, font=("Arial Rounded MT Bold", 16), width=10, bg="#ADDFDE")
    txt_ID.grid(row=5, column=1, padx=10, sticky="w")



######################################################################################################################################

    # Right Side | Menu

    lblMenu1 = Label(entries_frame, text="Container:", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    lblMenu1.grid(row=1, column=2, pady=10)
    txtMenu1 = Entry(entries_frame, font=("Arial Rounded MT Bold", 16), width=15, bg="#ADDFDE")
    txtMenu1.grid(row=1, column=3, pady=10)
    

    lblMenu2 = Label(entries_frame, text="Faucet:", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    lblMenu2.grid(row=2, column=2, pady=10)
    txtMenu2 = Entry(entries_frame, font=("Arial Rounded MT Bold", 16), width=15, bg="#ADDFDE")
    txtMenu2.grid(row=2, column=3, pady=10)


    lblMenu3 = Label(entries_frame, text="Gallon:", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    lblMenu3.grid(row=3, column=2, pady=10)
    txtMenu3 = Entry(entries_frame, font=("Arial Rounded MT Bold", 16), width=15, bg="#ADDFDE")
    txtMenu3.grid(row=3, column=3)
    
    
    lblMenu4 = Label(entries_frame, text="Mineral:", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    lblMenu4.grid(row=1, column=4, pady=10, padx=10)
    txtMenu4 = Entry(entries_frame, font=("Arial Rounded MT Bold", 16), width=10, bg="#ADDFDE")
    txtMenu4.grid(row=1, column=5)
    
    
    lblMenu5 = Label(entries_frame, text="Alkaline:", font=("Arial Rounded MT Bold", 16), bg="#1F375D", fg="white")
    lblMenu5.grid(row=2, column=4, pady=10, padx=10)
    txtMenu5 = Entry(entries_frame, font=("Arial Rounded MT Bold", 16), width=10, bg="#ADDFDE")
    txtMenu5.grid(row=2, column=5)
    
    '''
    # Create Qeury Function
    def query():
        conn = sqlite3.connect('water_market.db')

        # Create a Cursor
        c = conn.cursor()
        
        #Query the Database
        c.execute("SELECT")############# DI PA TAPOS ##############
        
        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()
    '''
    
    
########################################################################################################    
    # Submit function to Database
    def add_data():
        
        # Create a Database
        conn = sqlite3.connect('water_market_quezon.db')

        # Create a Cursor
        c = conn.cursor()
        
        # Add New Record
        c.execute("INSERT INTO customers VALUES (:txt_ID, :txtName, :txt_Email, :txt_Contact, :txtAddress, :txtMenu1, :txtMenu2, :txtMenu3, :txtMenu4, :txtMenu5)",
                  {
                      'txt_ID': txt_ID.get(),
                      'txtName': txtName.get(),
                      'txt_Email': txt_Email.get(),
                      'txt_Contact': txt_Contact.get(),
                      'txtAddress': txtAddress.get(),
                      'txtMenu1': txtMenu1.get(),
                      'txtMenu2': txtMenu2.get(),
                      'txtMenu3': txtMenu3.get(),
                      'txtMenu4': txtMenu4.get(),
                      'txtMenu5': txtMenu5.get()
                  })
        
        
        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()
        
        txt_ID.delete(0, END)
        txtName.delete(0, END)
        txt_Email.delete(0, END)
        txt_Contact.delete(0, END)
        txtAddress.delete(0, END)
        txtMenu1.delete(0, END)
        txtMenu2.delete(0, END)
        txtMenu3.delete(0, END)
        txtMenu4.delete(0, END)
        txtMenu5.delete(0, END)
        
        # Add Message Box
        #messagebox.showinfo("Added!", "Your Record Has Been Added!")
        
        
        
        '''
        # Insert Into table
        c.execute("INSERT INTO addresses VALUES (:txtName, :txt_Email, :txt_Contact, :txtAddress, :txtMenu1, :txtMenu2, :txtMenu3, :txtMenu4, :txtMenu5)",
                  {
                      'txtName': txtName.get(),
                      'txt_Email': txt_Email.get(),
                      'txt_Contact': txt_Contact.get(),
                      'txtAddress': txtAddress.get(),
                      'txtMenu1': txtMenu1.get(),
                      'txtMenu2': txtMenu2.get(),
                      'txtMenu3': txtMenu3.get(),
                      'txtMenu4': txtMenu4.get(),
                      'txtMenu5': txtMenu5.get()
                  })
        #messagebox.showinfo("Success", "Record Inserted")
        '''
        '''
        # Create a query button
        query_btn = Button(entries_frame, text="Show Records", command=query)
        query_btn.grid(row=5, column=4, pady=20, padx=10, width=15, font=("Calibri", 16, "bold"), fg="white", bg="#5885ed")
        '''

        # Commit Changes
        #conn.commit()

        # Close Connection
        #conn.close()
        
        
    # Clear The Text Boxes
    def clear_All():
        
        txt_ID.delete(0, END)
        txtName.delete(0, END)
        txt_Email.delete(0, END)
        txt_Contact.delete(0, END)
        txtAddress.delete(0, END)
        txtMenu1.delete(0, END)
        txtMenu2.delete(0, END)
        txtMenu3.delete(0, END)
        txtMenu4.delete(0, END)
        txtMenu5.delete(0, END)
        
    

    
######################################################################################################################################            

    # Buttons
    
    #btn_frame = Frame(entries_frame, bg="#333333")
    #btn_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")
    
    btnAdd = Button(entries_frame, text="Add Details", width=15, font=("Arial Rounded MT Bold", 16), fg="#0f0f0f",
                    bg="#ADDFDE", bd=0, command=add_data).grid(row=6, column=1, padx=20, pady=20)
    #btnEdit = Button(btn_frame, text="Update Details", width=15, font=("Calibri", 16, "bold"),
                    #fg="white", bg="#5885ed",
                    #bd=0).grid(row=0, column=1, padx=10)
    #btnDelete = Button(btn_frame, text="Delete Details", width=15, font=("Calibri", 16, "bold"),
                    #fg="white", bg="#5885ed",
                    #bd=0).grid(row=0, column=2, padx=10)
    btnClear = Button(entries_frame, text="Clear Details", width=15, font=("Arial Rounded MT Bold", 16), fg="#0f0f0f",
                    bg="#ADDFDE",
                    bd=0, command=clear_All).grid(row=6, column=2, pady=20, padx=20)
    
    #email_button = Button(entries_frame, text="Send Email", font=("Arial Rounded MT Bold", 16), command=send_email)
    #email_button.grid(row=6, column=4, padx=10, pady=10)
    
    update_button = Button(entries_frame, text="Go to Update", width=15, font=("Arial Rounded MT Bold", 16), fg="#0f0f0f",
                    bg="#ADDFDE",
                    bd=0, command=destroy)
    update_button.grid(row=6, column=3, padx=50, pady=20)
    
    
    
    


######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
def send_email():
    msg = EmailMessage()
    msg["Subject"] = subject.get()
    msg["To"] = receiver.get()
    msg.set_content(t_text.get("1.0", "end-1c"))

    try:
        with smtplib.SMTP(msg["To"], 465) as smtp: #port must be modifyed by user
            smtp.send_message(msg)
            Label(root, text="Email sent successfully", background="#1A3D56", foreground="green", font=("Calibri", 16)).place(relx=0.6, rely=0.9, width=300, height=30)
    except:
        Label(root, text="Email sent successfully", background="#1A3D56", foreground="green", font=("Calibri", 16)).place(relx=0.7, rely=0.9, width=300, height=30)

    email = "ejerasga123@gmail.com"
    password = "glvpewmsdhbsnkkb"

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(msg)

def email_sender_window():
    global root
    root = Toplevel()
    root.title("Email Sender")
    #root.state("zoomed")
    #root.configure(bg="#1A3D56")
    
    
    
    
        

    global sender, receiver, subject, t_text

    sender = StringVar()
    receiver = StringVar()
    subject = StringVar()

    canvas = Canvas(root, width=1000, height=700, background="#1A3D56")
    canvas.pack()

    w_lable = Label(root, text="Email Sender", background="#1A3D56", foreground="white", font=("Arial Rounded MT Bold", 30))
    w_lable.place(relx=0.5, rely=0.05, anchor=CENTER)

    r_lable = Label(root, text="Receiver Email:", background="#1A3D56", foreground="white", font=("Arial Rounded MT Bold", 14))
    r_lable.place(relx=0.1, rely=0.17, width=200, height=30)

    r_entry = Entry(root, textvariable=receiver, font=("Arial", 12))
    r_entry.place(relx=0.3, rely=0.17, width=600, height=30)

    sub_lable = Label(root, text="Email Subject:", background="#1A3D56", foreground="white", font=("Arial Rounded MT Bold", 14))
    sub_lable.place(relx=0.1, rely=0.3, width=200, height=30)

    sub_entry = Entry(root, textvariable=subject, font=("Arial", 12))
    sub_entry.place(relx=0.3, rely=0.3, width=600, height=30)

    t_lable = Label(root, text="Text:", background="#1A3D56", foreground="white", font=("Arial Rounded MT Bold", 14))
    t_lable.place(relx=0.05, rely=0.4, width=200, height=30)

    t_text = Text(root)
    t_text.place(relx=0.11, rely=0.45, width=790, height=300)

    s_button = Button(root, text="SEND EMAIL", font=("Arial Rounded MT Bold", 14), fg="black", bg="#ADDFDE", command=send_email)
    s_button.place(relx=0.11, rely=0.9, width=200, height=30)
    
    b_button = Button(root, text="Close", font=("Arial Rounded MT Bold", 14), fg="black", bg="#ADDFDE", command=root.destroy)
    b_button.place(relx=0.5, rely=0.9, width=200, height=30)

######################################################################################################################################
######################################################################################################################################
######################################################################################################################################

# Update Frame
def update_frame():
    #login.destroy()
    
    
    
    
    root2 = Tk()
    root2.title("Water Market Management System")
    root2.geometry("1920x1080+0+0") # Try 1700x800
    root2.config(bg="#1F375D")
    root2.state("zoomed")
    
    def close():
        add_frame()
        root2.destroy()
        
        
    def close1():
        invent()
        root2.destroy()
            
    
    
    
    def query_database():
        
        for record in my_tree.get_children():
            my_tree.delete(record)
        
        # Create a Database
        conn = sqlite3.connect('water_market_quezon.db')

        # Create a Cursor
        c = conn.cursor()
        
        c.execute("SELECT rowid, * FROM customers")
        records = c.fetchall()
        
        # Add out Data to the Screen
        global count
        count = 0
        
        #for record in records:
        #    print(record)
        
        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10]), tags=('oddrow',))
        
            # Increment counter
            count += 1
        
        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()
        
    
    
    def search_records():
        
        lookup_record = search_entry.get()
        #print(lookup_record)
        
        # Close the search Box
        search.destroy()
        
        for record in my_tree.get_children():
            my_tree.delete(record)
           
        # Create a Database
        conn = sqlite3.connect('water_market_quezon.db')

        # Create a Cursor
        c = conn.cursor()
        
        c.execute("SELECT rowid, * FROM customers WHERE name like ?", (lookup_record,))
        records = c.fetchall()
        
        # Add out Data to the Screen
        global count
        count = 0
        
        #for record in records:
        #    print(record)
        
        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10]), tags=('oddrow',))
        
            # Increment counter
            count += 1
        
        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()
        
        
    
    
    def lookup_records():
        
        global search_entry, search
        search = Toplevel(root2)
        search.title("Look for Records")
        search.geometry("400x200") 
        search.config(bg="#45afb5")
        
        # Create Label Frame
        search_frame = LabelFrame(search, text="Name", bg="#45afb5")
        search_frame.pack(padx=10, pady=10)
        
        # Add Entry box
        search_entry = Entry(search_frame, font=("Calibri", 16))
        search_entry.pack(padx=20, pady=20)
        
        # Add Button
        search_button = Button(search, text="Search Records", font=("Arial Rounded MT Bold", 14), fg="black", bg="#ADDFDE", command=search_records)
        search_button.pack(padx=20, pady=20)
        
        
    
    
    # Add Menu
    my_menu = Menu(root2)
    root2.config(menu=my_menu)
    
    # Search Menu
    search_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Search", menu=search_menu)
    
    # Drop Down Menu
    search_menu.add_command(label="Search", command=lookup_records)
    search_menu.add_separator()
    search_menu.add_command(label="Reset", command=query_database)
    
    '''
    # Add Fake data
    data = [
        ["1", "Ej Erasga", "ejerasga12@gmail.com", "9654073894", "Bayog, Los Banos, Laguna",	"2", "3", "11",	"1", "6"],
        ["2", "Dahyun Kim", "kimdahyun@twice.com", "9143143143", "South Korea", "1",	"2", "3", "4", "5"],
        ["3", "Roronoa", "ejerasga12@gmail.com", "9654073894", "Bayog, Los Banos, Laguna",	"2", "3", "11",	"1", "6"],
        ["4", "Dahyun Kim", "kimdahyun@twice.com", "9143143143", "South Korea", "1",	"2", "3", "4", "5"],
        ["5", "Roronoa", "ejerasga12@gmail.com", "9654073894", "Bayog, Los Banos, Laguna",	"2", "3", "11",	"1", "6"],
        ["6", "Dahyun Kim", "kimdahyun@twice.com", "9143143143", "South Korea", "1",	"2", "3", "4", "5"],
        ["7", "Ej Erasga", "ejerasga12@gmail.com", "9654073894", "Bayog, Los Banos, Laguna",	"2", "3", "11",	"1", "6"],
        ["7", "Dahyun Kim", "kimdahyun@twice.com", "9143143143", "South Korea", "1",	"2", "3", "4", "5"],
        ["9", "Roronoa", "ejerasga12@gmail.com", "9654073894", "Bayog, Los Banos, Laguna",	"2", "3", "11",	"1", "6"],
        ["10", "Dahyun Kim", "kimdahyun@twice.com", "9143143143", "South Korea", "1",	"2", "3", "4", "5"],
        ["11", "Ej Erasga", "ejerasga12@gmail.com", "9654073894", "Bayog, Los Banos, Laguna",	"2", "3", "11",	"1", "6"],
        ["12", "Dahyun Kim", "kimdahyun@twice.com", "9143143143", "South Korea", "1",	"2", "3", "4", "5"],
        ["13", "Roronoa", "ejerasga12@gmail.com", "9654073894", "Bayog, Los Banos, Laguna",	"2", "3", "11",	"1", "6"],
        ["14", "Dahyun Kim", "kimdahyun@twice.com", "9143143143", "South Korea", "1",	"2", "3", "4", "5"],
        ["15", "Ej Erasga", "ejerasga12@gmail.com", "9654073894", "Bayog, Los Banos, Laguna",	"2", "3", "11",	"1", "6"],
        ["16", "Dahyun Kim", "kimdahyun@twice.com", "9143143143", "South Korea", "1",	"2", "3", "4", "5"],
        ["17", "Ej Erasga", "ejerasga12@gmail.com", "9654073894", "Bayog, Los Banos, Laguna",	"2", "3", "11",	"1", "6"],
        ["18", "Dahyun Kim", "kimdahyun@twice.com", "9143143143", "South Korea", "1",	"2", "3", "4", "5"],
        ["19", "Ej Erasga", "ejerasga12@gmail.com", "9654073894", "Bayog, Los Banos, Laguna",	"2", "3", "11",	"1", "6"],
        ["20", "Dahyun Kim", "kimdahyun@twice.com", "9143143143", "South Korea", "1",	"2", "3", "4", "5"]
    ]
    '''
    
    # Database
    # Create a Database
    conn = sqlite3.connect('water_market_quezon.db')

    # Create a Cursor
    c = conn.cursor()
    
    # Create Table
    c.execute("""CREATE TABLE if not exists customers (
            id integer,
            name text,
            email text,
            contact text,
            address text,
            menu1 integer,
            menu2 integer,
            menu3 integer,
            menu4 integer,
            menu5 integer)
            """)
    
    
    '''
    # Add Dummy Data to Table
    for record in data:
        c.execute("INSERT INTO customers VALUES (:id, :name, :email, :contact, :address, :menu1, :menu2, :menu3, :menu4, :menu5)", 
                  {
                      'id': record[0],
                      'name': record[1],
                      'email': record[2],
                      'contact': record[3],
                      'address': record[4],
                      'menu1': record[5],
                      'menu2': record[6],
                      'menu3': record[7],
                      'menu4': record[8],
                      'menu5': record[9]
                  }
                  )
    '''
    
    # Commit Changes
    conn.commit()

    # Close Connection
    conn.close()
    
    
    
        
    
    '''
    # Add dummy data to table
    for record in data:
        c.execute("INSERT INTO addresses VALUES (:name, :email, :contact, :address, :menu1, :menu2, :menu3, :menu4, :menu5)", 
                  {
                      'name': record[0],
                      'email': record[1],
                      'contact': record[2],
                      'address': record[3],
                      'menu1': record[4],
                      'menu2': record[5],
                      'menu3': record[6],
                      'menu4': record[7],
                      'menu5': record[8]
                  }
                  )
                  
                  
    ''''''
    
    def query_database():
        
        # Create a Database
        conn = sqlite3.connect('water_market.db')

        # Create a Cursor
        c = conn.cursor()
        
        c.execute("SELECT rowid, * FROM addresses")
        records = c.fetchall()
        
        # Add out Data to the Screen
        global count
        count = 0
        
        for record in records:
            print(record)
        
        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text="", values=(record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text="", values=(record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=('oddrow',))
        
            # Increment counter
            count += 1
        
        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()
    '''
    
    # Add some Style
    style = ttk.Style()
    style.theme_use('default')
    
    # Configure the Treeview Colors
    style.configure("Treeview",
                    background="#333333",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#333333")
    
    
    style.map('Treeview',
              background=[('selected', "#7a7777")])
    
    # Create a Treeview Frame
    tree_frame = Frame(root2)
    tree_frame.pack(pady=20)
    
    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    
    # Create Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()
    
    # Configure the Scrollbar
    tree_scroll.config(command=my_tree.yview)
    
    # Define Columns
    my_tree['columns'] = ("ID", "Name", "Email", "Contact", "Address", "Container", "Faucet", "Gallon", "Mineral", "Alkaline")
    
    # Format our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID", anchor=CENTER, width=100)
    my_tree.column("Name", anchor=W, width=140)
    my_tree.column("Email", anchor=W, width=150)
    my_tree.column("Contact", anchor=W, width=140)
    my_tree.column("Address", anchor=W, width=180)
    my_tree.column("Container", anchor=CENTER, width=100)
    my_tree.column("Faucet", anchor=CENTER, width=100)
    my_tree.column("Gallon", anchor=CENTER, width=100)
    my_tree.column("Mineral", anchor=CENTER, width=100)
    my_tree.column("Alkaline", anchor=CENTER, width=100)
    
    
    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ID", text="ID", anchor=CENTER)
    my_tree.heading("Name", text="Name", anchor=W)
    my_tree.heading("Email", text="Email", anchor=W)
    my_tree.heading("Contact", text="Contact", anchor=W)
    my_tree.heading("Address", text="Address", anchor=W)
    my_tree.heading("Container", text="Container", anchor=CENTER)
    my_tree.heading("Faucet", text="Faucet", anchor=CENTER)
    my_tree.heading("Gallon", text="Gallon", anchor=CENTER)
    my_tree.heading("Mineral", text="Mineral", anchor=CENTER)
    my_tree.heading("Alkaline", text="Alkaline", anchor=CENTER)
    
     
    

    
    # Create Striped Row
    my_tree.tag_configure('oddrow', background="#c9e4ca") 
    my_tree.tag_configure('evenrow', background="#87BBA2") 
    
    
    
    # Add Record Entry Boxes
    data_frame = LabelFrame(root2, text="Record", bg="#1F375D", fg="white")
    data_frame.pack(fill="x", expand="yes", padx=20)
    
    name_label = Label(data_frame, text="Name", font=("Arial Rounded MT Bold", 12), bg="#1F375D", fg="white")
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry = Entry(data_frame, font=("Arial Rounded MT", 12), width=15, bg="#ADDFDE")
    name_entry.grid(row=0, column=1, padx=10, pady=10)
    
    email_label = Label(data_frame, text="Email", font=("Arial Rounded MT Bold", 12), bg="#1F375D", fg="white")
    email_label.grid(row=0, column=2, padx=10, pady=10)
    email_entry = Entry(data_frame, font=("Arial Rounded MT", 12), width=15, bg="#ADDFDE")
    email_entry.grid(row=0, column=3, padx=10, pady=10)
    
    contact_label = Label(data_frame, text="Contact", font=("Arial Rounded MT Bold", 12), bg="#1F375D", fg="white")
    contact_label.grid(row=0, column=4, padx=10, pady=10)
    contact_entry = Entry(data_frame, font=("Arial Rounded MT", 12), width=15, bg="#ADDFDE")
    contact_entry.grid(row=0, column=5, padx=10, pady=10)
    
    address_label = Label(data_frame, text="Address", font=("Arial Rounded MT Bold", 12), bg="#1F375D", fg="white")
    address_label.grid(row=0, column=6, padx=10, pady=10)
    address_entry = Entry(data_frame, font=("Arial Rounded MT", 12), width=15, bg="#ADDFDE")
    address_entry.grid(row=0, column=7, padx=10, pady=10)
    
    id_label = Label(data_frame, text="ID", font=("Arial Rounded MT Bold", 12), bg="#1F375D", fg="white")
    id_label.grid(row=0, column=8, padx=10, pady=10)
    id_entry = Entry(data_frame, font=("Arial Rounded MT", 12), width=15, bg="#ADDFDE")
    id_entry.grid(row=0, column=9, padx=10, pady=10)
    
    menu1_label = Label(data_frame, text="Container", font=("Arial Rounded MT Bold", 12), bg="#1F375D", fg="white")
    menu1_label.grid(row=1, column=0, padx=10, pady=10)
    menu1_entry = Entry(data_frame, font=("Arial Rounded MT", 12), width=15, bg="#ADDFDE")
    menu1_entry.grid(row=1, column=1, padx=10, pady=10)
    
    menu2_label = Label(data_frame, text="Faucet", font=("Arial Rounded MT Bold", 12), bg="#1F375D", fg="white")
    menu2_label.grid(row=1, column=2, padx=10, pady=10)
    menu2_entry = Entry(data_frame, font=("Arial Rounded MT", 12), width=15, bg="#ADDFDE")
    menu2_entry.grid(row=1, column=3, padx=10, pady=10)
    
    menu3_label = Label(data_frame, text="Gallon", font=("Arial Rounded MT Bold", 12), bg="#1F375D", fg="white")
    menu3_label.grid(row=1, column=4, padx=10, pady=10)
    menu3_entry = Entry(data_frame, font=("Arial Rounded MT", 12), width=15, bg="#ADDFDE")
    menu3_entry.grid(row=1, column=5, padx=10, pady=10)
    
    menu4_label = Label(data_frame, text="Mineral", font=("Arial Rounded MT Bold", 12), bg="#1F375D", fg="white")
    menu4_label.grid(row=1, column=6, padx=10, pady=10)
    menu4_entry = Entry(data_frame, font=("Arial Rounded MT", 12), width=15, bg="#ADDFDE")
    menu4_entry.grid(row=1, column=7, padx=10, pady=10)
    
    menu5_label = Label(data_frame, text="Alkaline", font=("Arial Rounded MT Bold", 12), bg="#1F375D", fg="white")
    menu5_label.grid(row=1, column=8, padx=10, pady=10)
    menu5_entry = Entry(data_frame, font=("Arial Rounded MT", 12), width=15, bg="#ADDFDE")
    menu5_entry.grid(row=1, column=9, padx=10, pady=10)
    
    
    # Remove One
    def removed_one():
        x = my_tree.selection()[0]
        my_tree.delete(x)
        
        
        # Create a Database
        conn = sqlite3.connect('water_market_quezon.db')

        # Create a Cursor
        c = conn.cursor()
        
        
        # Delete from Database
        c.execute("DELETE from customers WHERE oid=" + id_entry.get())
        
        
        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()
        
        # Add Message Box
        #messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")
        
     
    
        
        
        
    
    
    # Clear Entry Boxes
    def clear_entries():
        
        # Clear Entry Boxes
        id_entry.delete(0, END)
        name_entry.delete(0, END)
        email_entry.delete(0, END)
        contact_entry.delete(0, END)
        address_entry.delete(0, END)
        menu1_entry.delete(0, END)
        menu2_entry.delete(0, END)
        menu3_entry.delete(0, END)
        menu4_entry.delete(0, END)
        menu5_entry.delete(0, END)
    
    
    # Select Record
    def select_record(e):
        
        # Clear Entry Boxes
        id_entry.delete(0, END)
        name_entry.delete(0, END)
        email_entry.delete(0, END)
        contact_entry.delete(0, END)
        address_entry.delete(0, END)
        menu1_entry.delete(0, END)
        menu2_entry.delete(0, END)
        menu3_entry.delete(0, END)
        menu4_entry.delete(0, END)
        menu5_entry.delete(0, END)
    
        # Grab Record Number
        selected = my_tree.focus()
        
        # Grab Record Values
        values = my_tree.item(selected, 'values')
        
        # Output to Entry Boxes
        id_entry.insert(0, values[0])
        name_entry.insert(0, values[1])
        email_entry.insert(0, values[2])
        contact_entry.insert(0, values[3])
        address_entry.insert(0, values[4])
        menu1_entry.insert(0, values[5])
        menu2_entry.insert(0, values[6])
        menu3_entry.insert(0, values[7])
        menu4_entry.insert(0, values[8])
        menu5_entry.insert(0, values[9])
    
    
    ##########################################################################################
    # EXport to CSV
    
    def export_data():
        # prompt user for filename and location to save the CSV file
        file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        
        # Open a connection to the database
        conn = sqlite3.connect('water_market_quezon.db')
        
        # Create a cursor object
        cursor = conn.cursor()

        # execute SELECT query to get all data in inventory table
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()

        # write data to CSV file
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # write header row
            writer.writerow(['ID','Name', 'Email', 'Contact', 'Adress', 'Conrainer', 'Faucet',  'Gallon', 'Mineral', 'Alkaline'])
            # write data rows
            for row in rows:
                writer.writerow(row)

        print(f"Data exported to {file_path}")
        
        # Close the connection
        conn.close()
        
    
    
##########################################################################################
    
    
    
    
    
    # Update Record
    def update_record():
        
        # Grab the Record Number
        selected = my_tree.focus()
        
        # Update Record
        my_tree.item(selected, text="", values=(id_entry.get(), name_entry.get(), email_entry.get(), contact_entry.get(),address_entry.get(), menu1_entry.get(), menu2_entry.get(), menu3_entry.get(), menu4_entry.get(), menu5_entry.get(),))
    
        
        # Create a Database
        conn = sqlite3.connect('water_market_quezon.db')

        # Create a Cursor
        c = conn.cursor()
        
        c.execute("""UPDATE customers SET
                  
                  name = :name,
                  email = :email,
                  contact = :contact,
                  address = :address,
                  menu1 = :menu1,
                  menu2 = :menu2,
                  menu3 = :menu3,
                  menu4 = :menu4,
                  menu5 = :menu5
                  
                  WHERE oid = :oid""",
                  {
                      'name': name_entry.get(),
                      'email': email_entry.get(),
                      'contact': contact_entry.get(),
                      'address': address_entry.get(),
                      'menu1': menu1_entry.get(),
                      'menu2': menu2_entry.get(),
                      'menu3': menu3_entry.get(),
                      'menu4': menu4_entry.get(),
                      'menu5': menu5_entry.get(),
                      'oid': id_entry.get(),
                  })
        
        
        
        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()
        
        # Add Message Box
        #messagebox.showinfo("Updated!", "Your Record Has Been Updated!")
        
        
        # Clear Entry Boxes
        id_entry.delete(0, END)
        name_entry.delete(0, END)
        email_entry.delete(0, END)
        contact_entry.delete(0, END)
        address_entry.delete(0, END)
        menu1_entry.delete(0, END)
        menu2_entry.delete(0, END)
        menu3_entry.delete(0, END)
        menu4_entry.delete(0, END)
        menu5_entry.delete(0, END)
    
    '''
        # Update the Database
        
        # Create a Database
        conn = sqlite3.connect('water_market.db')

        # Create a Cursor
        c = conn.cursor()
        
        c.execute("""UPDATE addresses SET
                  
                  name = :name,
                  email = :email,
                  contact = :contact,
                  address = :address,
                  menu1 = :menu1,
                  menu2 = :menu2,
                  menu3 = :menu3,
                  menu4 = :menu4,
                  menu5 = :menu5
                  
                  WHERE oid = :oid""",
                  {
                      'name': name_entry.get(),
                      'email': email_entry.get(),
                      'contact': contact_entry.get(),
                      'address': address_entry.get(),
                      'menu1': menu1_entry.get(),
                      'menu2': menu2_entry.get(),
                      'menu3': menu3_entry.get(),
                      'menu4': menu4_entry.get(),
                      'menu5': menu5_entry.get(),
                  }
                  
                  )
        
        
        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()
        
        
        
        
        
    '''
    # Add Buttons
    button_frame = LabelFrame(root2, text="Commands", bg="#1F375D", fg="white")
    button_frame.pack(fill="x", expand="yes", padx=20)
    
    update_button = Button(button_frame, text="Update Record", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command=update_record)
    update_button.grid(row=0, column=0, padx=10, pady=10)
    
    delete_button = Button(button_frame, text="Delete Record", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command=removed_one)
    delete_button.grid(row=0, column=1, padx=10, pady=10)
    
    clear_button = Button(button_frame, text="Clear Record", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command=clear_entries)
    clear_button.grid(row=0, column=2, padx=10, pady=10)
    
    #email_button = Button(button_frame, text="Send Email", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command=send_email)
    #email_button.grid(row=0, column=3, padx=10, pady=10)
    
    add_button = Button(button_frame, text="Go to Add", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command=close)
    add_button.grid(row=0, column=3, padx=10, pady=10)
    
    invento = Button(button_frame, text="Inventory", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command=close1)
    invento.grid(row=0, column=4, padx=10, pady=10)
    
    export_button = Button(button_frame, text="Export Data", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command=export_data)
    export_button.grid(row=0, column=5, padx=10, pady=10)
    
    e_button = Button(button_frame, text="Send Email", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command = email_sender_window)
    e_button.grid(row=0, column=6, padx=10, pady=10)
    
    
    

    
    

    
    # Bind the Treeview
    my_tree.bind("<ButtonRelease-1>", select_record)
    
    # Run to pull data from database on start 
    query_database()
    
    '''
    # Entries Frame
    entries_frame2 = Frame(root2, bg="#333333")
    entries_frame2.pack(side=TOP, fill=X)
    title = Label(entries_frame2, text="Update Customer Info", font=("Arial", 22, "bold"),fg='#5885ed', bg="#333333")
    title.grid(row=0, columnspan=6, padx=400, pady=20, sticky="w")
    '''

######################################################################################################################################
######################################################################################################################################    

# Menu | Add | Update
def dashboard(username, password):

    
    if len(username) == 0:
        messagebox.showerror(title="Error", message="Enter Username.")

    elif len(password) == 0:
        messagebox.showerror(title="Error", message="Enter Password.")

    elif username == 'wtrmrktSAQ@gmail.com' and password == 'satisfied_customers':
        if password == 'admin':
            login.destroy()
            
            add_and_update = Tk()
            add_and_update.title("Water Market Management System")
            add_and_update.geometry('1000x700')
            #add_and_update.configure(bg='#1F375D') # Window main Background
            #add_and_update.state("zoomed")
            
            def closee():
                add_and_update.destroy()
                add_frame()
                
            def closeee():
                add_and_update.destroy()
                update_frame()
            
           
            
            
            
            
                
            bg = PhotoImage(file="images\dashboard.png")

            my_label= Label(add_and_update, image=bg)
            my_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            
            add = Button(text="Add Details", font=("Arial Rounded MT Bold", 18), fg="black", bg="#ADDFDE", width=8, command=closee, bd=2, relief="solid")
            add.place(relx=0.3, rely=0.7, width=150, anchor=NW)


            update = Button(text="Update Details", font=("Arial Rounded MT Bold", 18), fg="black", bg="#ADDFDE", width=8, command=closeee, bd=2, relief="solid")
            update.place(relx=0.6, rely=0.7, width=180, anchor=NW)

            
            date = dt.datetime.now()
            # Create Label to display the Date
            label = Label(add_and_update, text=f"{date:%A, %B %d, %Y, %H:%M}", font="Calibri, 14", bg="#e9ebef")
            label.place(relx=0.70, rely=0.17, anchor=NW)
            
            add_and_update.mainloop()

           
                
            


            #btn_add = Button(add_and_update, text = "Add Details", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command = closee)
            #btn_add.place(relx=0.3, rely=0.5, anchor=CENTER)

            #btn_update = Button(add_and_update, text = "Update Details", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command = closeee)
            #btn_update.place(relx=0.6, rely=0.5, anchor=CENTER)
            
            #btn_email = Button(add_and_update, text = "Send Email", font=("Arial Rounded MT Bold", 16), fg="black", bg="#ADDFDE", command = send_email)
            #btn_email.place(relx=0.6, rely=0.5, anchor=CENTER)
            
            
            
            
        else:
            messagebox.showerror(title="Error", message="Inavlid, Please try Again")
    else:
        messagebox.showerror(title="Error", message="Inavlid, Please try Again")
        

        
login.mainloop()