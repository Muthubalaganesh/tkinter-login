import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import mysql.connector
from mysql.connector import Error

class LibraryLoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Stock Management - Login")
        
        # Window setup
        self.setup_window()
        
        # Floating books background
        self.setup_animated_background()
        
        # MySQL connection
        self.db_connection = self.connect_to_database()
        self.create_users_table()
        
        # GUI components
        self.setup_login_ui()

    def setup_window(self):
        """Configure main window size and position"""
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height/2 - window_height/2)
        position_right = int(screen_width/2 - window_width/2)
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    def setup_animated_background(self):
        """Create floating books animation"""
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        
        # Book images (color placeholders)
        self.book_images = []
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        for color in colors:
            img = Image.new('RGB', (40, 60), color)
            self.book_images.append(ImageTk.PhotoImage(img))
        
        # Create floating books
        self.floating_books = []
        for _ in range(15):
            book = {
                'id': self.canvas.create_image(
                    random.randint(50, 750),
                    random.randint(50, 550),
                    image=random.choice(self.book_images)
                ),
                'dx': random.choice([-2, -1, 1, 2]),
                'dy': random.choice([-2, -1, 1, 2])
            }
            self.floating_books.append(book)
        
        # Start animation
        self.animate_books()

    def animate_books(self):
        """Update book positions for animation"""
        for book in self.floating_books:
            x, y = self.canvas.coords(book['id'])
            if x <= 40 or x >= 760:
                book['dx'] *= -1
            if y <= 40 or y >= 560:
                book['dy'] *= -1
            self.canvas.move(book['id'], book['dx'], book['dy'])
        self.root.after(50, self.animate_books)

    def connect_to_database(self):
        """Establish MySQL connection with your credentials"""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Muthu@200630',  # Your password here
                database='library_db'
            )
            return connection
        except Error as e:
            error_msg = f"""
            MySQL Connection Failed: {e}

            Required Setup:
            1. Start MySQL server
            2. Create database:
               CREATE DATABASE library_db;
            3. Verify password: 'Muthu@200630'
            """
            messagebox.showerror("Database Error", error_msg)
            return None

    def create_users_table(self):
        """Initialize database table"""
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL
                    )
                """)
                self.db_connection.commit()
                
                # Add default admin if empty
                cursor.execute("SELECT COUNT(*) FROM users")
                if cursor.fetchone()[0] == 0:
                    cursor.execute(
                        "INSERT INTO users (username, password) VALUES (%s, %s)",
                        ("admin", "admin123")
                    )
                    self.db_connection.commit()
            except Error as e:
                messagebox.showerror("Database Error", f"Table creation failed: {e}")

    def setup_login_ui(self):
        """Create login interface"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg='white', bd=2, relief=tk.RIDGE)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        tk.Label(
            self.main_frame, 
            text="LIBRARY LOGIN", 
            font=('Helvetica', 18, 'bold'), 
            bg='white', fg='#333'
        ).pack(pady=(20, 10))
        
        # Login form
        self.create_login_form()
        
        # Registration button
        tk.Button(
            self.main_frame, 
            text="New User? Register Here", 
            command=self.show_registration_form,
            bg='white', fg='#45B7D1', font=('Helvetica', 10),
            bd=0, relief=tk.FLAT
        ).pack(pady=(0, 20))

    def create_login_form(self):
        """Login form widgets"""
        self.login_frame = tk.Frame(self.main_frame, bg='white')
        self.login_frame.pack(pady=20, padx=40)
        
        # Username
        tk.Label(
            self.login_frame, 
            text="Username:", 
            bg='white', font=('Helvetica', 12)
        ).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        
        self.username_entry = tk.Entry(self.login_frame, font=('Helvetica', 12))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Password
        tk.Label(
            self.login_frame, 
            text="Password:", 
            bg='white', font=('Helvetica', 12)
        ).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        
        self.password_entry = tk.Entry(
            self.login_frame, 
            show="*", 
            font=('Helvetica', 12)
        )
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Login button
        tk.Button(
            self.login_frame, 
            text="Login", 
            command=self.login,
            bg='#4ECDC4', fg='white', font=('Helvetica', 12),
            padx=20, pady=5, relief=tk.FLAT
        ).grid(row=2, column=0, columnspan=2, pady=15)
        
        self.registration_frame = None

    def login(self):
        """Authenticate user against database"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not self.db_connection:
            messagebox.showerror("Error", "Database connection failed")
            return
        
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            if cursor.fetchone():
                messagebox.showinfo("Success", "Login successful!")
                # Add your post-login logic here
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Error as e:
            messagebox.showerror("Database Error", f"Login failed: {e}")

    def show_registration_form(self):
        """Switch to registration form"""
        self.login_frame.pack_forget()
        
        if self.registration_frame is None:
            self.registration_frame = tk.Frame(self.main_frame, bg='white')
            
            # Registration widgets
            tk.Label(
                self.registration_frame, 
                text="New User Registration", 
                font=('Helvetica', 14, 'bold'), 
                bg='white'
            ).pack(pady=10)
            
            # Username field
            tk.Label(
                self.registration_frame, 
                text="Username:", 
                bg='white', font=('Helvetica', 12)
            ).pack()
            self.new_username = tk.Entry(
                self.registration_frame, 
                font=('Helvetica', 12)
            )
            self.new_username.pack()
            
            # Password field
            tk.Label(
                self.registration_frame, 
                text="Password:", 
                bg='white', font=('Helvetica', 12)
            ).pack()
            self.new_password = tk.Entry(
                self.registration_frame, 
                show="*", 
                font=('Helvetica', 12)
            )
            self.new_password.pack()
            
            # Confirm Password field
            tk.Label(
                self.registration_frame, 
                text="Confirm Password:", 
                bg='white', font=('Helvetica', 12)
            ).pack()
            self.confirm_password = tk.Entry(
                self.registration_frame, 
                show="*", 
                font=('Helvetica', 12)
            )
            self.confirm_password.pack()
            
            # Register button
            tk.Button(
                self.registration_frame, 
                text="Register", 
                command=self.register_user,
                bg='#4ECDC4', fg='white', font=('Helvetica', 12),
                padx=20, pady=5, relief=tk.FLAT
            ).pack(pady=15)
            
            # Back to login button
            tk.Button(
                self.registration_frame, 
                text="Back to Login", 
                command=self.show_login_form,
                bg='white', fg='#45B7D1', font=('Helvetica', 10),
                bd=0, relief=tk.FLAT
            ).pack()
        
        self.registration_frame.pack(pady=20, padx=40)

    def register_user(self):
        """Handle new user registration"""
        username = self.new_username.get()
        password = self.new_password.get()
        confirm_password = self.confirm_password.get()
        
        # Validation
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if not self.db_connection:
            messagebox.showerror("Error", "Database connection failed")
            return
        
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            self.db_connection.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.show_login_form()
        except Error as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Error", "Username already exists")
            else:
                messagebox.showerror("Database Error", f"Registration failed: {e}")

    def show_login_form(self):
        """Return to login form"""
        if self.registration_frame:
            self.registration_frame.pack_forget()
        self.login_frame.pack(pady=20, padx=40)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryLoginSystem(root)
    root.mainloop()
