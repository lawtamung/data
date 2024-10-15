import tkinter as tk
from tkinter import messagebox
import heapq

# ข้อมูลที่ใช้เก็บผลลัพธ์
users = []  # เก็บข้อมูลผู้ใช้
selected_line = ""  # เก็บสายรถที่เลือก
selected_path = ""  # เก็บเส้นทางที่เลือก (ต้นทาง -> ปลายทาง)
seats = [["A1", "A2", "A3", "A4"],
         ["B1", "B2", "B3", "B4"],
         ["C1", "C2", "C3", "C4"]]  # ที่นั่ง
booked_seats = []  # เก็บที่นั่งที่ถูกจองแล้ว

# ข้อมูลกราฟสาย
graph = {
    'เมือง': {'กุสุมาลย์': 41, 'โพนหาแก้ว': 38, 'โคกศรีสุพรรณ': 29, 'เต่างอย': 27, 'พรรณานิคม': 39, 'กุฬาน': 66},
    'กุสุมาลย์': {'เมือง': 41, 'โพนหาแก้ว': 23},
    'โพนหาแก้ว': {'กุสุมาลย์': 23, 'เมือง': 38, 'โคกศรีสุพรรณ': 26},
    'โคกศรีสุพรรณ': {'โพนหาแก้ว': 26, 'เมือง': 29, 'เต่างอย': 23},
    'เต่างอย': {'โคกศรีสุพรรณ': 23, 'เมือง': 27, 'กุฬาน': 38},
    'พรรณานิคม': {'เมือง': 39},
    'กุฬาน': {'เมือง': 66, 'เต่างอย': 38}
}

# ฟังก์ชันสำหรับการคำนวณเส้นทางสั้นที่สุด
def dijkstra(graph, start, goal):
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    shortest_path = {}

    while queue:
        (current_distance, current_node) = heapq.heappop(queue)

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = shortest_path.get(current_node, None)
            return distances[goal], path[::-1]

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                shortest_path[neighbor] = current_node

    return float('inf'), []

# ฟังก์ชันแสดงหน้าเลือกสถานที่ต้นทางและปลายทาง
def show_select_location_page():
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="เลือกสถานที่ต้นทางและปลายทาง", font=("Arial", 20, "bold"), bg="#FAFAFA", fg="#4A90E2")
    label.pack(pady=20)

    # ตัวเลือกสถานที่ต้นทางและปลายทาง
    start_label = tk.Label(root, text="ต้นทาง:", font=("Arial", 14), bg="#FAFAFA", fg="#4A90E2")
    start_label.pack()
    start_var.set(list(graph.keys())[0])  # ตั้งค่าต้นทางเริ่มต้น
    start_menu = tk.OptionMenu(root, start_var, *graph.keys())
    start_menu.pack(pady=10)

    goal_label = tk.Label(root, text="ปลายทาง:", font=("Arial", 14), bg="#FAFAFA", fg="#4A90E2")
    goal_label.pack()
    goal_var.set(list(graph.keys())[1])  # ตั้งค่าปลายทางเริ่มต้น
    goal_menu = tk.OptionMenu(root, goal_var, *graph.keys())
    goal_menu.pack(pady=10)

    # ปุ่มค้นหาเส้นทาง
    find_path_button = tk.Button(root, text="ค้นหาเส้นทาง", width=15, height=2, bg="#4A90E2", fg="white",
                                 font=("Arial", 14, "bold"), command=find_shortest_path)
    find_path_button.pack(pady=20)

# ฟังก์ชันสำหรับหาทางสั้นที่สุด
def find_shortest_path():
    start = start_var.get()
    goal = goal_var.get()
    if start not in graph or goal not in graph:
        messagebox.showerror("ข้อผิดพลาด", "ไม่มีข้อมูลของสายที่ระบุ")
        return
    distance, path = dijkstra(graph, start, goal)
    if distance == float('inf'):
        messagebox.showinfo("ผลลัพธ์", "ไม่มีเส้นทางจาก {} ไป {}".format(start, goal))
    else:
        global selected_path
        selected_path = " -> ".join(path)
        messagebox.showinfo("ผลลัพธ์", "เส้นทางที่สั้นที่สุดจาก {} ไป {} คือ: {} ระยะทาง: {} km".format(start, goal, selected_path, distance))
        show_select_line_page()  # ไปหน้าเลือกสาย

# ฟังก์ชันสำหรับยืนยันข้อมูลผู้ใช้และไปยังหน้าเลือกสถานที่
def submit_user_info():
    name = name_entry.get()
    phone = phone_entry.get()
    if name and phone:
        users.append({"name": name, "phone": phone})
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        show_select_location_page()  # ไปหน้าเลือกสถานที่
    else:
        messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอกชื่อและเบอร์โทรศัพท์")

