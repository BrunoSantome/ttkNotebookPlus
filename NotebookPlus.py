# -*- coding: utf-8 -*-

# Copyright (c) Bruno Santome Antolín 2024
# For license see LICENSE

import tkinter as tk
from tkinter import ttk
import warnings

class Colors(str):
    GRAY = "#E4E4E4"
    GRAY_LIGHT = "#F0F0F0"
    BLACK = "#121212"
    WHITE = "#FFFFFF"
    BLUE = "#207DB0"
    RED = "#F5B7B1"


class _NotebookPlus(ttk.Frame):
    def __init__(
        self,
        master,
        wheelscroll=False,
        *args,
        **kwargs
    ) -> None:
        super().__init__(master=master)
        ttk.Frame.__init__(self=self, master=master)
        self.tabs_frame_list: list[tk.Frame] = []
        self.close_labels: list[tk.Label] = []
        self.names: list[str] = []
        self.windows: list[tk.Frame] = []
        self.tabs_labels_list: list[tk.Label] = []
        self.wheelscroll = wheelscroll
        self.state_scroll = True
        self._draw_tabs_canvas()

# #####################################Tab-Creation#############################################

    def _add_window(self, frame_window, name) -> None:
         self._init_tab(frame_window=frame_window, name=name)
         self._focus_tab(frame_window=frame_window)

    def _draw_tabs_canvas(self) -> None:
        self.tabs_canvas = tk.Canvas(master=self, highlightthickness=0, height=29)
        self.tabs_main_frame = tk.Frame(master=self.tabs_canvas)
        self.scroll_bar_widget = ttk.Scrollbar(master=self, orient='horizontal')
        self.tabs_canvas.config(xscrollcommand=self.scroll_bar_widget.set)
        self.scroll_bar_widget.pack(fill=tk.X, side="top",expand=1)
        self.tabs_canvas.pack(side="top", fill=tk.X, padx=3.5, pady=0.5)
        self.tabs_canvas.create_window((0, 0), window=self.tabs_main_frame, anchor="nw", tags="self.tabs_main_frame")

        self.scroll_bar_widget.bind("<B1-Motion>", lambda _: self._activate_scrollbar())
        self.tabs_main_frame.bind("<Configure>",lambda _: self._frame_conf())
        self.scroll_bar_widget.bind("<Configure>", lambda _: self._state_scrollbar())
        if self.wheelscroll:
            self.tabs_canvas.bind("<Enter>", lambda _: self._bound_wheel())
            self.scroll_bar_widget.bind("<Enter>", lambda _: self._bound_wheel())
            self.tabs_canvas.bind("<Leave>", lambda _: self._unbound_wheel())
            self.scroll_bar_widget.bind("<Leave>", lambda _: self._unbound_wheel())
     
    def _init_tab(self, name: str, frame_window, colour: str = Colors.WHITE) -> None:
        tab_f = tk.Frame(master=self.tabs_main_frame, bg=colour, highlightbackground="grey", highlightthickness=0.5)
        txt_label = tk.Label(master=tab_f, text=name, bg=colour)
        btn_close = ttk.Label(master=tab_f, text=u'\u274E', background=Colors.GRAY)
        tab_f.pack(side="left", padx=0.5, pady=5)
        btn_close.grid(row=0, column=2, sticky="ew")
        txt_label.grid(row=0, column=1, sticky="ew")
        self.tabs_frame_list.append(tab_f)
        self.windows.append(frame_window)
        self.tabs_labels_list.append(txt_label)
        self.names.append(name)
        self._tab_change(frame_window, tab_f, txt_label)
        self.after(ms=50, func=self._end_scroll)

        txt_label.bind("<Button-1>", lambda _: self._tab_change(frame_window, tab_f, txt_label))
        txt_label.bind("<Button-2>", lambda _: self._close_tab_window(tab_f, frame_window))
        txt_label.bind("<Button-3>", lambda event, tab_f=tab_f, frame_window=frame_window: self._menu_tab(tab_f, frame_window, event))
        btn_close.bind("<Enter>", lambda _: self._enter_close_label(btn_close))
        btn_close.bind("<Leave>", lambda _: self._leave_close_label(btn_close))
        btn_close.bind("<Button-1>", lambda _: self._close_tab_window(tab_f, frame_window))
        tab_f.bind("<Enter>", lambda _: self._hovering_tab(frame_window=tab_f, txt_label=txt_label))
        tab_f.bind("<Leave>", lambda _: self._unhovering_tab(frame_window=tab_f, txt_label=txt_label))

