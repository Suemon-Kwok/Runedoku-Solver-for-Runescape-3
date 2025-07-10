import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class RunedokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Runedoku Solver")
        self.root.geometry("700x800")
        self.root.configure(bg='#f0f4f8')
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Rune mappings
        self.rune_to_num = {
            'Air': 1, 'Water': 2, 'Earth': 3, 'Fire': 4, 'Mind': 5,
            'Body': 6, 'Death': 7, 'Chaos': 8, 'Law': 9, 'Nature': 9
        }
        
        self.num_to_rune = {
            1: 'Air', 2: 'Water', 3: 'Earth', 4: 'Fire', 5: 'Mind',
            6: 'Body', 7: 'Death', 8: 'Chaos', 9: 'Law'
        }
        
        # Grid data
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.original_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.selected_rune = None
        self.grid_buttons = []
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#f0f4f8')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, text="🧩 Runedoku Solver", 
                              font=('Arial', 24, 'bold'), 
                              bg='#f0f4f8', fg='#2d3748')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Click buttons to enter runes, then solve your 9x9 Runedoku puzzle!", 
                                 font=('Arial', 12), 
                                 bg='#f0f4f8', fg='#4a5568')
        subtitle_label.pack(pady=5)
        
        # Instructions
        instructions_frame = tk.Frame(self.root, bg='#e2e8f0', relief='raised', bd=2)
        instructions_frame.pack(pady=5, padx=20, fill='x')
        
        instructions_label = tk.Label(instructions_frame, 
                                    text="How to use: 1. Select a rune → 2. Click grid squares → 3. Click 'Solve Puzzle' → 4. Green = solution!",
                                    font=('Arial', 9), 
                                    bg='#e2e8f0', fg='#2d3748',
                                    justify='center')
        instructions_label.pack(pady=5, padx=10)
        
        # Control buttons (moved above rune selection)
        control_frame = tk.Frame(self.root, bg='#f0f4f8')
        control_frame.pack(pady=10)
        
        self.solve_btn = tk.Button(control_frame, text="🔍 Solve Puzzle", 
                                  font=('Arial', 12, 'bold'),
                                  width=15, height=2,
                                  bg='#48bb78', fg='white',
                                  activebackground='#38a169',
                                  relief='raised', bd=3,
                                  command=self.solve_puzzle)
        self.solve_btn.pack(side='left', padx=10)
        
        self.clear_btn = tk.Button(control_frame, text="🗑️ Clear Grid", 
                                  font=('Arial', 12, 'bold'),
                                  width=15, height=2,
                                  bg='#f56565', fg='white',
                                  activebackground='#e53e3e',
                                  relief='raised', bd=3,
                                  command=self.clear_grid)
        self.clear_btn.pack(side='left', padx=10)
        
        # Rune selector
        rune_frame = tk.Frame(self.root, bg='#f0f4f8')
        rune_frame.pack(pady=5)
        
        rune_label = tk.Label(rune_frame, text="Select Rune:", 
                             font=('Arial', 12, 'bold'), 
                             bg='#f0f4f8', fg='#2d3748')
        rune_label.pack(pady=3)
        
        self.rune_buttons = {}
        rune_button_frame = tk.Frame(rune_frame, bg='#f0f4f8')
        rune_button_frame.pack()
        
        runes = ['Air', 'Water', 'Earth', 'Fire', 'Mind', 'Body', 'Death', 'Chaos', 'Law', 'Empty']
        for i, rune in enumerate(runes):
            row = i // 5
            col = i % 5
            
            btn = tk.Button(rune_button_frame, text=rune, 
                           font=('Arial', 9, 'bold'),
                           width=7, height=1,
                           bg='#e2e8f0', fg='#2d3748',
                           activebackground='#cbd5e0',
                           relief='raised', bd=2,
                           command=lambda r=rune: self.select_rune(r))
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.rune_buttons[rune] = btn
        
        # Grid
        grid_frame = tk.Frame(self.root, bg='#2d3748', relief='raised', bd=5)
        grid_frame.pack(pady=15)
        
        self.create_grid(grid_frame)
        
        # Status
        self.status_label = tk.Label(self.root, text="Welcome! Select a rune and click on grid squares to start.", 
                                    font=('Arial', 11, 'bold'), 
                                    bg='#bee3f8', fg='#2a4365',
                                    relief='raised', bd=2)
        self.status_label.pack(pady=10, padx=20, fill='x')
        
    def create_grid(self, parent):
        """Create the 9x9 grid of buttons"""
        self.grid_buttons = []
        
        for row in range(9):
            button_row = []
            for col in range(9):
                # Calculate padding for proper 3x3 box separation
                padx = (8 if col in [3, 6] else 2, 2)
                pady = (8 if row in [3, 6] else 2, 2)
                
                btn = tk.Button(parent, text="", 
                               font=('Arial', 9, 'bold'),
                               width=5, height=2,
                               bg='#f7fafc', fg='#2d3748',
                               activebackground='#e2e8f0',
                               relief='raised', bd=2,
                               command=lambda r=row, c=col: self.place_rune(r, c))
                btn.grid(row=row, column=col, padx=padx, pady=pady)
                button_row.append(btn)
                
            self.grid_buttons.append(button_row)
    
    def select_rune(self, rune):
        """Select a rune for placing"""
        self.selected_rune = rune
        
        # Update button appearances
        for r, btn in self.rune_buttons.items():
            if r == rune:
                btn.configure(bg='#667eea', fg='white')
            else:
                btn.configure(bg='#e2e8f0', fg='#2d3748')
        
        self.update_status(f"Selected: {rune}", "info")
    
    def place_rune(self, row, col):
        """Place selected rune on grid"""
        if not self.selected_rune:
            messagebox.showwarning("No Rune Selected", "Please select a rune first!")
            return
        
        button = self.grid_buttons[row][col]
        
        if self.selected_rune == 'Empty':
            self.grid[row][col] = 0
            self.original_grid[row][col] = 0
            button.configure(text="", bg='#f7fafc', fg='#2d3748')
        else:
            self.grid[row][col] = self.rune_to_num[self.selected_rune]
            self.original_grid[row][col] = self.rune_to_num[self.selected_rune]
            button.configure(text=self.selected_rune, bg='#667eea', fg='white')
    
    def is_valid(self, row, col, num):
        """Check if placing num at position (row, col) is valid"""
        # Check row
        for c in range(9):
            if self.grid[row][c] == num:
                return False
        
        # Check column
        for r in range(9):
            if self.grid[r][col] == num:
                return False
        
        # Check 3x3 box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.grid[r][c] == num:
                    return False
        
        return True
    
    def solve(self):
        """Solve the puzzle using backtracking"""
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            self.grid[row][col] = num
                            if self.solve():
                                return True
                            self.grid[row][col] = 0
                    return False
        return True
    
    def solve_puzzle(self):
        """Solve the puzzle and update display"""
        # Check if puzzle has input
        has_input = False
        for row in range(9):
            for col in range(9):
                if self.original_grid[row][col] != 0:
                    has_input = True
                    break
            if has_input:
                break
        
        if not has_input:
            messagebox.showwarning("No Input", "Please enter some runes first!")
            return
        
        # Disable buttons during solving
        self.solve_btn.configure(state='disabled')
        self.clear_btn.configure(state='disabled')
        self.update_status("Solving puzzle...", "info")
        
        # Copy original grid to working grid
        for row in range(9):
            for col in range(9):
                self.grid[row][col] = self.original_grid[row][col]
        
        # Solve in separate thread to prevent GUI freezing
        def solve_thread():
            time.sleep(0.1)  # Small delay for visual feedback
            
            if self.solve():
                self.root.after(0, self.display_solution)
                self.root.after(0, lambda: self.update_status("🎉 Puzzle solved successfully!", "success"))
            else:
                self.root.after(0, lambda: self.update_status("❌ No solution exists for this puzzle. Check your input!", "error"))
            
            # Re-enable buttons
            self.root.after(0, lambda: self.solve_btn.configure(state='normal'))
            self.root.after(0, lambda: self.clear_btn.configure(state='normal'))
        
        thread = threading.Thread(target=solve_thread)
        thread.daemon = True
        thread.start()
    
    def display_solution(self):
        """Display the solved puzzle"""
        for row in range(9):
            for col in range(9):
                button = self.grid_buttons[row][col]
                rune = self.num_to_rune[self.grid[row][col]]
                
                button.configure(text=rune)
                
                if self.original_grid[row][col] == 0:
                    # Solved squares - green
                    button.configure(bg='#48bb78', fg='white')
                else:
                    # Original input - blue
                    button.configure(bg='#667eea', fg='white')
    
    def clear_grid(self):
        """Clear the entire grid"""
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.original_grid = [[0 for _ in range(9)] for _ in range(9)]
        
        for row in range(9):
            for col in range(9):
                button = self.grid_buttons[row][col]
                button.configure(text="", bg='#f7fafc', fg='#2d3748')
        
        self.update_status("Grid cleared!", "info")
    
    def update_status(self, message, status_type):
        """Update status message"""
        colors = {
            "info": ("#bee3f8", "#2a4365"),
            "success": ("#c6f6d5", "#22543d"),
            "error": ("#fed7d7", "#742a2a")
        }
        
        bg, fg = colors.get(status_type, colors["info"])
        self.status_label.configure(text=message, bg=bg, fg=fg)
        
        # Auto-clear info messages after 3 seconds
        if status_type == "info":
            self.root.after(3000, lambda: self.status_label.configure(text=""))

def main():
    root = tk.Tk()
    app = RunedokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()