# ฟังก์ชันแสดงหน้าเลือกสาย
def show_select_line_page():
    for widget in root.winfo_children():
        widget.destroy()
    
    last_user = users[-1]["name"]
    welcome_label = tk.Label(root, text=f"ยินดีต้อนรับ {last_user}!", font=("Arial", 16, "bold"), bg="#FAFAFA", fg="#4A90E2")
    welcome_label.pack(pady=20)
    
    label = tk.Label(root, text=f"เลือกสายรถเมล์ (เส้นทาง: {selected_path})", font=("Arial", 20, "bold"), bg="#FAFAFA", fg="#4A90E2")
    label.pack(pady=20)
    
    lines = ["เมือง-ภูพาน", "เมือง-เต่างอย", "เมือง-พรรณา", "เมือง-โพนหาแก้ว", "เมือง-โคกศรีสุพรรณ", "เมือง-กุสุมาลย์", "กุสุมาลย์-โพนหาแก้ว", "โพนหาแก้ว-โคกศรีสุพรรณ", "โคกศรีสุพรรณ-เต่างอย", "เต่างอย-ภูพาน"]
    for line in lines:
        line_button = tk.Button(root, text=line, width=20, height=1, bg="#4A90E2", fg="white", font=("Arial", 14, "bold"),
                                command=lambda l=line: select_line(l))
        line_button.pack(pady=10)

    # ปุ่มย้อนกลับไปยังหน้าเลือกสถานที่
    back_button = tk.Button(root, text="ย้อนกลับไปยังสถานที่", width=20, height=2, bg="#F39C12", fg="white",
                            font=("Arial", 14, "bold"), command=back_to_select_location)
    back_button.pack(pady=10)

# ฟังก์ชันสำหรับย้อนกลับไปยังหน้าเลือกสถานที่
def back_to_select_location():
    show_select_location_page()  # แสดงหน้าเลือกสถานที่

# ฟังก์ชันสำหรับการเลือกสาย
def select_line(line):
    global selected_line
    selected_line = line
    show_select_seat_page()

# ฟังก์ชันแสดงหน้าเลือกที่นั่ง
def show_select_seat_page():
    for widget in root.winfo_children():
        widget.destroy()
    
    label = tk.Label(root, text=f"เลือกที่นั่ง (สาย {selected_line})", font=("Arial", 20, "bold"), bg="#FAFAFA", fg="#4A90E2")
    label.pack(pady=20)

    # สร้างปุ่มเลือกที่นั่ง
    for row in seats:
        seat_frame = tk.Frame(root, bg="#FAFAFA")
        seat_frame.pack(pady=5)
        for seat in row:
            color = "green" if seat not in booked_seats else "red"
            seat_button = tk.Button(seat_frame, text=seat, width=5, height=2, bg=color, fg="white",
                                    font=("Arial", 12, "bold"),
                                    state=tk.NORMAL if seat not in booked_seats else tk.DISABLED,
                                    command=lambda s=seat: select_seat(s))
            seat_button.pack(side=tk.LEFT, padx=5)

    # ปุ่มยกเลิกที่นั่ง
    cancel_button = tk.Button(root, text="ยกเลิกที่นั่ง", width=15, height=2, bg="#D0021B", fg="white",
                              font=("Arial", 14, "bold"), command=cancel_booking)
    cancel_button.pack(pady=20)

    # ปุ่มยืนยันการจองที่นั่ง
    confirm_button = tk.Button(root, text="ยืนยันการจองที่นั่ง", width=15, height=2, bg="#4A90E2", fg="white",
                                font=("Arial", 14, "bold"), command=confirm_booking)
    confirm_button.pack(pady=20)

# ฟังก์ชันสำหรับเลือกที่นั่ง
def select_seat(seat):
    if seat in booked_seats:
        messagebox.showwarning("ที่นั่งถูกจองแล้ว", "กรุณาเลือกที่นั่งอื่น")
    else:
        booked_seats.append(seat)
        messagebox.showinfo("ที่นั่งเลือกแล้ว", f"คุณได้เลือกที่นั่ง {seat}")

# ฟังก์ชันสำหรับยกเลิกที่นั่ง
def cancel_booking():
    if booked_seats:
        seat_to_cancel = booked_seats.pop()
        messagebox.showinfo("ยกเลิกการจองที่นั่ง", f"คุณได้ยกเลิกการจองที่นั่ง {seat_to_cancel}")
    else:
        messagebox.showwarning("ไม่มีที่นั่งที่ถูกจอง", "คุณยังไม่ได้จองที่นั่งใด ๆ")

# ฟังก์ชันสำหรับยืนยันการจองที่นั่ง
def confirm_booking():
    if booked_seats:
        messagebox.showinfo("การจองที่นั่งเสร็จสมบูรณ์", f"คุณได้จองที่นั่ง {', '.join(booked_seats)} ในสาย {selected_line}")
        booked_seats.clear()  # ล้างที่นั่งที่ถูกจองหลังการยืนยัน
        show_select_location_page()  # กลับไปหน้าเลือกสถานที่
    else:
        messagebox.showwarning("ไม่มีที่นั่งที่ถูกจอง", "กรุณาเลือกที่นั่งก่อนที่จะยืนยันการจอง")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("ระบบจองที่นั่งรถเมล์")
root.geometry("400x600")
root.configure(bg="#FAFAFA")

# ตัวแปรสำหรับสถานที่
start_var = tk.StringVar()
goal_var = tk.StringVar()

# ตัวกรอกข้อมูลผู้ใช้
name_label = tk.Label(root, text="ชื่อ:", font=("Arial", 14), bg="#FAFAFA", fg="#4A90E2")
name_label.pack(pady=10)
name_entry = tk.Entry(root, font=("Arial", 14))
name_entry.pack(pady=10)

phone_label = tk.Label(root, text="เบอร์โทรศัพท์:", font=("Arial", 14), bg="#FAFAFA", fg="#4A90E2")
phone_label.pack(pady=10)
phone_entry = tk.Entry(root, font=("Arial", 14))
phone_entry.pack(pady=10)

submit_button = tk.Button(root, text="ยืนยันข้อมูล", width=20, height=2, bg="#4A90E2", fg="white",
                          font=("Arial", 14, "bold"), command=submit_user_info)
submit_button.pack(pady=20)

# เริ่มต้นแสดงหน้าแรก
root.mainloop()
