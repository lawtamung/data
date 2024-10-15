import tkinter as tk
from tkinter import messagebox
import heapq

# สร้างกราฟจากข้อมูลในภาพ
graph = {
    'เมือง': {'กุสุมาลย์': 41, 'โพนหาแก้ว': 38, 'โคกศรีสุพรรณ': 29, 'เต่างอย': 27, 'พรรณานิคม': 39, 'กุฬาน': 66},
    'กุสุมาลย์': {'เมือง': 41, 'โพนหาแก้ว': 23},
    'โพนหาแก้ว': {'กุสุมาลย์': 23, 'เมือง': 38, 'โคกศรีสุพรรณ': 26},
    'โคกศรีสุพรรณ': {'โพนหาแก้ว': 26, 'เมือง': 29, 'เต่างอย': 23},
    'เต่างอย': {'โคกศรีสุพรรณ': 23, 'เมือง': 27, 'กุฬาน': 38},
    'พรรณานิคม': {'เมือง': 39},
    'กุฬาน': {'เมือง': 66, 'เต่างอย': 38}
}

# ฟังก์ชันหาทางที่สั้นที่สุดโดยใช้ Dijkstra's Algorithm
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

# ฟังก์ชันแสดงผลลัพธ์เส้นทางที่สั้นที่สุด
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
        messagebox.showinfo("ผลลัพธ์", "เส้นทางที่สั้นที่สุดจาก {} ไป {} คือ: {} ระยะทาง: {} km".format(start, goal, ' -> '.join(path), distance))

# สร้าง GUI
root = tk.Tk()
root.title("ค้นหาเส้นทางที่สั้นที่สุด")
root.geometry("400x300")

# รายการสถานีทั้งหมดในดรอปดาวน์
stations = list(graph.keys())

# ตัวแปรเก็บค่าสถานีต้นทางและปลายทาง
start_var = tk.StringVar(root)
goal_var = tk.StringVar(root)

# ตั้งค่าเริ่มต้นในดรอปดาวน์
start_var.set(stations[0])
goal_var.set(stations[1])

# ป้ายบอกให้ผู้ใช้เลือกข้อมูล
start_label = tk.Label(root, text="ต้นทาง:", font=("Arial", 14))
start_label.pack(pady=10)

# สร้างดรอปดาวน์สำหรับเลือกต้นทาง
start_menu = tk.OptionMenu(root, start_var, *stations)
start_menu.pack(pady=10)

goal_label = tk.Label(root, text="ปลายทาง:", font=("Arial", 14))
goal_label.pack(pady=10)

# สร้างดรอปดาวน์สำหรับเลือกปลายทาง
goal_menu = tk.OptionMenu(root, goal_var, *stations)
goal_menu.pack(pady=10)

# ปุ่มเพื่อค้นหาเส้นทาง
search_button = tk.Button(root, text="ค้นหาเส้นทาง", font=("Arial", 14), command=find_shortest_path)
search_button.pack(pady=20)

root.mainloop()
