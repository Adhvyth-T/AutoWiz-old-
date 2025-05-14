import tkinter as tk
from tkinter import messagebox
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FormFillerApp:
  
    def __init__(self, root):
        self.root = root
        self.root.title("Form Filler App")

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.additional_info = {}  # Additional information stored as key-value pairs

        # Load saved user details
        self.load_details()

        # Create UI elements
        self.create_main_window()


    def load_details(self):
        try:
            with open("user_details.json", "r") as file:
                data = json.load(file)
                self.name_var.set(data.get("name", ""))
                self.email_var.set(data.get("email", ""))
                self.additional_info = data.get("additional_info", {})
        except FileNotFoundError:
            pass

    def create_main_window(self):
        # Create main window for user details and form filling
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(self.root, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(self.root, textvariable=self.email_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Save Details", command=self.save_details).grid(row=2, column=0, columnspan=2, pady=10)

        # Additional information section
        tk.Label(self.root, text="Additional Information:").grid(row=3, column=0, columnspan=2, pady=5)

        # Entry for key and value
        tk.Label(self.root, text="Key:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.key_entry = tk.Entry(self.root)
        self.key_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Value:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.value_entry = tk.Entry(self.root)
        self.value_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Add Info", command=self.add_info).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Delete Info", command=self.delete_info).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="View Info", command=self.view_info).grid(row=8, column=0, columnspan=2, pady=10)

        tk.Button(self.root, text="Fill Form", command=self.fill_form).grid(row=12, column=0, columnspan=2, pady=10)

    def save_details(self):
        # Save details to JSON file
        data = {
            "name": self.name_var.get(),
            "email": self.email_var.get(),
            "additional_info": self.additional_info
        }
        with open("user_details.json", "w") as file:
            json.dump(data, file)
        messagebox.showinfo("Saved", "Details saved successfully!")

    def add_info(self):
        # Add additional information using key-value pairs
        key = self.key_entry.get()
        value = self.value_entry.get()
        if key and value:
            self.additional_info[key] = value
            messagebox.showinfo("Added", "Information added successfully!")
        else:
            messagebox.showwarning("Invalid", "Key and value cannot be empty!")

    def delete_info(self):
        # Delete additional information using key
        key = self.key_entry.get()
        if key in self.additional_info:
            del self.additional_info[key]
            self.save_details()  
            messagebox.showinfo("Deleted", f"Information with key '{key}' deleted successfully!")
        else:
            messagebox.showwarning("Not Found", f"Information with key '{key}' not found!")

    def view_info(self):
        # View all additional information
        info_window = tk.Toplevel(self.root)
        info_window.title("User Details")

        info_text = tk.Text(info_window)
        info_text.pack()

        info_text.insert(tk.END, "User Details:\n")
        info_text.insert(tk.END, f"Name: {self.name_var.get()}\n")
        info_text.insert(tk.END, f"Email: {self.email_var.get()}\n")
        info_text.insert(tk.END, "Additional Information:\n")
        for key, value in self.additional_info.items():
            info_text.insert(tk.END, f"{key}: {value}\n")

        info_text.config(state=tk.DISABLED)

    def fill_form(self):
        # Use Selenium to fetch the current URL
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Add experimental option for remote debugging
        driver = webdriver.Chrome(options=options)

        # Get the current URL from the active tab
        current_url = driver.current_url

        # Detect form type and fill accordingly
        if current_url :
            self.fill_all_form(driver)
        else:
            messagebox.showwarning("Empty URL", "The current URL is empty. Please navigate to a valid form page.")

    def fill_all_form(self, driver):
        # Fill form fields based on their names
        name = self.name_var.get()
        email = self.email_var.get()

        wait = WebDriverWait(driver, 10)

        # Find the label element with the text "Name:"
        name_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[contains(text(), 'Name')]/..//input")))


        name_field.send_keys(name)

        # Find and fill the "Email" input field
        email_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[contains(text(), 'Email')]/..//input")))
        email_field.send_keys(email)

      # Fill additional information fields based on key-value pairs
        if 'Phone' in self.additional_info:
            phone_value = self.additional_info['Phone']
            phone_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[contains(text(), 'Phone')]/..//input")))
            phone_field.send_keys(str(phone_value))  # Convert to string if necessary

        # Fill confirm password field with the same value as password if 'Password' key exists
        if 'Password' in self.additional_info:
            password_value = self.additional_info['Password']
            password_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[contains(text(), 'Password')]/..//input")))
            confirm_password_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[contains(text(), 'Confirm Password')]/..//input")))
            password_field.send_keys(str(password_value)) 
            confirm_password_field.send_keys(str(password_value)) 

        for key, value in self.additional_info.items():
            try:
                if key not in ['Phone', 'Password']:
                    field = wait.until(EC.visibility_of_element_located((By.XPATH, f"//label[contains(text(), '{key}')]/following-sibling::input")))
                    field.send_keys(value)
            except Exception as e:
                print(f"Error filling field '{key}': {str(e)}")

        messagebox.showinfo("Filled Form", "Form filled successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FormFillerApp(root)
    root.mainloop()