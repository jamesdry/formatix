from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2docx import Converter
from docx2pdf import convert
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
import os

#configuration

window = Tk()
window.title("ConvertMe")
window.state('zoomed')
window.resizable(False, False)
window.configure(background='orange')

#functions feature

def openPDFtoDOCX():
    pdf_to_docx = Toplevel(window)
    pdf_to_docx.title("Convert PDF to DOCX")
    pdf_to_docx.geometry("450x300")
    pdf_to_docx.resizable(False, False)
    pdf_to_docx.configure(background='orange')

    pdf_to_docx.transient(window)
    pdf_to_docx.attributes('-topmost', True)

    open_pdf_to_docx.config(state="disabled")

    file_name_variable = tk.StringVar()
    file_path_variable = tk.StringVar()

    def select_pdf_file():
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")],
            title="Select a PDF File",
            parent=pdf_to_docx
        )
        if file_path:
            file_name = os.path.basename(file_path)
            file_name_variable.set(file_name)
            file_path_variable.set(file_path)

    def convert_pdf_to_docx():
        pdf_file_path = file_path_variable.get()
        if not pdf_file_path.endswith('.pdf'):
            messagebox.showerror("Error", "Please Select A Valid PDF File !")
            return

        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        output_filename = os.path.basename(pdf_file_path).replace(".pdf", ".docx")
        docx_file = os.path.join(downloads_folder, output_filename)

        try:
            convert = Converter(pdf_file_path)
            convert.convert(docx_file, start=0, end=None)
            convert.close()
            messagebox.showinfo("Success", f"PDF Successfully Converted to DOCX File !\nSaved As: {docx_file}")
        except Exception as error:
            messagebox.showerror("Error", f"Failed To Convert PDF To DOCX.\nError: {str(error)}")

    input_field = tk.Entry(pdf_to_docx, textvariable=file_name_variable, width=50)
    input_field.grid(row=0, column=0, padx=20, pady=20)
    input_field.config(state=tk.DISABLED)

    select_pdf_file_button = Button(pdf_to_docx, text="Select PDF File", command=select_pdf_file)
    select_pdf_file_button.grid(row=0, column=1, padx=0, pady=20)

    convert_to_docx_button = Button(pdf_to_docx, text="Convert To DOCX", command=convert_pdf_to_docx)
    convert_to_docx_button.grid(row=1, column=0, columnspan=2, pady=20)

    def on_window_close():
        open_pdf_to_docx.config(state="normal")
        pdf_to_docx.destroy()
    
    pdf_to_docx.protocol("WM_DELETE_WINDOW", on_window_close)

def openDOCXtoPDF():
    docx_to_pdf = Toplevel(window)
    docx_to_pdf.title("Convert DOCX to PDF")
    docx_to_pdf.geometry("450x300")
    docx_to_pdf.resizable(False, False)
    docx_to_pdf.configure(background='orange')

    docx_to_pdf.transient(window)
    docx_to_pdf.attributes("-topmost", True)

    open_docx_to_pdf.config(state="disabled")

    file_name_variable = tk.StringVar()
    file_path_variable = tk.StringVar()

    def select_docx_file():
        file_path = filedialog.askopenfilename(
            filetypes=[("DOCX Files", "*.docx")],
            title="Select a DOCX File",
            parent=docx_to_pdf
        )
        if file_path:
            file_name = os.path.basename(file_path)
            file_name_variable.set(file_name)
            file_path_variable.set(file_path)

    def convert_docx_to_pdf():
        docx_file_path = file_path_variable.get()
        if not docx_file_path.endswith('.docx'):
            messagebox.showerror("Error", "Please Select A Valid DOCX File !")
            return

        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        output_filename = os.path.basename(docx_file_path).replace(".docx", ".pdf")
        pdf_file = os.path.join(downloads_folder, output_filename)

        try:
            convert(docx_file_path, pdf_file)
            messagebox.showinfo("Success", f"DOCX Successfully Converted to PDF File !\nSaved As: {pdf_file}")
        except Exception as error:
            messagebox.showerror("Error", f"Failed To Convert DOCX To PDF.\nError: {str(error)}")

    input_field = tk.Entry(docx_to_pdf, textvariable=file_name_variable, width=50)
    input_field.grid(row=0, column=0, padx=20, pady=20)
    input_field.config(state=tk.DISABLED)

    select_docx_file_button = Button(docx_to_pdf, text="Select DOCX File", command=select_docx_file)
    select_docx_file_button.grid(row=0, column=1, padx=0, pady=20)

    convert_to_pdf_button = Button(docx_to_pdf, text="Convert To PDF", command=convert_docx_to_pdf)
    convert_to_pdf_button.grid(row=1, column=0, columnspan=2, pady=20)

    def on_window_close():
        open_docx_to_pdf.config(state="normal")
        docx_to_pdf.destroy()
    
    docx_to_pdf.protocol("WM_DELETE_WINDOW", on_window_close)

