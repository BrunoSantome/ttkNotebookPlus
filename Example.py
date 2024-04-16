import tkinter as tk
from tkinter import ttk
from NotebookPlus import ttkNotebookPlus

class Aplication(ttk.Frame):
    def __init__(self, main_window: tk.Tk):
        super().__init__(main_window)
        main_window.title('Notebook')
        self.Notebook = ttkNotebookPlus(master=main_window, wheelscroll=True)
        self.Notebook.pack(fill="both")
        self.pack()
        self.counter = 1
        menu = tk.Menu()
        menu.add_command(label="Add a tab", command=self.add_tab, accelerator="Ctrl+N")
        menu.add_command(label="Close all", command= self.Notebook.delete_all_windows)
        main_window.config(menu=menu)
        main_window.state("zoomed")
        main_window.minsize(400,200)

    def add_tab(self):
        frame = tk.Frame(master=self.Notebook)
        label = ttk.Label(master=frame, text=f"I am the window {self.counter}", font=('castellar', 20))
        label.pack()
        self.Notebook.add_window(frame_window=frame, name= f"WINDOW {self.counter}")
        self.counter +=1
        #self.try_functions()

    # def try_functions(self):
    #     tabs = self.Notebook.get_tabs()
    #     windows = self.Notebook.get_windows()
    #     print(windows)
    #     if len(tabs): 
    #         print(f'obtain the labels of the tabs {self.Notebook.get_tabs_names()}')

    #         print(f'obtain tab by index: {self.Notebook.get_tab(0)}')
    #         print(f'obtain tab by a specific window frame: {self.Notebook.get_tab(windows[0])}')
    #         print(f'obtain tab by the tab name: {self.Notebook.get_tab("WINDOW 1")}')

    #         print(f'obtain window by index: {self.Notebook.get_window(0)}')
    #         print(f'obtain window by a specific tab frame: {self.Notebook.get_window(tabs[0])}')
    #         print(f'obtain window by tab name: {self.Notebook.get_window("WINDOW 1")}')
    
if __name__ == "__main__":
    main_window = tk.Tk()
    App = Aplication(main_window)
    App.mainloop()
