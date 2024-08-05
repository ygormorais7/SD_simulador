from tkinter import *

class Menu:
    def __init__(self):
        self.root = Tk()
        self.tam(self.root, "Menu")
        self.second_wind = None

    def botoes_menu(self):
        Label(self.root, text="Nome da Aplicacao").place(relx=0.5, rely=0.1, anchor='n')
        self.app_name_entry = Entry(self.root)
        self.app_name_entry.place(relx=0.5, rely=0.15, anchor='n')

        Label(self.root, text="CPU").place(relx=0.5, rely=0.2, anchor='n')
        self.cpu_entry = Entry(self.root)
        self.cpu_entry.place(relx=0.5, rely=0.25, anchor='n')

        Label(self.root, text="RAM").place(relx=0.5, rely=0.3, anchor='n')
        self.ram_entry = Entry(self.root)
        self.ram_entry.place(relx=0.5, rely=0.35, anchor='n')

        Label(self.root, text="ROM").place(relx=0.5, rely=0.4, anchor='n')
        self.rom_entry = Entry(self.root)
        self.rom_entry.place(relx=0.5, rely=0.45, anchor='n')

        self.error_label = Label(self.root, text="", fg="red")
        self.error_label.place(relx=0.5, rely=0.55, anchor='n')

        Button(self.root, text="Iniciar", command=self.on_start).place(relx=0.5, rely=0.6, anchor='n')
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.root.mainloop()

    def on_start(self):
        app_name = self.app_name_entry.get()
        cpu = self.cpu_entry.get()
        ram = self.ram_entry.get()
        rom = self.rom_entry.get()

        if not app_name or not cpu or not ram or not rom:
            self.error_label.config(text="Error: Todos os campos devem ser preenchidos.")
            print("Error: Todos os campos devem ser preenchidos.")
        else:
            try:
                cpu = int(cpu)
                ram = int(ram)
                rom = int(rom)
            except ValueError:
                self.error_label.config(text="Erro: CPU, RAM e ROM devem ser números inteiros.")
                print("Error: CPU, RAM e ROM devem ser números inteiros.")
                return

            self.error_label.config(text="")
            print(f"Nome da Aplicacao: {app_name}")
            print(f"CPU: {cpu}")
            print(f"RAM: {ram}")
            print(f"ROM: {rom}")

            # Hide the root window
            self.root.withdraw()

            # Create a new window
            self.app_wind()

            # Show the root window again when the new window is closed
            self.second_wind.protocol("WM_DELETE_WINDOW", lambda: self.on_close(self.second_wind))
    
    def app_wind(self):
        self.second_wind = Toplevel(self.root)
        self.tam(self.second_wind, "")

        Label(self.second_wind, text="Bem-vindo ao Kubernetes!").pack(pady=20)
        Button(self.second_wind, text="Fechar", command=lambda: self.on_close(self.second_wind)).pack(pady=10)


    def on_close(self, window):
        self.root.deiconify()
        window.destroy()

    def tam(self, win, title, width=500, height=500):
        win.title(title)
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        sum_width = int(screen_width / 2 - width / 2)
        sum_height = int(screen_height / 2 - height / 2)
        win.geometry(f"{width}x{height}+{sum_width}+{sum_height}")

if __name__ == "__main__":
    menu = Menu()
    menu.botoes_menu()