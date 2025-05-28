import tkinter as tk
from tkinter import messagebox
import threading

from data.unegui_scraper import scrape_unegui
from vectorstore.vectorstore_builder import build_vectorstore
from analysis.group_listings import group_listings
from search.web_search import search_web_results
from report.pdf_report_generator import generate_pdf

def run_pipeline(query):
    try:
        log_text.set("Өгөгдөл татаж байна...")
        scrape_unegui()
        log_text.set("Өгөгдөл таталт дууслаа.")

        log_text.set("Вектор сан үүсгэж байна...")
        build_vectorstore()
        log_text.set("Вектор сан үүсгэлээ.")

        log_text.set("Бүлэглэл үүсгэж байна...")
        group_listings()
        log_text.set("Бүлэглэл амжилттай.")

        log_text.set("Интернетээс хайлт хийж байна...")
        search_web_results(query)
        log_text.set("Хайлтын үр дүн амжилттай.")

        log_text.set("📄 Тайлан PDF болгон үүсгэж байна...")
        generate_pdf(query)
        log_text.set("Тайлан бүрэн бэлэн боллоо.")

        messagebox.showinfo("Тайлан бэлэн!", "Тайлан амжилттай үүсгэгдлээ!")
    except Exception as e:
        messagebox.showerror("Алдаа", str(e))

def start_pipeline():
    query = search_entry.get()
    if not query:
        messagebox.showwarning("Анхааруулга", "Хайлтын түлхүүр үг оруулна уу.")
        return
    threading.Thread(target=run_pipeline, args=(query,), daemon=True).start()

root = tk.Tk()
root.title("Үл хөдлөх хөрөнгийн туслах - Тайлан үүсгэгч")
root.geometry("500x300")

tk.Label(root, text="Хайлтын түлхүүр үг:").pack(pady=10)
search_entry = tk.Entry(root, width=50)
search_entry.pack(pady=5)

generate_button = tk.Button(root, text="Тайлан үүсгэх", command=start_pipeline, bg="#4CAF50", fg="white", font=("Arial", 12))
generate_button.pack(pady=20)

log_text = tk.StringVar()
log_text.set("Систем бэлэн байна.")
log_label = tk.Label(root, textvariable=log_text, wraplength=450, justify="left")
log_label.pack(pady=10)

root.mainloop()