def openJPGtoPNG():
    jpg_to_png = Toplevel(window)
    jpg_to_png.title("Convert JPG to PNG")
    jpg_to_png.geometry("450x300")
    jpg_to_png.resizable(False, False)
    jpg_to_png.configure(background='orange')

    jpg_to_png.transient(window)
    jpg_to_png.attributes('-topmost', True)

    open_jpg_to_png.config(state="disabled")

    file_name_variable = tk.StringVar()
    file_path_variable = tk.StringVar()

    def select_jpg_file():
        file_path = filedialog.askopenfilename(
            filetypes=[("JPG Files", "*.jpg"), ("JPEG Files", "*.jpeg")],
            title="Select a JPG File",
            parent=jpg_to_png
        )
        if file_path:
            file_name = os.path.basename(file_path)
            file_name_variable.set(file_name)
            file_path_variable.set(file_path)

    def convert_jpg_to_png():
        jpg_file_path = file_path_variable.get()
        if not jpg_file_path.lower().endswith(('.jpg', '.jpeg')):
            messagebox.showerror("Error", "Please Select A Valid JPG File !")
            return
        
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        output_filename = os.path.basename(jpg_file_path).replace(".jpg", ".png").replace(".jpeg", ".png")
        png_file = os.path.join(downloads_folder, output_filename)

        try:
            image = Image.open(jpg_file_path)
            image.save(png_file, "PNG")
            messagebox.showinfo("Success", f"JPG Successfully Converted to PNG File !\nSaved As: {png_file}")
        except Exception as error:
            messagebox.showerror("Error", f"Failed To Convert JPG To PNG.\nError: {str(error)}")

    input_field = tk.Entry(jpg_to_png, textvariable=file_name_variable, width=50)
    input_field.grid(row=0, column=0, padx=20, pady=20)
    input_field.config(state=tk.DISABLED)

    select_jpg_file_button = Button(jpg_to_png, text="Select JPG File", command=select_jpg_file)
    select_jpg_file_button.grid(row=0, column=1, padx=0, pady=20)

    convert_to_png_button = Button(jpg_to_png, text="Convert To PNG", command=convert_jpg_to_png)
    convert_to_png_button.grid(row=1, column=0, columnspan=2, pady=20)

    def on_window_close():
        open_jpg_to_png.config(state="normal")
        jpg_to_png.destroy()

    jpg_to_png.protocol("WM_DELETE_WINDOW", on_window_close)

