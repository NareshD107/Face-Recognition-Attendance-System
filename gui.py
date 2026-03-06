import os
import sys
from datetime import datetime
import shutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import email_utils
import pdf_utils
import cv2
from PIL import Image, ImageTk
import threading
import time
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import database
from recognition_engine import RecognitionEngine
import attendance

# System Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        print("[INFO] Starting Face Recognition GUI v3.0 (Professional Phase 2)")
        
        self.camera_running = False
        self.cap = None
        self.engine = RecognitionEngine()

        self.title("Face Recognition Attendance System")
        self.geometry("1100x600")

        # set grid layout 1x2
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # load images (placeholders for now if needed, or use icons)
        
        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1) # Spacer row

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  MENU", 
                                                 font=ctk.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Dashboard",
                                               fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                               anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.students_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Students",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_2_button_event)
        self.students_button.grid(row=2, column=0, sticky="ew")

        self.reports_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Attendance Logs",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_3_button_event)
        self.reports_button.grid(row=3, column=0, sticky="ew")

        self.analytics_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Analytics",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_5_button_event)
        self.analytics_button.grid(row=4, column=0, sticky="ew")

        self.settings_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="System Utilities",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_4_button_event)
        self.settings_button.grid(row=5, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=10, sticky="s")

        self.exit_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Exit",
                                              fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                              anchor="w", command=self.quit)
        self.exit_button.grid(row=8, column=0, sticky="ew")

        # Create Frames
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_home_frame()

        self.students_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_students_frame()

        self.reports_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_reports_frame()

        self.settings_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_settings_frame()

        self.analytics_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.setup_analytics_frame()

        # select default frame
        self.select_frame_by_name("home")

    def setup_home_frame(self):
        self.home_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(self.home_frame, text="Welcome to Attendance System", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=20)

        # Session Input
        session_frame = ctk.CTkFrame(self.home_frame)
        session_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(session_frame, text="Session/Subject Name:").pack(side="left", padx=10, pady=10)
        self.session_entry = ctk.CTkEntry(session_frame, placeholder_text="e.g. Math, OS")
        self.session_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.start_btn = ctk.CTkButton(self.home_frame, text="🚀 START CAMERA FEED", height=50, 
                                      font=ctk.CTkFont(size=16, weight="bold"), command=self.toggle_camera)
        self.start_btn.pack(pady=10, padx=20, fill="x")

        # Camera Display Label
        self.camera_label = ctk.CTkLabel(self.home_frame, text="Camera Offline", width=640, height=360, fg_color="black")
        self.camera_label.pack(pady=10)

        # Stats placeholders
        stats_frame = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        stats_frame.pack(pady=20, padx=20, fill="both", expand=True)
        stats_frame.grid_columnconfigure((0, 1), weight=1)

        self.total_students_card = ctk.CTkFrame(stats_frame, height=150)
        self.total_students_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.total_students_card, text="Total Students", font=ctk.CTkFont(size=14)).pack(pady=10)
        self.total_students_val = ctk.CTkLabel(self.total_students_card, text="0", font=ctk.CTkFont(size=36, weight="bold"))
        self.total_students_val.pack(pady=10)

        self.today_attendance_card = ctk.CTkFrame(stats_frame, height=150)
        self.today_attendance_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.today_attendance_card, text="Today's Attendance", font=ctk.CTkFont(size=14)).pack(pady=10)
        self.today_attendance_val = ctk.CTkLabel(self.today_attendance_card, text="0", font=ctk.CTkFont(size=36, weight="bold"))
        self.today_attendance_val.pack(pady=10)
        
        self.refresh_stats()

    def setup_students_frame(self):
        title_label = ctk.CTkLabel(self.students_frame, text="Student Management", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=20)

        btns_frame = ctk.CTkFrame(self.students_frame, fg_color="transparent")
        btns_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(btns_frame, text="Register New Student", command=self.add_student_ui).pack(side="left", padx=5)
        ctk.CTkButton(btns_frame, text="Update Student", command=self.update_student_ui).pack(side="left", padx=5)
        ctk.CTkButton(btns_frame, text="Delete Student", fg_color="red", hover_color="darkred", command=self.delete_student_ui).pack(side="left", padx=5)
        
        ctk.CTkLabel(btns_frame, text="Search:").pack(side="left", padx=(20, 5))
        self.student_search_entry = ctk.CTkEntry(btns_frame, placeholder_text="Name or Roll...", width=150)
        self.student_search_entry.pack(side="left", padx=5)
        ctk.CTkButton(btns_frame, text="🔍", width=40, command=self.refresh_students).pack(side="left", padx=5)

        ctk.CTkButton(btns_frame, text="Refresh All", command=lambda: self.refresh_students(clear_search=True)).pack(side="left", padx=5)

        # Student Table (Using Treeview for advanced fields)
        self.student_tree = ttk.Treeview(self.students_frame, columns=("Name", "Roll", "Dept", "Email"), show='headings')
        self.student_tree.heading("Name", text="Name")
        self.student_tree.heading("Roll", text="Roll No")
        self.student_tree.heading("Dept", text="Dept")
        self.student_tree.heading("Email", text="Email")
        self.student_tree.pack(pady=20, padx=20, fill="both", expand=True)
        self.refresh_students()

    def setup_reports_frame(self):
        title_label = ctk.CTkLabel(self.reports_frame, text="Attendance Logs & Reports", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=20)
        
        ctrl_frame = ctk.CTkFrame(self.reports_frame, fg_color="transparent")
        ctrl_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(ctrl_frame, text="Export CSV", command=self.export_report).pack(side="left", padx=5)
        ctk.CTkButton(ctrl_frame, text="Export PDF Report", command=self.export_pdf).pack(side="left", padx=5)
        
        ctk.CTkLabel(ctrl_frame, text="Search Date:").pack(side="left", padx=(20, 5))
        self.search_date_entry = ctk.CTkEntry(ctrl_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.search_date_entry.pack(side="left", padx=5)
        ctk.CTkButton(ctrl_frame, text="🔍 Search", width=80, command=self.refresh_logs).pack(side="left", padx=5)
        
        ctk.CTkButton(ctrl_frame, text="Refresh All", command=lambda: self.refresh_logs(clear_search=True)).pack(side="left", padx=5)

        # Logs Table (using Treeview for multi-column)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])
        
        self.tree = ttk.Treeview(self.reports_frame, columns=("Name", "Date", "Time", "Session"), show='headings')
        self.tree.heading("Name", text="Student Name")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Session", text="Session")
        self.tree.pack(pady=20, padx=20, fill="both", expand=True)
        self.refresh_logs()

    def setup_analytics_frame(self):
        title_label = ctk.CTkLabel(self.analytics_frame, text="Attendance Analytics & Trends", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=20)
        
        self.charts_container = ctk.CTkScrollableFrame(self.analytics_frame, fg_color="transparent")
        self.charts_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.refresh_analytics_btn = ctk.CTkButton(self.analytics_frame, text="Update Charts", command=self.render_charts)
        self.refresh_analytics_btn.pack(pady=10)

    def render_charts(self):
        # Clear previous charts
        for widget in self.charts_container.winfo_children():
            widget.destroy()

        # Trend Chart (Days vs Count)
        trends = database.get_attendance_trends()
        if trends:
            dates = [t[0] for t in trends]
            counts = [t[1] for t in trends]
            
            fig1, ax1 = plt.subplots(figsize=(6, 4), dpi=100)
            fig1.patch.set_facecolor('#2b2b2b')
            ax1.set_facecolor('#2b2b2b')
            ax1.bar(dates, counts, color='#1f538d')
            ax1.set_title("Attendance Trend (Last 7 Days)", color='white')
            ax1.tick_params(axis='x', colors='white', rotation=45)
            ax1.tick_params(axis='y', colors='white')
            fig1.tight_layout()
            
            canvas1 = FigureCanvasTkAgg(fig1, master=self.charts_container)
            canvas1.draw()
            canvas1.get_tk_widget().pack(pady=20, fill="x")

        # Top Attendees Chart (Horizontal Bar)
        top = database.get_top_attendees()
        if top:
            names = [t[0].replace("_", " ") for t in top]
            counts = [t[1] for t in top]
            
            fig2, ax2 = plt.subplots(figsize=(6, 4), dpi=100)
            fig2.patch.set_facecolor('#2b2b2b')
            ax2.set_facecolor('#2b2b2b')
            ax2.barh(names, counts, color='#2fa572')
            ax2.set_title("Top 5 Attendees", color='white')
            ax2.tick_params(axis='x', colors='white')
            ax2.tick_params(axis='y', colors='white')
            fig2.tight_layout()
            
            canvas2 = FigureCanvasTkAgg(fig2, master=self.charts_container)
            canvas2.draw()
            canvas2.get_tk_widget().pack(pady=20, fill="x")

        # Department Distribution Chart (Pie)
        dept_data = database.get_attendance_by_department()
        if dept_data:
            # ... existing pie chart code ...
            depts = [d[0] if d[0] else "Unknown" for d in dept_data]
            counts = [d[1] for d in dept_data]
            
            fig3, ax3 = plt.subplots(figsize=(6, 4), dpi=100)
            fig3.patch.set_facecolor('#2b2b2b')
            ax3.set_facecolor('#2b2b2b')
            ax3.pie(counts, labels=depts, autopct='%1.1f%%', textprops={'color':"white"}, colors=['#1f538d', '#2fa572', '#ff7f0e', '#d62728'])
            ax3.set_title("Attendance by Department", color='white')
            fig3.tight_layout()
            
            canvas3 = FigureCanvasTkAgg(fig3, master=self.charts_container)
            canvas3.draw()
            canvas3.get_tk_widget().pack(pady=20, fill="x")

        if not trends and not top and not dept_data:
            ctk.CTkLabel(self.charts_container, text="No attendance data found to generate charts.\nMark some attendance first!", font=ctk.CTkFont(size=14)).pack(pady=100)

    def setup_settings_frame(self):
        title_label = ctk.CTkLabel(self.settings_frame, text="System Utilities & Email Settings", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=20)
        
        # Email Config Section
        email_frame = ctk.CTkFrame(self.settings_frame)
        email_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(email_frame, text="SMTP Email Notification Settings", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        self.sender_entry = ctk.CTkEntry(email_frame, placeholder_text="Sender Email (e.g. gmail)")
        self.sender_entry.pack(pady=5, padx=20, fill="x")
        
        self.password_entry = ctk.CTkEntry(email_frame, placeholder_text="App Password", show="*")
        self.password_entry.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkButton(email_frame, text="Save Email Config", command=self.save_email_settings).pack(pady=10)
        
        # Load existing config if available
        config = email_utils.load_config()
        if config:
            self.sender_entry.insert(0, config.get("sender_email", ""))
            self.password_entry.insert(0, config.get("app_password", ""))

        # Utility buttons
        utils_grid = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        utils_grid.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkButton(utils_grid, text="Generate Face Encodings", height=40, command=self.run_encoding).pack(pady=10, fill="x")
        ctk.CTkButton(utils_grid, text="Check Camera Connection", height=40, command=self.check_camera).pack(pady=10, fill="x")
        ctk.CTkButton(utils_grid, text="Clear All Attendance Logs", height=40, fg_color="red", hover_color="darkred", command=self.clear_logs).pack(pady=10, fill="x")

    def save_email_settings(self):
        sender = self.sender_entry.get().strip()
        pwd = self.password_entry.get().strip()
        if sender and pwd:
            email_utils.save_config(sender, pwd)
            messagebox.showinfo("Success", "Email configuration saved!")
        else:
            messagebox.showerror("Error", "Please fill both fields.")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.students_button.configure(fg_color=("gray75", "gray25") if name == "students" else "transparent")
        self.reports_button.configure(fg_color=("gray75", "gray25") if name == "reports" else "transparent")
        self.analytics_button.configure(fg_color=("gray75", "gray25") if name == "analytics" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "students":
            self.students_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.students_frame.grid_forget()
        if name == "reports":
            self.reports_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.reports_frame.grid_forget()
        if name == "analytics":
            self.analytics_frame.grid(row=0, column=1, sticky="nsew")
            self.render_charts()
        else:
            self.analytics_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")
        self.refresh_stats()

    def frame_2_button_event(self):
        self.select_frame_by_name("students")
        self.refresh_students()

    def frame_3_button_event(self):
        self.select_frame_by_name("reports")
        self.refresh_logs()

    def frame_4_button_event(self):
        self.select_frame_by_name("settings")

    def frame_5_button_event(self):
        self.select_frame_by_name("analytics")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    # Actions
    def refresh_stats(self):
        students = database.get_all_students()
        today_att = database.get_today_summary()
        self.total_students_val.configure(text=str(len(students)))
        self.today_attendance_val.configure(text=str(len(today_att)))

    def refresh_students(self, clear_search=False):
        if clear_search:
            self.student_search_entry.delete(0, tk.END)
        
        search_query = self.student_search_entry.get().strip().lower()

        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        students = database.get_all_students_full()
        for s in students:
            name, roll, dept, email = s
            # Simple filter
            if search_query and search_query not in name.lower() and search_query not in str(roll).lower():
                continue
            self.student_tree.insert("", tk.END, values=(name.replace("_", " "), roll, dept, email))

    def refresh_logs(self, clear_search=False):
        if clear_search:
            self.search_date_entry.delete(0, tk.END)
        
        date_query = self.search_date_entry.get().strip()
        if not date_query:
            date_query = None

        for item in self.tree.get_children():
            self.tree.delete(item)
        
        logs = database.get_logs_by_date(date_query)
        for log in logs:
            name, date, time, subject = log
            self.tree.insert("", tk.END, values=(name, date, time, subject if subject else "General"))

    def toggle_camera(self):
        if not self.camera_running:
            subject = self.session_entry.get().strip()
            if not subject:
                subject = "General"
            self.session_id = database.create_session(subject)
            
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open camera.")
                return
            
            self.camera_running = True
            self.start_btn.configure(text="🛑 STOP CAMERA FEED", fg_color="red")
            
            # Start camera thread
            threading.Thread(target=self.camera_stream, daemon=True).start()
        else:
            self.camera_running = False
            self.start_btn.configure(text="🚀 START CAMERA FEED", fg_color=["#3B8ED0", "#1F6AA5"])
            if self.cap:
                self.cap.release()
            self.camera_label.configure(image="", text="Camera Offline")

    def camera_stream(self):
        blink_state = {}
        
        while self.camera_running:
            ret, frame = self.cap.read()
            if not ret: break
            
            # Process using engine
            results, blink_state = self.engine.process_frame(frame, blink_state)
            
            for res in results:
                name = res["name"]
                top, right, bottom, left = res["location"]
                confidence = res["confidence"]
                has_blinked = res["has_blinked"]

                if name == "Unknown":
                    color = (0, 0, 255)
                    display_text = name
                elif not has_blinked:
                    color = (0, 255, 255)
                    display_text = f"{name} ({confidence}%) - Blink!"
                else:
                    color = (0, 255, 0)
                    display_text = f"{name} ({confidence}%)"
                    attendance.mark_attendance(name, self.session_id)
                
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, display_text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Convert to PhotoImage
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img.thumbnail((640, 360))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            
            self.camera_label.configure(image=ctk_img, text="")
            time.sleep(0.01)

    def start_attendance(self):
        pass # Replaced by toggle_camera

    def add_student_ui(self):
        # Create a custom popup with multiple entries
        popup = ctk.CTkToplevel(self)
        popup.title("Register Student")
        popup.geometry("400x500")
        popup.attributes("-topmost", True)
        
        ctk.CTkLabel(popup, text="Professional Registration", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        ctk.CTkLabel(popup, text="Student Name:").pack(pady=2)
        name_entry = ctk.CTkEntry(popup)
        name_entry.pack(pady=5, fill="x", padx=40)
        
        ctk.CTkLabel(popup, text="Roll Number:").pack(pady=2)
        roll_entry = ctk.CTkEntry(popup)
        roll_entry.pack(pady=5, fill="x", padx=40)
        
        ctk.CTkLabel(popup, text="Department:").pack(pady=2)
        dept_entry = ctk.CTkEntry(popup)
        dept_entry.pack(pady=5, fill="x", padx=40)
        
        ctk.CTkLabel(popup, text="Email:").pack(pady=2)
        email_entry = ctk.CTkEntry(popup)
        email_entry.pack(pady=5, fill="x", padx=40)

        def submit():
            name = name_entry.get().strip()
            roll = roll_entry.get().strip()
            dept = dept_entry.get().strip()
            email = email_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Name is required.")
                return
            
            name_db = name.replace(" ", "_")
            # Register in DB with all fields
            database.add_student(name_db, email if email else None, roll if roll else None, dept if dept else None)
            
            # Folder creation
            user_dir = os.path.join("dataset", name_db)
            if not os.path.exists(user_dir): 
                os.makedirs(user_dir)
            
            popup.destroy()
            messagebox.showinfo("Info", f"Capturing faces for {name}. Look at the camera.")
            # Run capture script with name as argument
            os.system(f'"{sys.executable}" capture_faces.py --name {name_db}')
            self.refresh_students()
            self.refresh_stats()

        ctk.CTkButton(popup, text="Register & Capture Faces", command=submit, height=40, font=ctk.CTkFont(weight="bold")).pack(pady=30)

    def update_student_ui(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student from the list.")
            return
        
        old_name = self.student_tree.item(selected[0])['values'][0].replace(" ", "_")
        
        new_name = ctk.CTkInputDialog(text=f"Enter NEW name for {old_name.replace('_', ' ')}:", title="Update Student").get_input()
        
        if new_name:
            new_name_db = new_name.strip().replace(" ", "_")
            old_path = os.path.join("dataset", old_name)
            new_path = os.path.join("dataset", new_name_db)
            
            try:
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                database.update_student_name(old_name, new_name_db)
                messagebox.showinfo("Success", f"Updated {old_name} to {new_name_db}")
                self.run_encoding()
                self.refresh_students()
            except Exception as e:
                messagebox.showerror("Error", f"Update failed: {e}")

    def delete_student_ui(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student from the list.")
            return
        
        name = self.student_tree.item(selected[0])['values'][0].replace(" ", "_")
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete ALL data for {name}?"):
            try:
                path = os.path.join("dataset", name)
                if os.path.exists(path):
                    shutil.rmtree(path)
                database.delete_student(name)
                messagebox.showinfo("Success", f"Deleted {name}")
                self.run_encoding()
                self.refresh_students()
                self.refresh_stats()
            except Exception as e:
                messagebox.showerror("Error", f"Deletion failed: {e}")

    def run_encoding(self):
        messagebox.showinfo("Info", "Recalculating face embeddings... Please wait.")
        os.system(f'"{sys.executable}" encode_faces.py')
        messagebox.showinfo("Success", "Model updated successfully!")

    def check_camera(self):
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not detect camera.")
        else:
            messagebox.showinfo("Success", "Camera detected and working!")
            cap.release()

    def clear_logs(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear ALL logs?"):
            database.clear_all_logs()
            self.refresh_logs()
            self.refresh_stats()

    def export_report(self):
        logs = database.get_logs_by_date(None)
        if not logs:
            messagebox.showerror("Error", "No logs to export.")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_name = f"attendance_report_{timestamp}.csv"
        try:
            import csv
            with open(export_name, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Student Name', 'Date', 'Time', 'Session/Subject'])
                writer.writerows(logs)
            messagebox.showinfo("Success", f"CSV Report exported as {export_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")

    def export_pdf(self):
        logs = database.get_logs_by_date(None)
        if not logs:
            messagebox.showerror("Error", "No logs to export.")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_name = f"attendance_report_{timestamp}.pdf"
        try:
            pdf_utils.generate_attendance_pdf(logs, export_name)
            messagebox.showinfo("Success", f"PDF Report exported as {export_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
