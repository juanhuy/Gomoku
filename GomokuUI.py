import tkinter as tk
from tkinter import ttk, messagebox
from gomoku import Gomoku, GomokuBot, GomokuPos, BOARD_SIZE
from PIL import Image, ImageTk 


class GomokuGUI(tk.Toplevel):
    def __init__(self, parent, who_go_first='BOT'):
        super().__init__(parent)
        self.title("Welcome To Gomoku")
        self.geometry("700x700")

        self.game = Gomoku()
        self.bot = GomokuBot(self.game)
        self.who_go_first = who_go_first
        self.last_possition = GomokuPos()

        self.create_widgets()
        self.place_widgets()

        if self.who_go_first == "BOT":
            self.bot_move()
        else:
            self.bot.name = 'O'

    def create_widgets(self):
        self.fra_blanks = ttk.Frame(self)
        self.labels = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.labels[i][j] = tk.Label(self.fra_blanks, width=2, height=1, text='', relief=tk.RAISED, bg='white', font=("Helvetica", 16))
                self.labels[i][j].grid(row=i, column=j, sticky='nsew')
                self.labels[i][j].bind('<Button-1>', lambda e, row=i, col=j: self.make_move(row, col))

        self.status_label = ttk.Label(self, text="", font=("Helvetica", 16))
        
    def place_widgets(self):
        self.fra_blanks.grid(row=0, column=0)
        self.status_label.grid(row=BOARD_SIZE, columnspan=10)

    def bot_move(self):
        self.status_label.config(text="Bot is thinking... be patient...")
        self.update()
        print("Bot is thinking...")
        self.bot.take_turn_alpha_beta()
        print("Bot done thinking.")
        self.status_label.config(text="Bot done thinking.")
        self.game.move(self.bot.choice)
        self.update_board(self.bot.choice)
        self.update()

    def human_move(self, row, col):
        self.game.move(GomokuPos(row, col))
        self.update_board(GomokuPos(row, col))
        self.update()

    def make_move(self, row, col):
        self.human_move(row, col)
        if self.game.over():
            self.show_result()
        else:
            self.bot_move()
            if self.game.over():
                self.show_result()

    def update_board(self, pos=None):
        if pos is not None:
            x = pos.x
            y = pos.y
            self.labels[x][y]['text'] = self.game.board[x][y]
            color = ''
            move_name = self.game.board[x][y]
            if move_name == 'X':
                color = 'blue'
            else:
                color = 'red'
            self.labels[x][y].config(text=move_name, fg=color, bg='yellow')
            self.labels[self.last_possition.x][self.last_possition.y].config(bg='white')
            self.last_possition = GomokuPos(x, y)
        else:
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    self.labels[i][j]['text'] = ''

    def show_result(self):
        result = self.game.win()
        if result == 'T':
            messagebox.showinfo("Game Over", "It's a tie!")
        else:
            winner = "Player X" if result == 'X' else "Player O"
            messagebox.showinfo("Game Over", f"{winner} wins!")

        self.game = Gomoku()
        self.bot = GomokuBot(self.game)
        self.update_board()
        self.update()
        if self.who_go_first == "BOT":
            self.bot_move()
        else:
            self.bot.name = 'O'



class GomokuSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gomoku Welcome")
        self.geometry("750x500")

       
        original_image = Image.open("background.jpg")  
        resized_image = original_image.resize((750, 500))
        self.bg_image = ImageTk.PhotoImage(resized_image)

        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_widgets()
        self.place_widgets()
        self.associate_events()
        self.protocol("WM_DELETE_WINDOW", self.on_close)


    def create_widgets(self):
        
        self.fra_user_options = tk.Frame(self, bg="#ffffff", bd=2, relief="ridge")

        self.lbl_who_go_first = ttk.Label(self.fra_user_options, text="Who go first:")
        self.cb_who_go_first = ttk.Combobox(self.fra_user_options, values=('YOU', 'BOT'), state='readonly')
        self.cb_who_go_first.set('BOT')
        self.btn_play = ttk.Button(self.fra_user_options, text="Play")

    def place_widgets(self):
       
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.fra_user_options.grid(row=1, column=0, padx=20, pady=20)

        self.lbl_who_go_first.grid(row=0, column=0, pady=(0, 10))
        self.cb_who_go_first.grid(row=1, column=0, pady=(0, 10))
        self.btn_play.grid(row=2, column=0)

    def associate_events(self):
        self.btn_play.bind("<Button-1>", lambda e: self.btn_play_Button_1())

    def btn_play_Button_1(self):
        gomoku_gui = GomokuGUI(self, self.cb_who_go_first.get())
        gomoku_gui.grab_set()         
        gomoku_gui.focus_force()      
        gomoku_gui.lift()           
        gomoku_gui.attributes('-topmost', True)  
        gomoku_gui.after(100, lambda: gomoku_gui.attributes('-topmost', False)) 
        self.withdraw()              
    def on_close(self):
        self.destroy()
        self.master.destroy() 


if __name__ == "__main__":
    app = GomokuSelector()
    app.mainloop()