def openPNGtoJPG():
    png_to_jpg = Toplevel(window)
    png_to_jpg.title("Convert PNG to JPG")
    png_to_jpg.geometry("450x300")
    png_to_jpg.resizable(False, False)
    png_to_jpg.configure(background='orange')

    png_to_jpg.transient(window)
    png_to_jpg.attributes('-topmost', True)

    open_png_to_jpg.config(state="disabled")

    file_name_variable = tk.StringVar()
    file_path_variable = tk.StringVar()

    def select_png_file():
        file_path = filedialog.askopenfilename(
            filetypes=[("PNG Files", "*.png")],
            title="Select a PNG File",
            parent=png_to_jpg
        )
        if file_path:
            file_name = os.path.basename(file_path)
            file_name_variable.set(file_name)
            file_path_variable.set(file_path)

    def convert_png_to_jpg():
        png_file_path = file_path_variable.get()
        if not png_file_path.lower().endswith('.png'):
            messagebox.showerror("Error", "Please Select A Valid PNG File!")
            return
        
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        output_filename = os.path.basename(png_file_path).replace(".png", ".jpg")
        jpg_file = os.path.join(downloads_folder, output_filename)
        
        try:
            image = Image.open(png_file_path)
            rgb_image = image.convert("RGB")
            rgb_image.save(jpg_file, "JPEG")
            messagebox.showinfo("Success", f"PNG Successfully Converted to JPG File!\nSaved As: {jpg_file}")
        except Exception as error:
            messagebox.showerror("Error", f"Failed To Convert PNG To JPG.\nError: {str(error)}")

    input_field = tk.Entry(png_to_jpg, textvariable=file_name_variable, width=50)
    input_field.grid(row=0, column=0, padx=20, pady=20)
    input_field.config(state=tk.DISABLED)

    select_png_file_button = Button(png_to_jpg, text="Select PNG File", command=select_png_file)
    select_png_file_button.grid(row=0, column=1, padx=0, pady=20)

    convert_to_jpg_button = Button(png_to_jpg, text="Convert To JPG", command=convert_png_to_jpg)
    convert_to_jpg_button.grid(row=1, column=0, columnspan=2, pady=20)

    def on_window_close():
        open_png_to_jpg.config(state="normal")
        png_to_jpg.destroy()

    png_to_jpg.protocol("WM_DELETE_WINDOW", on_window_close)

def openWEBPtoPNG():
    webp_to_png = Toplevel(window)
    webp_to_png.title("Convert WEBP to PNG")
    webp_to_png.geometry("450x300")
    webp_to_png.resizable(False, False)
    webp_to_png.configure(background='orange')

    webp_to_png.transient(window)
    webp_to_png.attributes('-topmost', True)

    open_webp_to_png.config(state="disabled")

    file_name_variable = tk.StringVar()
    file_path_variable = tk.StringVar()

    def select_webp_file():
        file_path = filedialog.askopenfilename(
            filetypes=[("WEBP Files", "*.webp")],
            title="Select a WEBP File",
            parent=webp_to_png
        )
        if file_path:
            file_name = os.path.basename(file_path)
            file_name_variable.set(file_name)
            file_path_variable.set(file_path)

    def convert_webp_to_png():
        webp_file_path = file_path_variable.get()
        if not webp_file_path.lower().endswith('.webp'):
            messagebox.showerror("Error", "Please Select A Valid WEBP File!")
            return

        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads" )
        output_filename = os.path.basename(webp_file_path).replace(".webp", ".png")
        png_file = os.path.join(downloads_folder, output_filename)

        try:
            image = Image.open(webp_file_path)
            image.save(png_file, "PNG")
            messagebox.showinfo("Success", f"WEBP Successfully Converted to PNG File!\nSaved As: {png_file}")
        except Exception as error:
            messagebox.showerror("Error", f"Failed To Convert WEBP To PNG.\nError: {str(error)}")

    input_field = tk.Entry(webp_to_png, textvariable=file_name_variable, width=50)
    input_field.grid(row=0, column=0, padx=20, pady=20)
    input_field.config(state=tk.DISABLED)

    select_webp_file_button = Button(webp_to_png, text="Select WEBP File", command=select_webp_file)
    select_webp_file_button.grid(row=0, column=1, padx=0, pady=20)

    convert_to_png_button = Button(webp_to_png, text="Convert To PNG", command=convert_webp_to_png)
    convert_to_png_button.grid(row=1, column=0, columnspan=2, pady=20)

    def on_window_close():
        open_webp_to_png.config(state="normal")
        webp_to_png.destroy()

    webp_to_png.protocol("WM_DELETE_WINDOW", on_window_close)


