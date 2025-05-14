import tkinter as tk
from tkinter import filedialog, messagebox
from fpdf import FPDF
from docx import Document
from PyPDF2 import PdfReader, PdfWriter
from pdf2docx import Converter
import os
from comtypes import client

# Function to convert text to PDF
def text_to_pdf(text_content, output_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text_content, 0, 'L')
    pdf.output(output_file)

# Function to convert PDF to Word
def pdf_to_word(input_pdf, output_docx):
    try:
        # Initialize comtypes client
        word = client.CreateObject("Word.Application")
        word.Visible = False

        # Convert PDF to temporary Word document
        temp_word_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'temp.docx')
        cv = Converter(input_pdf)
        cv.convert(temp_word_path)
        cv.close()

        # Open temporary Word document and save as final output
        doc = word.Documents.Open(temp_word_path)
        doc.SaveAs(output_docx, FileFormat=16)  # FileFormat=16 for .docx format
        doc.Close()

        # Quit Word application
        word.Quit()
    except Exception as e:
        messagebox.showerror("Conversion Error", f"Error occurred during PDF to Word conversion: {e}")

# Function to convert Word to PDF using comtypes
def word_to_pdf(input_docx, output_pdf):
    try:
        # Create a Word application object
        word = client.CreateObject("Word.Application")
        word.Visible = False  # Hide the Word application window

        # Open the input Word document
        doc = word.Documents.Open(os.path.abspath(input_docx))

        # Save the document as PDF
        doc.SaveAs(os.path.abspath(output_pdf), FileFormat=17)  # FileFormat=17 for PDF format

        # Close the document and Word application
        doc.Close()
        word.Quit()
    except Exception as e:
        messagebox.showerror("Conversion Error", f"Error occurred during Word to PDF conversion: {e}")

# Function to convert Python script to PDF
def py_to_pdf(input_py, output_pdf):
    with open(input_py, 'r', encoding='utf-8') as py_file:
        text_content = py_file.read()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=10)
    pdf.multi_cell(0, 10, text_content)
    pdf.output(output_pdf)

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        if file_path.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
                output_file = 'converted.pdf'
                text_to_pdf(text_content, output_file)
        elif file_path.lower().endswith('.pdf'):
            output_file = 'converted.docx'
            pdf_to_word(file_path, output_file)
        elif file_path.lower().endswith('.docx'):
            output_file = 'converted.pdf'
            word_to_pdf(file_path, output_file)
        elif file_path.lower().endswith('.py'):
            output_file = 'converted.pdf'
            py_to_pdf(file_path, output_file)
        else:
            messagebox.showwarning("Unsupported File", "Unsupported file format. Please select a text, PDF, Word, or Python script file.")


        try:
            if output_file.lower().endswith('.pdf'):
                save_file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            elif output_file.lower().endswith('.docx'):
                save_file_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word files", "*.docx")])

            if save_file_path:
                os.rename(output_file, save_file_path)
                messagebox.showinfo("Download Complete", f"Converted file downloaded at: {save_file_path}")
                root.destroy()
        except Exception as e:
            messagebox.showerror("Save Error", f"Error occurred during file save: {e}")
            
root = tk.Tk()
root.title("File Converter")

open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack()

root.mainloop()