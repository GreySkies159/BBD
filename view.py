from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile

root = Tk()
root.title('Moksliniu straipsniu kokybes vertinimo sistema')


#opening file ONLY PDF, MOVE TO OTHER FILE
def open_file():
    file_path = askopenfile(
        mode='r', title="Ikelti PDF",  filetypes=(
            ('PDF failai', '*.pdf'),
            #('Visi failai', '*.*')
        )
    )
    if file_path is not None:
        pass


frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Ikelkite mokslini straipsni").grid(column=0, row=0)
ttk.Button(frm, text="Pasirinkite faila", command=lambda:open_file()).grid(column=1, row=0)
root.mainloop()
