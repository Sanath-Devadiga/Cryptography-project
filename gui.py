import tkinter as tk
from tkinter import ttk, messagebox
from group import Group
from member import Member
from colors import bcolors
from absl import app
import sys

def main(argv):
    # Add the current directory to Python path
    sys.path.append('.')
    root = tk.Tk()
    app = CryptographyGUI(root)
    root.mainloop()

class CryptographyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptography Project")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Set theme colors
        self.primary_color = '#2c3e50'
        self.secondary_color = '#3498db'
        self.accent_color = '#e74c3c'
        self.text_color = '#2c3e50'
        self.bg_color = '#f0f0f0'
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TButton', 
                           background=self.secondary_color,
                           foreground='white',
                           padding=10,
                           font=('Arial', 10))
        self.style.map('TButton',
                      background=[('active', self.primary_color)],
                      foreground=[('active', 'white')])
        
        # Initialize data structures
        self.groups = {}
        self.members = {}
        self.current_member = None
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create header frame
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create welcome label
        self.welcome_label = ttk.Label(self.header_frame, 
                                     text="Welcome to Cryptography Project",
                                     font=("Arial", 24, "bold"),
                                     foreground=self.primary_color)
        self.welcome_label.pack(pady=10)
        
        # Create subtitle
        self.subtitle_label = ttk.Label(self.header_frame,
                                      text="Secure Group Communication System",
                                      font=("Arial", 12),
                                      foreground=self.text_color)
        self.subtitle_label.pack()
        
        # Create buttons frame
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Create buttons for main actions with custom styling
        self.signup_btn = tk.Button(self.buttons_frame,
                                  text="Sign Up as New Member",
                                  command=self.signup,
                                  bg=self.secondary_color,
                                  fg='white',
                                  font=('Arial', 11),
                                  padx=20,
                                  pady=10,
                                  relief='flat',
                                  cursor='hand2')
        self.signup_btn.pack(side=tk.LEFT, padx=10)
        
        self.login_btn = tk.Button(self.buttons_frame,
                                 text="Log In as Existing Member",
                                 command=self.login,
                                 bg=self.primary_color,
                                 fg='white',
                                 font=('Arial', 11),
                                 padx=20,
                                 pady=10,
                                 relief='flat',
                                 cursor='hand2')
        self.login_btn.pack(side=tk.LEFT, padx=10)
        
        # Create status frame with custom styling
        self.status_frame = ttk.LabelFrame(self.main_frame,
                                         text="Current Status",
                                         padding="15")
        self.status_frame.grid(row=2, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        self.members_label = ttk.Label(self.status_frame,
                                     text="Members: []",
                                     font=('Arial', 11))
        self.members_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        
        self.groups_label = ttk.Label(self.status_frame,
                                    text="Groups: []",
                                    font=('Arial', 11))
        self.groups_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        
        # Create member actions frame with custom styling
        self.member_frame = ttk.LabelFrame(self.main_frame,
                                         text="Member Actions",
                                         padding="15")
        self.member_frame.grid(row=3, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        self.member_frame.grid_remove()
        
        # Create member action buttons with custom styling
        button_config = {
            'bg': self.secondary_color,
            'fg': 'white',
            'font': ('Arial', 10),
            'padx': 15,
            'pady': 8,
            'relief': 'flat',
            'cursor': 'hand2'
        }
        
        self.create_group_btn = tk.Button(self.member_frame,
                                        text="Create New Group",
                                        command=self.create_group,
                                        **button_config)
        self.create_group_btn.grid(row=0, column=0, padx=10, pady=5)
        
        self.add_member_btn = tk.Button(self.member_frame,
                                      text="Add Member to Group",
                                      command=self.add_member,
                                      **button_config)
        self.add_member_btn.grid(row=0, column=1, padx=10, pady=5)
        
        self.remove_member_btn = tk.Button(self.member_frame,
                                         text="Remove Member from Group",
                                         command=self.remove_member,
                                         **button_config)
        self.remove_member_btn.grid(row=1, column=0, padx=10, pady=5)
        
        self.send_message_btn = tk.Button(self.member_frame,
                                        text="Send Message",
                                        command=self.send_message,
                                        **button_config)
        self.send_message_btn.grid(row=1, column=1, padx=10, pady=5)
        
        self.read_messages_btn = tk.Button(self.member_frame,
                                         text="Read Messages",
                                         command=self.read_messages,
                                         **button_config)
        self.read_messages_btn.grid(row=2, column=0, padx=10, pady=5)
        
        self.logout_btn = tk.Button(self.member_frame,
                                  text="Logout",
                                  command=self.logout,
                                  bg=self.accent_color,
                                  fg='white',
                                  font=('Arial', 10),
                                  padx=15,
                                  pady=8,
                                  relief='flat',
                                  cursor='hand2')
        self.logout_btn.grid(row=2, column=1, padx=10, pady=5)
        
        # Create message display area with custom styling
        self.message_frame = ttk.LabelFrame(self.main_frame,
                                          text="Messages",
                                          padding="15")
        self.message_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        self.message_frame.grid_remove()
        
        self.message_text = tk.Text(self.message_frame,
                                  height=10,
                                  width=70,
                                  font=('Arial', 11),
                                  bg='white',
                                  fg=self.text_color,
                                  relief='flat',
                                  padx=10,
                                  pady=10)
        self.message_text.grid(row=0, column=0, padx=5, pady=5)
        
        # Add scrollbar to message text
        scrollbar = ttk.Scrollbar(self.message_frame, orient="vertical", command=self.message_text.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.message_text.configure(yscrollcommand=scrollbar.set)
        
        self.update_status()
    
    def update_status(self):
        """Update the status labels with current members and groups"""
        self.members_label.config(text=f"Members: {list(self.members.keys())}")
        if self.groups:
            groups_text = "Groups:\n"
            for group_id, group in self.groups.items():
                groups_text += f"Group {group_id}: {list(group.members.keys())}\n"
            self.groups_label.config(text=groups_text)
        else:
            self.groups_label.config(text="Groups: []")
    
    def signup(self):
        """Create a new member"""
        mem_id = len(self.members) + 1
        m = Member(id=mem_id)
        self.members[mem_id] = m
        messagebox.showinfo("Success", f"Member created with ID: {mem_id}")
        self.update_status()
    
    def login(self):
        """Login as an existing member"""
        if not self.members:
            messagebox.showerror("Error", "No members exist. Please sign up first.")
            return
        
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("400x200")
        login_window.configure(bg=self.bg_color)
        
        # Center the window
        login_window.update_idletasks()
        width = login_window.winfo_width()
        height = login_window.winfo_height()
        x = (login_window.winfo_screenwidth() // 2) - (width // 2)
        y = (login_window.winfo_screenheight() // 2) - (height // 2)
        login_window.geometry(f'{width}x{height}+{x}+{y}')
        
        ttk.Label(login_window,
                 text="Enter Member ID:",
                 font=('Arial', 11),
                 background=self.bg_color).pack(pady=10)
        
        member_id_entry = ttk.Entry(login_window, font=('Arial', 11))
        member_id_entry.pack(pady=5)
        
        def do_login():
            try:
                mem_id = int(member_id_entry.get())
                if mem_id in self.members:
                    self.current_member = self.members[mem_id]
                    self.member_frame.grid()
                    self.message_frame.grid()
                    login_window.destroy()
                else:
                    messagebox.showerror("Error", "Invalid member ID")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
        
        login_btn = tk.Button(login_window,
                            text="Login",
                            command=do_login,
                            bg=self.secondary_color,
                            fg='white',
                            font=('Arial', 11),
                            padx=20,
                            pady=5,
                            relief='flat',
                            cursor='hand2')
        login_btn.pack(pady=20)
    
    def create_group(self):
        """Create a new group"""
        if self.current_member.group_id is not None:
            messagebox.showerror("Error", "You are already part of a group!")
            return
        
        group_id = len(self.groups) + 1
        g = Group(id=group_id)
        g.add_member(self.current_member)
        self.groups[group_id] = g
        messagebox.showinfo("Success", f"Group {group_id} created successfully")
        self.update_status()
    
    def add_member(self):
        """Add a member to the current group"""
        if self.current_member.group_id is None:
            messagebox.showerror("Error", "You are not part of any group!")
            return
        
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Member")
        add_window.geometry("400x200")
        add_window.configure(bg=self.bg_color)
        
        # Center the window
        add_window.update_idletasks()
        width = add_window.winfo_width()
        height = add_window.winfo_height()
        x = (add_window.winfo_screenwidth() // 2) - (width // 2)
        y = (add_window.winfo_screenheight() // 2) - (height // 2)
        add_window.geometry(f'{width}x{height}+{x}+{y}')
        
        ttk.Label(add_window,
                 text="Select Member ID:",
                 font=('Arial', 11),
                 background=self.bg_color).pack(pady=10)
        
        member_id_entry = ttk.Entry(add_window, font=('Arial', 11))
        member_id_entry.pack(pady=5)
        
        def do_add():
            try:
                mem_id = int(member_id_entry.get())
                if mem_id in self.members:
                    mem = self.members[mem_id]
                    group = self.groups[self.current_member.group_id]
                    self.current_member.add_member_to_group(mem, group)
                    self.update_status()
                    add_window.destroy()
                else:
                    messagebox.showerror("Error", "Invalid member ID")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
        
        add_btn = tk.Button(add_window,
                          text="Add Member",
                          command=do_add,
                          bg=self.secondary_color,
                          fg='white',
                          font=('Arial', 11),
                          padx=20,
                          pady=5,
                          relief='flat',
                          cursor='hand2')
        add_btn.pack(pady=20)
    
    def remove_member(self):
        """Remove a member from the current group"""
        if self.current_member.group_id is None:
            messagebox.showerror("Error", "You are not part of any group!")
            return
        
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Member")
        remove_window.geometry("400x200")
        remove_window.configure(bg=self.bg_color)
        
        # Center the window
        remove_window.update_idletasks()
        width = remove_window.winfo_width()
        height = remove_window.winfo_height()
        x = (remove_window.winfo_screenwidth() // 2) - (width // 2)
        y = (remove_window.winfo_screenheight() // 2) - (height // 2)
        remove_window.geometry(f'{width}x{height}+{x}+{y}')
        
        ttk.Label(remove_window,
                 text="Select Member ID:",
                 font=('Arial', 11),
                 background=self.bg_color).pack(pady=10)
        
        member_id_entry = ttk.Entry(remove_window, font=('Arial', 11))
        member_id_entry.pack(pady=5)
        
        def do_remove():
            try:
                mem_id = int(member_id_entry.get())
                if mem_id in self.members:
                    mem = self.members[mem_id]
                    group = self.groups[self.current_member.group_id]
                    self.current_member.remove_member_from_group(mem, group)
                    self.update_status()
                    remove_window.destroy()
                else:
                    messagebox.showerror("Error", "Invalid member ID")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
        
        remove_btn = tk.Button(remove_window,
                             text="Remove Member",
                             command=do_remove,
                             bg=self.accent_color,
                             fg='white',
                             font=('Arial', 11),
                             padx=20,
                             pady=5,
                             relief='flat',
                             cursor='hand2')
        remove_btn.pack(pady=20)
    
    def send_message(self):
        """Send a message to a group"""
        if not self.groups:
            messagebox.showerror("Error", "No groups exist!")
            return
        
        send_window = tk.Toplevel(self.root)
        send_window.title("Send Message")
        send_window.geometry("500x300")
        send_window.configure(bg=self.bg_color)
        
        # Center the window
        send_window.update_idletasks()
        width = send_window.winfo_width()
        height = send_window.winfo_height()
        x = (send_window.winfo_screenwidth() // 2) - (width // 2)
        y = (send_window.winfo_screenheight() // 2) - (height // 2)
        send_window.geometry(f'{width}x{height}+{x}+{y}')
        
        ttk.Label(send_window,
                 text="Enter message:",
                 font=('Arial', 11),
                 background=self.bg_color).pack(pady=5)
        
        message_entry = ttk.Entry(send_window, width=40, font=('Arial', 11))
        message_entry.pack(pady=5)
        
        ttk.Label(send_window,
                 text="Select group ID:",
                 font=('Arial', 11),
                 background=self.bg_color).pack(pady=5)
        
        group_id_entry = ttk.Entry(send_window, font=('Arial', 11))
        group_id_entry.pack(pady=5)
        
        def do_send():
            try:
                message = message_entry.get()
                group_id = int(group_id_entry.get())
                
                if group_id in self.groups:
                    group = self.groups[group_id]
                    self.current_member.add_message_to_group(group, message)
                    
                    if group_id == self.current_member.group_id:
                        for mem in group.members.values():
                            mem.read_latest_message_of_group(group)
                    else:
                        for mem in group.members.values():
                            mem.read_latest_intergroup_message(group)
                    
                    messagebox.showinfo("Success", "Message sent successfully")
                    send_window.destroy()
                else:
                    messagebox.showerror("Error", "Invalid group ID")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values")
        
        send_btn = tk.Button(send_window,
                           text="Send Message",
                           command=do_send,
                           bg=self.secondary_color,
                           fg='white',
                           font=('Arial', 11),
                           padx=20,
                           pady=5,
                           relief='flat',
                           cursor='hand2')
        send_btn.pack(pady=20)
    
    def read_messages(self):
        """Display all messages for the current member"""
        self.message_text.delete(1.0, tk.END)
        if self.current_member.message_history:
            for message, sender in self.current_member.message_history:
                self.message_text.insert(tk.END, f'"{message}" - from {sender}\n')
        else:
            self.message_text.insert(tk.END, "No messages to display")
    
    def logout(self):
        """Logout the current member"""
        self.current_member = None
        self.member_frame.grid_remove()
        self.message_frame.grid_remove()
        self.update_status()

if __name__ == "__main__":
    app.run(main) 