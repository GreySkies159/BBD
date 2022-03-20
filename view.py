from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile

root = Tk()
root.title('Moksliniu straipsniu kokybes vertinimo sistema')
root.geometry('500x200')


# opening file ONLY PDF, MOVE TO OTHER FILE
def open_file():
    file = askopenfile(
        mode='r', title="Ikelti PDF", filetypes=(
            ('PDF failai', '*.pdf'),
        )
    )
    if file is not None:
        # define actions what to do when file is opened
        content = file.read()

        # pass


def get_data():
    citations = citavimo_var.get()
    print(citations)
    citavimo_var.set("")


frm = ttk.Frame(root, padding=10)
frm.grid()

citavimo_var = StringVar()

ttk.Label(frm, text="Ikelkite mokslini straipsni").grid(column=0, row=0)
ttk.Button(frm, text="Pasirinkite faila", command=lambda: open_file()).grid(column=1, row=0)
ttk.Label(frm, text="Citavimo skaicius").grid(column=0, row=1)
citavimo_skaicius = ttk.Entry(frm, textvariable=citavimo_var).grid(column=1, row=1)

ttk.Button(frm, text="Apdoroti faila", command=lambda: get_data()).grid(column=1, row=2)

root.mainloop()
