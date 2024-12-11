import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import pandas as pd
root = tk.Tk()
root.title("Thông tin nhân viên")
CSV_FILE = "nhan_vien.csv"
HEADER = ["Mã", "Tên", "Đơn vị", "Chức danh", "Ngày sinh", "Giới tính", "Số CMND", "Nơi cấp", "Ngày cấp"]
try:
    with open(CSV_FILE, "x", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
except FileExistsError:
    pass
def save_data():
    data = [
        entry_ma.get(),
        entry_ten.get(),
        entry_don_vi.get(),
        entry_chuc_danh.get(),
        entry_ngay_sinh.get(),
        gender_var.get(),
        entry_cmnd.get(),
        entry_noi_cap.get(),
        entry_ngay_cap.get()
    ]
    if any(not field for field in data):
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")
        return
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data)
    messagebox.showinfo("Thành công", "Dữ liệu đã được lưu")
    clear_fields()
def clear_fields():
    entry_ma.delete(0, tk.END)
    entry_ten.delete(0, tk.END)
    entry_don_vi.delete(0, tk.END)
    entry_chuc_danh.delete(0, tk.END)
    entry_ngay_sinh.delete(0, tk.END)
    entry_cmnd.delete(0, tk.END)
    entry_noi_cap.delete(0, tk.END)
    entry_ngay_cap.delete(0, tk.END)
    gender_var.set("")
def show_today_birthdays():
    today = datetime.now().strftime("%d/%m/%Y")
    results = []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Ngày sinh"] == today:
                results.append(row)
    if results:
        result_str = "\n".join([f"{r['Mã']} - {r['Tên']}" for r in results])
        messagebox.showinfo("Sinh nhật hôm nay", result_str)
    else:
        messagebox.showinfo("Sinh nhật hôm nay", "Không có nhân viên nào sinh nhật hôm nay")

def export_sorted_excel():
    df = pd.read_csv(CSV_FILE)
    try:
        df["Ngày sinh"] = pd.to_datetime(df["Ngày sinh"], format="%d/%m/%Y")
        df_sorted = df.sort_values(by="Ngày sinh", ascending=True)
        output_file = "nhan_vien_sorted.xlsx"
        df_sorted.to_excel(output_file, index=False)
        messagebox.showinfo("Thành công", f"File đã được xuất: {output_file}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xuất file: {e}")
labels = ["Mã", "Tên", "Đơn vị", "Chức danh", "Ngày sinh (DD/MM/YYYY)", "Giới tính", "Số CMND", "Nơi cấp", "Ngày cấp"]
entry_ma = ttk.Entry(root)
entry_ten = ttk.Entry(root)
entry_don_vi = ttk.Entry(root)
entry_chuc_danh = ttk.Entry(root)
entry_ngay_sinh = ttk.Entry(root)
entry_cmnd = ttk.Entry(root)
entry_noi_cap = ttk.Entry(root)
entry_ngay_cap = ttk.Entry(root)
entries = [entry_ma, entry_ten, entry_don_vi, entry_chuc_danh, entry_ngay_sinh, entry_cmnd, entry_noi_cap, entry_ngay_cap]
gender_var = tk.StringVar()
radiobutton_male = ttk.Radiobutton(root, text="Nam", variable=gender_var, value="Nam")
radiobutton_female = ttk.Radiobutton(root, text="Nữ", variable=gender_var, value="Nữ")

for i, label in enumerate(labels):
    ttk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
for i, entry in enumerate(entries):
    entry.grid(row=i, column=1, padx=10, pady=5, sticky=tk.W)
radiobutton_male.grid(row=5, column=1, sticky=tk.W)
radiobutton_female.grid(row=5, column=1, padx=60, sticky=tk.W)

btn_save = ttk.Button(root, text="Lưu", command=save_data)
btn_birthday = ttk.Button(root, text="Sinh nhật hôm nay", command=show_today_birthdays)
btn_export = ttk.Button(root, text="Xuất toàn bộ danh sách", command=export_sorted_excel)
btn_save.grid(row=9, column=0, padx=10, pady=10, sticky=tk.W)
btn_birthday.grid(row=9, column=1, padx=10, pady=10, sticky=tk.W)
btn_export.grid(row=10, column=0, padx=10, pady=10, sticky=tk.W)
root.mainloop()