# #######################################Tab-Management#########################################
 
    def _frame_conf(self) -> None:
        self.tabs_canvas.configure(scrollregion=self.tabs_canvas.bbox("all"))

    def _tab_change(self, frame_window: tk.Frame, tab_f: tk.Frame, txt_label: tk.Label) -> None:
        for i, t in enumerate(self.tabs_labels_list):
            t.configure(bg=Colors.GRAY, fg=Colors.BLACK)
            self.tabs_frame_list[i].configure(bg=Colors.GRAY)
        self.current_tab_frame = frame_window
        self._state_scrollbar()
        tab_f.configure(bg=Colors.WHITE)
        txt_label.configure(bg=Colors.WHITE, fg=Colors.BLUE)
        self._focus_tab(frame_window)
    
    def _close_tab_window(self, tab_f: tk.Frame, window: tk.Frame) -> None:
        index = self.tabs_frame_list.index(tab_f)
        self.tabs_labels_list.pop(index)
        self.tabs_frame_list.pop(index).pack_forget()
        self.names.pop(index)
        self.update()
        self.windows.pop(self.windows.index(window)).pack_forget()
        if len(self.windows) != 0:
            self._tab_change(self.windows[-1], self.tabs_frame_list[-1], self.tabs_labels_list[-1])

    def _focus_tab(self, frame_window: tk.Frame) -> None:
        for window in self.windows:
            window.pack_forget()
        frame_window.configure(borderwidth=2, border=2)
        frame_window.pack(expand=True, fill=tk.BOTH, anchor="center", padx=5, pady=20)
        self.current_frame = frame_window

    def _hovering_tab(self, frame_window: tk.Frame, txt_label: tk.Label) -> None:
        self._state_scrollbar()
        if self.current_tab_frame != frame_window:
            if frame_window.cget("bg") == Colors.GRAY:
                txt_label.configure(bg=Colors.GRAY_LIGHT, fg=Colors.BLUE)
                frame_window.configure(bg=Colors.GRAY_LIGHT)

    def _unhovering_tab(self, frame_window: tk.Frame, txt_label: tk.Label) -> None:
        if frame_window.cget("bg") == Colors.GRAY_LIGHT:
            txt_label.configure(bg=Colors.GRAY, fg=Colors.BLACK)
            frame_window.configure(bg=Colors.GRAY)
    
    def _menu_tab(self, tab_f: tk.Frame, frame_window: tk.Frame, event) -> None:
        m = tk.Menu(tab_f, tearoff=False)
        m.add_command(label="Close", command=lambda: self._close_tab_window(tab_f=tab_f, window=frame_window))
        m.add_command(label="Close All", command=lambda: self._delete_tabs())
        m.add_separator()
        m.add_command(label="Rename tab", command=lambda: self._rename_tab(tab_f, "RENAMED"))
        m.tk_popup(event.x_root, event.y_root)

# #######################################Scrollbar############################################# 
    def _state_scrollbar(self) -> None:
        self.after(ms=50, func=self._check_scrollbar_state_delay)
 
    def _end_scroll(self) -> None:
        self.tabs_canvas.xview_moveto(1)
      
    def _check_scrollbar_state_delay(self) -> None:
        if len(self.scroll_bar_widget.state()) != 0:
            if self.scroll_bar_widget.state()[0] == "hover" and self.state_scroll == False:
                self.state_scroll = False
            else:
                self.state_scroll = True
        else:
            self.state_scroll = False
 
    def _activate_scrollbar(self) -> None:
        if len(self.windows) != 0 and not self.state_scroll:
            self.scroll_bar_widget.configure(command=self.tabs_canvas.xview)
        else:
            self.scroll_bar_widget.configure(command="")

    def _bound_wheel(self) -> None:
        if len(self.windows) != 0 and not self.state_scroll:
            self.scroll_bar_widget.bind_all("<MouseWheel>", self._on_mousewheel)
  
    def _unbound_wheel(self) -> None:
        self.scroll_bar_widget.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event) -> None:
        if self.state_scroll:
            self._unbound_wheel()
        elif not self.state_scroll:
            self.tabs_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

# #####################################Close-Label##############################################

    def _enter_close_label(self, btn) -> None:
        btn.configure(background=Colors.RED)

    def _leave_close_label(self, btn) -> None:
        btn.configure(background=Colors.GRAY)