def openPNGtoWEBP():
    png_to_webp = Toplevel(window)
    png_to_webp.title("Convert PNG to WEBP")
    png_to_webp.geometry("450x300")
    png_to_webp.resizable(False, False)
    png_to_webp.configure(background='orange')

    png_to_webp.transient(window)
    png_to_webp.attributes('-topmost', True)

    open_png_to_webp.config(state="disabled")

    file_name_variable = tk.StringVar()
    file_path_variable = tk.StringVar()

    def select_png_file():
        file_path = filedialog.askopenfilename(
            filetypes=[("PNG Files", "*.png")],
            title="Select a PNG File",
            parent=png_to_webp
        )
        if file_path:
            file_name = os.path.basename(file_path)
            file_name_variable.set(file_name)
            file_path_variable.set(file_path)

    def convert_png_to_webp():
        png_file_path = file_path_variable.get()
        if not png_file_path.lower().endswith('.png'):
            messagebox.showerror("Error", "Please Select A Valid PNG File!")
            return
        
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        output_filename = os.path.basename(png_file_path).replace(".png", ".webp")
        webp_file = os.path.join(downloads_folder, output_filename)

        try:
            image = Image.open(png_file_path)
            image.save(webp_file, "WEBP")
            messagebox.showinfo("Success", f"PNG Successfully Converted to WEBP File!\nSaved As: {webp_file}")
        except Exception as error:
            messagebox.showerror("Error", f"Failed To Convert PNG To WEBP.\nError: {str(error)}")

    input_field = tk.Entry(png_to_webp, textvariable=file_name_variable, width=50)
    input_field.grid(row=0, column=0, padx=20, pady=20)
    input_field.config(state=tk.DISABLED)

    select_png_file_button = Button(png_to_webp, text="Select PNG File", command=select_png_file)
    select_png_file_button.grid(row=0, column=1, padx=0, pady=20)

    convert_to_webp_button = Button(png_to_webp, text="Convert To WEBP", command=convert_png_to_webp)
    convert_to_webp_button.grid(row=1, column=0, columnspan=2, pady=20)

    def on_window_close():
        open_png_to_webp.config(state="normal")
        png_to_webp.destroy()

    png_to_webp.protocol("WM_DELETE_WINDOW", on_window_close)


