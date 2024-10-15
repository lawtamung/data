import tkinter as tk
from tkinter import messagebox

# ข้อมูลที่ใช้เก็บผลลัพธ์
users = []  # เก็บข้อมูลผู้ใช้
selected_line = ""  # เก็บสายรถที่เลือก
seats = [["A1", "A2", "A3", "A4"],
         ["B1", "B2", "B3", "B4"],
         ["C1", "C2", "C3", "C4"]]  # ที่นั่ง
booked_seats = []  # เก็บที่นั่งที่ถูกจองแล้ว

# ฟังก์ชันสำหรับยืนยันข้อมูลผู้ใช้และไปยังหน้าเลือกสาย
def submit_user_info():
    name = name_entry.get()
    phone = phone_entry.get()
    if name and phone:
        users.append({"name": name, "phone": phone})
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        show_select_line_page()
    else:
        messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอกชื่อและเบอร์โทรศัพท์")

# ฟังก์ชันแสดงหน้าเลือกสาย
def show_select_line_page():
    for widget in root.winfo_children():
        widget.destroy()
    
    label = tk.Label(root, text="เลือกสายรถเมล์", font=("Arial", 16))
    label.pack(pady=20)
    
    # สายรถเมล์ที่ให้เลือก
    lines = ["สาย 1", "สาย 2", "สาย 3"]
    
    for line in lines:
        line_button = tk.Button(root, text=line, width=20, height=2, command=lambda l=line: select_line(l))
        line_button.pack(pady=10)

    # เพิ่มปุ่มยกเลิก
    cancel_button = tk.Button(root, text="ยกเลิก", width=10, height=2, command=show_user_info_page)
    cancel_button.pack(pady=20)

# ฟังก์ชันสำหรับการเลือกสาย
def select_line(line):
    global selected_line
    selected_line = line
    show_select_seat_page()

# ฟังก์ชันแสดงหน้าเลือกที่นั่ง
def show_select_seat_page():
    for widget in root.winfo_children():
        widget.destroy()
    
    label = tk.Label(root, text=f"เลือกที่นั่ง (สาย {selected_line})", font=("Arial", 16))
    label.pack(pady=20)

    # สร้างปุ่มเลือกที่นั่ง
    for row in seats:
        seat_frame = tk.Frame(root)
        seat_frame.pack()
        for seat in row:
            color = "green" if seat not in booked_seats else "red"
            seat_button = tk.Button(seat_frame, text=seat, width=5, height=2, bg=color,
                                    state=tk.NORMAL if seat not in booked_seats else tk.DISABLED,
                                    command=lambda s=seat: select_seat(s))
            seat_button.pack(side=tk.LEFT, padx=5, pady=5)

    # เพิ่มปุ่มยกเลิก
    cancel_button = tk.Button(root, text="ยกเลิก", width=10, height=2, command=show_user_info_page)
    cancel_button.pack(pady=20)

# ฟังก์ชันสำหรับเลือกที่นั่ง
def select_seat(seat):
    booked_seats.append(seat)  # บันทึกที่นั่ง
    messagebox.showinfo("สำเร็จ", f"จองที่นั่ง {seat} สำเร็จ!")
    show_select_seat_page()  # รีเฟรชหน้าเลือกที่นั่ง

# ฟังก์ชันแสดงหน้ารับข้อมูลผู้ใช้
def show_user_info_page():
    global name_entry, phone_entry
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="กรอกข้อมูลผู้ใช้", font=("Arial", 16))
    label.pack(pady=20)

    name_label = tk.Label(root, text="ชื่อ:")
    name_label.pack()
    name_entry = tk.Entry(root)
    name_entry.pack(pady=5)

    phone_label = tk.Label(root, text="เบอร์โทรศัพท์:")
    phone_label.pack()
    phone_entry = tk.Entry(root)
    phone_entry.pack(pady=5)

    submit_button = tk.Button(root, text="OK", width=10, height=2, command=submit_user_info)
    submit_button.pack(pady=20)

# เริ่มต้นโปรแกรม
root = tk.Tk()
root.title("ระบบจองตั๋วรถเมล์")
root.geometry("400x400")

# แสดงหน้ารับข้อมูลผู้ใช้
show_user_info_page()

root.mainloop()
