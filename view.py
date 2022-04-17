from tkinter import *
from tkinter import ttk
#TODO askopenfilename - returns the path of selected file. you can use that path later to open file
from tkinter.filedialog import askopenfilename

import controller as con

root = Tk()
root.title('Moksliniu straipsniu kokybes vertinimo sistema')
root.geometry('500x200')
opened_pdf_file_location = ""


# opening file ONLY PDF, MOVE TO OTHER FILE
def open_file():
    global opened_pdf_file_location
    file = askopenfilename(
         title="Ikelti PDF", filetypes=(
            ('PDF failai', '*.pdf'),
        )
    )
    if file is not None:
        # define actions what to do when file is opened
        # content = file.read()

        opened_pdf_file_location= file
        print(opened_pdf_file_location)
        # pass


def get_data():
    global opened_pdf_file_location
    abstract = 0
    citations = citavimo_var.get()
    print(citations)
    citavimo_var.set("")
    #(opened_pdf_file_location)
    content, abstract = con.get_filtered_text(opened_pdf_file_location)
    #print(content)

    structure_score= con.structure_evaluation(content, abstract)
    print(structure_score)
    opened_pdf_file_location = ""


frm = ttk.Frame(root, padding=10)
frm.grid()

citavimo_var = StringVar()

ttk.Label(frm, text="Ikelkite mokslini straipsni").grid(column=0, row=0)
ttk.Button(frm, text="Pasirinkite faila", command=lambda: open_file()).grid(column=1, row=0)
ttk.Label(frm, text="Citavimo skaicius").grid(column=0, row=1)
citavimo_skaicius = ttk.Entry(frm, textvariable=citavimo_var).grid(column=1, row=1)

ttk.Button(frm, text="Apdoroti faila", command=lambda: get_data()).grid(column=1, row=2)

root.mainloop()
