import Page
import tkinter as tk


if __name__ == '__main__':
    root = tk.Tk()
    page = Page.Page(root)
    page.encryptTab()
    root.mainloop()