def mergePDF():
    merge_pdf_window = Toplevel(window)
    merge_pdf_window.title("Merge PDF")
    merge_pdf_window.geometry("500x400")
    merge_pdf_window.resizable(False, False)
    merge_pdf_window.configure(background='orange')

    merge_pdf_window.transient(window)
    merge_pdf_window.attributes('-topmost', True)

    merge_pdf.config(state='disabled')

    pdf_files = []

    frame = Frame(merge_pdf_window)
    frame.pack(pady=10, fill=tk.BOTH, expand=True)

    listbox = Listbox(frame, width=60, height=10)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    def add_pdf():
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")], title="Select PDF File", parent=merge_pdf_window)
        if files:
            for file in files:
                if file not in pdf_files:
                    pdf_files.append(file)
                    listbox.insert(END, file)
    
    def remove_selected_pdf():
        selected_pdf = listbox.curselection()
        for index in reversed(selected_pdf):
            listbox.delete(index)
            del pdf_files[index]

    def merge_pdfs():
        if not pdf_files:
            messagebox.showwarning("No PDFs Selected", "please add at least one PDF to merge.")
            return

        if len(pdf_files) < 2:
            messagebox.showwarning("Not Enough PDFs", "Please add at least two PDFs to merge.")
            return
        
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], parent=merge_pdf_window)
        if not save_path:
            return
        
        try:
            merger = PdfMerger()
            for pdf in pdf_files:
                merger.append(pdf)
            merger.write(save_path)
            merger.close()
            messagebox.showinfo("Success", "PDFs merged successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"an error occured: {e}")

    add_pdf_button = Button(merge_pdf_window, text="Add PDF", command=add_pdf)
    add_pdf_button.pack(padx=0, pady=20)

    remove_pdf_button = Button(merge_pdf_window, text="Remove Selected PDF", command=remove_selected_pdf)
    remove_pdf_button.pack(padx=0, pady=20)

    merge_pdf_button = Button(merge_pdf_window, text="Merge PDFs", command=merge_pdfs)
    merge_pdf_button.pack(padx=0, pady=20)

    def on_window_close():
        merge_pdf.config(state='normal')
        merge_pdf_window.destroy()

    merge_pdf_window.protocol("WM_DELETE_WINDOW", on_window_close)


def splitPDF():
    split_pdf_window = Toplevel(window)
    split_pdf_window.title("Split PDF")
    split_pdf_window.geometry("500x400")
    split_pdf_window.resizable(False, False)
    split_pdf_window.configure(background='orange')

    split_pdf_window.transient(window)
    split_pdf_window.attributes("-topmost", True)

    split_pdf.config(state='disabled')

    pdf_files = []

    frame = Frame(split_pdf_window)
    frame.pack(pady=10, fill=tk.BOTH, expand=True)

    listbox = Listbox(frame, width=60, height=10)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    def add_pdf():
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")], title="Select PDF File", parent=split_pdf_window)
        if file and file not in pdf_files:
            pdf_files.append(file)
            listbox.insert(END, file)

    def remove_selected_pdf():
        selected_pdf = listbox.curselection()
        for index in reversed(selected_pdf):
            listbox.delete(index)
            del pdf_files[index]

    def split_pdfs():
        if not pdf_files:
            messagebox.showwarning("No PDFs Selected", "Please add a PDF file to split.")
            return

        if len(pdf_files) >= 2:
            messagebox.showwarning("Cannot Accept Two PDFs", "cannot accept two pdf to split, please provide only one pdf in the listbox !")
            return
        
        for file_path in pdf_files:
            
            try:
                pdf_reader = PdfReader(file_path)
                total_pages = len(pdf_reader.pages)

                output_folder = os.path.join(os.path.dirname(file_path), "Split PDFs")
                os.makedirs(output_folder, exist_ok=True)

                for page_num in range(total_pages):
                    pdf_writer = PdfWriter()
                    pdf_writer.add_page(pdf_reader.pages[page_num])

                    output_path = os.path.join(output_folder, f"{os.path.basename(file_path).replace('.pdf', '')}_page_{page_num + 1}.pdf")
                    with open(output_path, "wb") as output_pdf:
                        pdf_writer.write(output_pdf)

                messagebox.showinfo("Success", f"PDF split successfully!\nSaved in: {output_folder}")
            
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    add_pdf_button = Button(split_pdf_window, text="Add PDF", command=add_pdf)
    add_pdf_button.pack(padx=0, pady=20)

    remove_pdf_button = Button(split_pdf_window, text="Remove Selected PDF", command=remove_selected_pdf)
    remove_pdf_button.pack(padx=0, pady=20)

    split_pdf_button = Button(split_pdf_window, text="Split PDF", command=split_pdfs)
    split_pdf_button.pack(padx=0, pady=20)

    def on_window_close():
        split_pdf.config(state='normal')
        split_pdf_window.destroy()

    split_pdf_window.protocol("WM_DELETE_WINDOW", on_window_close)

# button to select feature

open_pdf_to_docx = Button(window, text="Convert PDF to DOCX", height=3, width=20, command=openPDFtoDOCX)
open_pdf_to_docx.grid(row=0, column=0, pady=10, padx=30)

open_docx_to_pdf = Button(window, text="Convert DOCX to PDF", height=3, width=20, command=openDOCXtoPDF)
open_docx_to_pdf.grid(row=0, column=1, pady=10, padx=30)

open_jpg_to_png = Button(window, text="Convert JPG to PNG", height=3, width=20, command=openJPGtoPNG)
open_jpg_to_png.grid(row=1, column=0, pady=20, padx=30)

open_png_to_jpg = Button(window, text="Convert PNG to JPG", height=3, width=20, command=openPNGtoJPG)
open_png_to_jpg.grid(row=1, column=1, pady=20, padx=30)

open_webp_to_png = Button(window, text="Convert WEBP to PNG", height=3, width=20, command=openWEBPtoPNG)
open_webp_to_png.grid(row=2, column=0, pady=20, padx=30)

open_png_to_webp = Button(window, text="Convert PNG to WEBP", height=3, width=20, command=openPNGtoWEBP)
open_png_to_webp.grid(row=2, column=1, pady=20, padx=30)

merge_pdf = Button(window, text="Merge PDF", height=3, width=20, command=mergePDF)
merge_pdf.grid(row=3, column=0, pady=20, padx=30)

split_pdf = Button(window, text="Split PDF", height=3, width=20, command=splitPDF)
split_pdf.grid(row=3, column=1, pady=20, padx=30)

window.mainloop()