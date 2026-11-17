import os
import tkinter as tk
from tkinter import filedialog, messagebox

import fitz
from PIL import Image
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from docx2pdf import convert
from pdf2docx import Converter


class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.feature_buttons = []
        self.buttons_by_name = {}
        self.setup_window()
        self.setup_search()
        self.setup_features()

    def setup_window(self):
        self.root.title("Formatix")
        self.root.state("zoomed")
        self.root.resizable(False, False)
        self.root.configure(background="orange")

    def setup_search(self):
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_features)

        search_frame = tk.Frame(self.root, background="orange")
        search_frame.grid(row=0, column=0, columnspan=2, pady=20, padx=30, sticky="ew")

        tk.Label(search_frame, text="Search Features:", background="orange").pack(
            side=tk.LEFT, padx=(0, 10)
        )

        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind("<Escape>", lambda event: self.search_var.set(""))

    def setup_features(self):
        features = [
            ("Convert PDF to DOCX", self.open_pdf_to_docx),
            ("Convert DOCX to PDF", self.open_docx_to_pdf),
            ("Convert PDF to JPG", self.open_pdf_to_jpg),
            ("Convert JPG to PNG", self.open_jpg_to_png),
            ("Convert PNG to JPG", self.open_png_to_jpg),
            ("Convert WEBP to PNG", self.open_webp_to_png),
            ("Convert PNG to WEBP", self.open_png_to_webp),
            ("Merge PDF", self.merge_pdf),
            ("Split PDF", self.split_pdf),
        ]

        columns = 2
        for index, (name, command) in enumerate(features):
            row = index // columns + 1
            column = index % columns
            button = tk.Button(
                self.root,
                text=name,
                height=3,
                width=20,
                command=command,
                cursor="hand2",
            )
            button.grid(row=row, column=column, pady=20, padx=30)
            self.feature_buttons.append((name, button))
            self.buttons_by_name[name] = button

    def filter_features(self, *_):
        query = self.search_var.get().strip().lower()
        for name, button in self.feature_buttons:
            if query in name.lower():
                button.grid()
            else:
                button.grid_remove()

    def create_feature_window(self, title, button_name, geometry="450x300"):
        button = self.buttons_by_name[button_name]
        button.config(state="disabled")

        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(geometry)
        window.resizable(False, False)
        window.configure(background="orange")
        window.transient(self.root)
        window.attributes("-topmost", True)

        return window, button

    def close_feature_window(self, window, button):
        button.config(state="normal")
        window.destroy()

    def get_downloads_folder(self):
        folder = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(folder, exist_ok=True)
        return folder

    def create_single_file_conversion_window(
        self, source_name, target_name, filetypes, valid_extensions, converter
    ):
        title = f"Convert {source_name} to {target_name}"
        window, button = self.create_feature_window(title, title)

        file_name_var = tk.StringVar()
        file_path_var = tk.StringVar()

        def select_file():
            file_path = filedialog.askopenfilename(
                filetypes=filetypes,
                title=f"Select a {source_name} File",
                parent=window,
            )
            if file_path:
                file_name_var.set(os.path.basename(file_path))
                file_path_var.set(file_path)

        def run_conversion():
            file_path = file_path_var.get()
            if not file_path.lower().endswith(valid_extensions):
                messagebox.showerror(
                    "Error", f"Please Select A Valid {source_name} File !"
                )
                return

            try:
                output_path = converter(file_path)
                messagebox.showinfo(
                    "Success",
                    f"{source_name} Successfully Converted to {target_name} File !\n"
                    f"Saved As: {output_path}",
                )
            except Exception as error:
                messagebox.showerror(
                    "Error",
                    f"Failed To Convert {source_name} To {target_name}.\n"
                    f"Error: {error}",
                )

        input_field = tk.Entry(
            window, textvariable=file_name_var, width=50, state=tk.DISABLED
        )
        input_field.grid(row=0, column=0, padx=20, pady=20)

        tk.Button(
            window,
            text=f"Select {source_name} File",
            command=select_file,
            cursor="hand2",
        ).grid(row=0, column=1, padx=0, pady=20)

        tk.Button(
            window,
            text=f"Convert To {target_name}",
            command=run_conversion,
            cursor="hand2",
        ).grid(row=1, column=0, columnspan=2, pady=20)

        window.protocol(
            "WM_DELETE_WINDOW", lambda: self.close_feature_window(window, button)
        )

    def open_pdf_to_docx(self):
        def converter(pdf_file_path):
            output_filename = os.path.basename(pdf_file_path).replace(".pdf", ".docx")
            docx_file = os.path.join(self.get_downloads_folder(), output_filename)
            conv = Converter(pdf_file_path)
            try:
                conv.convert(docx_file, start=0, end=None)
            finally:
                conv.close()
            return docx_file

        self.create_single_file_conversion_window(
            "PDF",
            "DOCX",
            [("PDF Files", "*.pdf")],
            (".pdf",),
            converter,
        )

    def open_docx_to_pdf(self):
        def converter(docx_file_path):
            output_filename = os.path.basename(docx_file_path).replace(".docx", ".pdf")
            pdf_file = os.path.join(self.get_downloads_folder(), output_filename)
            convert(docx_file_path, pdf_file)
            return pdf_file

        self.create_single_file_conversion_window(
            "DOCX",
            "PDF",
            [("DOCX Files", "*.docx")],
            (".docx",),
            converter,
        )

    def open_pdf_to_jpg(self):
        window, button = self.create_feature_window(
            "Convert PDF to JPG", "Convert PDF to JPG"
        )

        file_name_var = tk.StringVar()
        file_path_var = tk.StringVar()

        def select_pdf_file():
            file_path = filedialog.askopenfilename(
                filetypes=[("PDF Files", "*.pdf")],
                title="Select a PDF File",
                parent=window,
            )
            if file_path:
                file_name_var.set(os.path.basename(file_path))
                file_path_var.set(file_path)

        def convert_pdf_to_jpg():
            pdf_file_path = file_path_var.get()
            if not pdf_file_path.lower().endswith(".pdf"):
                messagebox.showerror("Error", "Please Select A Valid PDF File !")
                return

            base_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
            output_folder = os.path.join(
                self.get_downloads_folder(), f"{base_name}_jpg"
            )

            try:
                os.makedirs(output_folder, exist_ok=True)
                with fitz.open(pdf_file_path) as pdf_document:
                    total_pages = len(pdf_document)
                    for page_num in range(total_pages):
                        page = pdf_document.load_page(page_num)
                        pixmap = page.get_pixmap(dpi=200)
                        output_path = os.path.join(
                            output_folder, f"{base_name}_page_{page_num + 1}.jpg"
                        )
                        pixmap.save(output_path)
                messagebox.showinfo(
                    "Success",
                    f"PDF Successfully Converted to JPG !\n"
                    f"Saved in: {output_folder}",
                )
            except Exception as error:
                messagebox.showerror(
                    "Error", f"Failed To Convert PDF To JPG.\nError: {error}"
                )

        input_field = tk.Entry(
            window, textvariable=file_name_var, width=50, state=tk.DISABLED
        )
        input_field.grid(row=0, column=0, padx=20, pady=20)

        tk.Button(
            window, text="Select PDF File", command=select_pdf_file, cursor="hand2"
        ).grid(row=0, column=1, padx=0, pady=20)

        tk.Button(
            window, text="Convert To JPG", command=convert_pdf_to_jpg, cursor="hand2"
        ).grid(row=1, column=0, columnspan=2, pady=20)

        window.protocol(
            "WM_DELETE_WINDOW", lambda: self.close_feature_window(window, button)
        )

    def open_jpg_to_png(self):
        def converter(jpg_file_path):
            output_filename = (
                os.path.basename(jpg_file_path)
                .replace(".jpg", ".png")
                .replace(".jpeg", ".png")
            )
            png_file = os.path.join(self.get_downloads_folder(), output_filename)
            image = Image.open(jpg_file_path)
            image.save(png_file, "PNG")
            return png_file

        self.create_single_file_conversion_window(
            "JPG",
            "PNG",
            [("JPG Files", "*.jpg"), ("JPEG Files", "*.jpeg")],
            (".jpg", ".jpeg"),
            converter,
        )

    def open_png_to_jpg(self):
        def converter(png_file_path):
            output_filename = os.path.basename(png_file_path).replace(".png", ".jpg")
            jpg_file = os.path.join(self.get_downloads_folder(), output_filename)
            image = Image.open(png_file_path)
            rgb_image = image.convert("RGB")
            rgb_image.save(jpg_file, "JPEG")
            return jpg_file

        self.create_single_file_conversion_window(
            "PNG",
            "JPG",
            [("PNG Files", "*.png")],
            (".png",),
            converter,
        )

    def open_webp_to_png(self):
        def converter(webp_file_path):
            output_filename = os.path.basename(webp_file_path).replace(".webp", ".png")
            png_file = os.path.join(self.get_downloads_folder(), output_filename)
            image = Image.open(webp_file_path)
            image.save(png_file, "PNG")
            return png_file

        self.create_single_file_conversion_window(
            "WEBP",
            "PNG",
            [("WEBP Files", "*.webp")],
            (".webp",),
            converter,
        )

    def open_png_to_webp(self):
        def converter(png_file_path):
            output_filename = os.path.basename(png_file_path).replace(".png", ".webp")
            webp_file = os.path.join(self.get_downloads_folder(), output_filename)
            image = Image.open(png_file_path)
            image.save(webp_file, "WEBP")
            return webp_file

        self.create_single_file_conversion_window(
            "PNG",
            "WEBP",
            [("PNG Files", "*.png")],
            (".png",),
            converter,
        )

    def merge_pdf(self):
        window, button = self.create_feature_window(
            "Merge PDF", "Merge PDF", geometry="500x400"
        )

        pdf_files = []

        frame = tk.Frame(window)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        listbox = tk.Listbox(frame, width=60, height=10)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        def add_pdf():
            files = filedialog.askopenfilenames(
                filetypes=[("PDF Files", "*.pdf")],
                title="Select PDF File",
                parent=window,
            )
            if files:
                for file in files:
                    if file not in pdf_files:
                        pdf_files.append(file)
                        listbox.insert(tk.END, file)

        def remove_selected_pdf():
            selected_pdf = listbox.curselection()
            for index in reversed(selected_pdf):
                listbox.delete(index)
                del pdf_files[index]

        def merge_pdfs():
            if not pdf_files:
                messagebox.showwarning(
                    "No PDFs Selected", "Please add at least one PDF to merge."
                )
                return

            if len(pdf_files) < 2:
                messagebox.showwarning(
                    "Not Enough PDFs", "Please add at least two PDFs to merge."
                )
                return

            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                parent=window,
            )
            if not save_path:
                return

            try:
                merger = PdfMerger()
                for pdf in pdf_files:
                    merger.append(pdf)
                merger.write(save_path)
                merger.close()
                messagebox.showinfo("Success", "PDFs merged successfully!")
            except Exception as error:
                messagebox.showerror("Error", f"An error occurred: {error}")

        tk.Button(window, text="Add PDF", command=add_pdf).pack(padx=0, pady=20)
        tk.Button(
            window,
            text="Remove Selected PDF",
            command=remove_selected_pdf,
            cursor="hand2",
        ).pack(padx=0, pady=20)
        tk.Button(
            window, text="Merge PDFs", command=merge_pdfs, cursor="hand2"
        ).pack(padx=0, pady=20)

        window.protocol(
            "WM_DELETE_WINDOW", lambda: self.close_feature_window(window, button)
        )

    def split_pdf(self):
        window, button = self.create_feature_window(
            "Split PDF", "Split PDF", geometry="500x400"
        )

        pdf_files = []

        frame = tk.Frame(window)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        listbox = tk.Listbox(frame, width=60, height=10)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        def add_pdf():
            file = filedialog.askopenfilename(
                filetypes=[("PDF Files", "*.pdf")],
                title="Select PDF File",
                parent=window,
            )
            if file and file not in pdf_files:
                pdf_files.append(file)
                listbox.insert(tk.END, file)

        def remove_selected_pdf():
            selected_pdf = listbox.curselection()
            for index in reversed(selected_pdf):
                listbox.delete(index)
                del pdf_files[index]

        def split_pdfs():
            if not pdf_files:
                messagebox.showwarning(
                    "No PDFs Selected", "Please add a PDF file to split."
                )
                return

            if len(pdf_files) >= 2:
                messagebox.showwarning(
                    "Cannot Accept Two PDFs",
                    "Cannot accept two PDFs to split, please provide only one PDF in the listbox !",
                )
                return

            for file_path in pdf_files:
                try:
                    pdf_reader = PdfReader(file_path)
                    total_pages = len(pdf_reader.pages)

                    output_folder = os.path.join(
                        os.path.dirname(file_path), "Split PDFs"
                    )
                    os.makedirs(output_folder, exist_ok=True)

                    base_name = os.path.basename(file_path).replace(".pdf", "")

                    for page_num in range(total_pages):
                        pdf_writer = PdfWriter()
                        pdf_writer.add_page(pdf_reader.pages[page_num])

                        output_path = os.path.join(
                            output_folder, f"{base_name}_page_{page_num + 1}.pdf"
                        )
                        with open(output_path, "wb") as output_pdf:
                            pdf_writer.write(output_pdf)

                    messagebox.showinfo(
                        "Success",
                        f"PDF split successfully!\nSaved in: {output_folder}",
                    )
                except Exception as error:
                    messagebox.showerror("Error", f"An error occurred: {error}")

        tk.Button(
            window, text="Add PDF", command=add_pdf, cursor="hand2"
        ).pack(padx=0, pady=20)
        tk.Button(
            window,
            text="Remove Selected PDF",
            command=remove_selected_pdf,
            cursor="hand2",
        ).pack(padx=0, pady=20)
        tk.Button(
            window, text="Split PDF", command=split_pdfs, cursor="hand2"
        ).pack(padx=0, pady=20)

        window.protocol(
            "WM_DELETE_WINDOW", lambda: self.close_feature_window(window, button)
        )


def main():
    root = tk.Tk()
    ConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()