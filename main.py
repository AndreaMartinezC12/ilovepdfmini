import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PyPDF2 import PdfMerger, PdfReader, PdfWriter


class PDFApp:
    def __init__(self,root):
        self.root = root
        self.root.title("Mini IlovePDF")
        self.root.geometry("400x300")
        self.pdf_files=[]

        ttk.Button(root, text="+ agregar pdf", command=self.select_pdfs).pack(pady=10)
        ttk.Button(root, text="unir pdf", command=self.merge_pdfs).pack(pady=10)
        ttk.Button(root, text="dividir pdf", command=self.split_pdf).pack(pady=10)
        ttk.Button(root, text="dividir pdf por paginas", command=self.split_pdf_perpage).pack(pady=10)
        self.listbox = tk.Listbox(root, width=80, height=15)
        self.listbox.pack(pady=10)
        #ttk.Button(root, text="- comprimir pdf", command=self.compress_pdfs).pack(pady=10)


    def select_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        self.pdf_files= list(files)
        messagebox.showinfo("Seleccionados",f"{len(files)} archivos seleccionados")

        for i in range(0, (len(self.pdf_files))):
            self.listbox.insert(tk.END, self.pdf_files[i])
    
    def merge_pdfs(self):
        if len(self.pdf_files)<2:
            messagebox.showwarning("Advertencia", "Para esta funcion se necesitan minimo 2 archivos")
            return
        merger = PdfMerger()
        for pdf in self.pdf_files:
            merger.append(pdf)

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if output_path:
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Exito", f"PDFs_unidos en {output_path}")

    def split_pdf(self):
        if not self.pdf_files:
            messagebox.showwarning("Advertencia", "Tienes que seleccionar un pdf")
            return
        pdf_path=self.pdf_files[0]
        reader=PdfReader(pdf_path)
        total_pages=len(reader.pages)
        rango=tk.simpledialog.askstring("Dividir", f"Total de paginas:{total_pages}\n Ingresa rango (ej.1-3)")
        if not rango:
            return
        inicio, fin = map(int, rango.split("-"))
        writer=PdfWriter()
        for i in range(inicio-1, fin):
            writer.add_page(reader.pages[i])
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf")

        if output_path:
            with open(output_path,"wb") as f:
                writer.write(f)
            messagebox.showinfo("Exito", "Archivo dividido guardado")
        
    def split_pdf_perpage(self):
        if not self.pdf_files:
            messagebox.showwarning("Advertencia", "Tienes que seleccionar un pdf")
            return
        pdf_path=self.pdf_files[0]
        reader=PdfReader(pdf_path)
        total_pages=len(reader.pages)
        rango=tk.simpledialog.askstring("Dividir", f"Total de paginas:{total_pages}\n Ingresa las paginas a conservar (ej.1-3-4)")
        if not rango:
            return
        paginasselec = map(int, rango.split("-"))
        pagsselect = list(paginasselec)
        print(len(pagsselect))
        writer=PdfWriter()
        for i in range(0, (len(pagsselect))):
            print(i)
            print(pagsselect[i])
            writer.add_page(reader.pages[(pagsselect[i]-1)])
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf")

        if output_path:
            with open(output_path,"wb") as f:
                writer.write(f)
            messagebox.showinfo("Exito", "Archivo dividido guardado")

if __name__ == "__main__":
    root =tk.Tk()
    app = PDFApp(root)
    root.mainloop()