# ##############################################################################################

    def _get_tab_frame(self, window) -> tk.Frame:
        return self.tabs_frame_list[self.tabs_frame_list.index(self.windows.index(window))]

    def _get_tab_label(self, tab) -> tk.Label:
        return self.tabs_labels_list[self.tabs_frame_list.index(tab)]

    def _get_tabs_names(self) -> list[str]: 
        return self.names

    def _get_labels_tabs(self) -> list[tk.Label]:
        return self.tabs_labels_list

    def _get_frames_tabs(self) -> list[tk.Frame]:
        return self.tabs_frame_list
    
    def _get_window(self, id: int | tk.Frame | str) -> tk.Frame:
        if isinstance(id, int):
            if id >= len(self.windows):
                warnings.warn("Warning: incorrect index")
            else:
                return self.windows[id]
        elif isinstance(id, tk.Frame):
            return self.windows[self.tabs_frame_list.index(id)]
        elif isinstance(id, str):                
            return self.windows[self.names.index(id)]

    def _get_all_windows(self) -> list[tk.Frame]:
        return self.windows

    def _get_tab(self, id: int | tk.Frame | str) -> tk.Frame:
        if  isinstance(id, int):
            if id >= len(self.tabs_frame_list):
                warnings.warn("Warning: incorrect index")
            else:
                return self.tabs_frame_list[id]
        elif isinstance(id, tk.Frame):
            return self.tabs_frame_list[self.windows.index(id)]
        elif isinstance(id, str):                
            return self.tabs_frame_list[self.names.index(id)]

    def _get_tabs(self) -> list[tk.Frame]:
        return self.tabs_frame_list

    def _rename_tab(self, tab, text) -> None:
        tab_label = self._get_tab_label(tab)
        tab_label.configure(text=text)

    def _delete_tabs(self) -> None:
        for tab in self.tabs_frame_list[::-1]:
            self._close_tab_window(tab, self.windows[self.tabs_frame_list.index(tab)])
  
    def _set_wheelscroll(self, value) -> None:
        self.wheelscroll = value


class ttkNotebookPlus(_NotebookPlus):

    '''
    The ttk Notebook widget organizes mltiple windows, showing one at a time.
    Each window is linked to a tab, allowing users to switch between them. 
    
    This improved version of a Notebook has the following improvements:
        - improved design
        - Tabs of notebook not resizable
        - Menu on tab when right-clicking, the posibility to add extra functions to it
        - Current tab-menu include: Close tab function, Close all tabs, Close others
        - Close tabs with middle-click on or by clicking the "close" button on each tab
        - Visible hover on tabs and on the closing button
        - Scrollbar to navigate through all tabs easly 
        - Posibility of using the mouse-wheel to scroll

    '''
    def __init__(self, master, wheelscroll, **kw):
        super().__init__(master=master, wheelscroll=wheelscroll)

    def add_window(self, frame_window: tk.Frame, name: str) -> None:
        '''Open a new window in the notebook'''
        self._add_window(frame_window, name)

    def delete_window(self, frame_window) -> None:
        '''Delete a window of the notebook'''
        tab_frame = self._get_tab_frame(frame_window)
        self._close_tab_window(tab_frame, frame_window)

    def delete_all_windows(self) -> None:
        '''Delete all windows managed by the notebook'''
        self._delete_tabs()

    def get_windows(self) -> list[tk.Frame]:
        '''Obtain all the windows managed by the notebook'''
        return self._get_all_windows()

    def get_window(self, index: int) -> tk.Frame:
        '''
        Obtain a specific window of the notebook with an identifier.
        The identifier can be one of the following posibilities: 
            -numerical index
            -string (name asigned to the tab)
            -tk.Frame (get the window by the tab asigned to it)
        '''
        return self._get_window(index)

    def get_tab(self, id: int | tk.Frame | str) -> tk.Frame:
        '''
        Obtain a specific tab of the notebook with an identifier.
        The identifier can be one of the following posibilities: 
            -numerical index
            -string (name asigned to the tab)
            -tk.Frame (look the tab by the window asign to it)
        '''
        return self._get_tab(id)

    def get_tabs(self) -> list[tk.Frame]:
        '''Obtain the list of tab frames'''
        return self._get_tabs()

    def get_tabs_names(self) -> list[str]:
        '''Obtain a list of names of all the tabs of the notebook'''
        return self._get_tabs_names()

    def rename_tab(self, tab: tk.Frame, text) -> None:
        '''Rename a specific tab given a tab and a text'''
        self._rename_tab(tab, text)
