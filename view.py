import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
#TODO askopenfilename - returns the path of selected file. you can use that path later to open file
from tkinter.filedialog import askopenfilename

import controller as con

root = Tk()
root.title('Moksliniu straipsniu kokybes vertinimo sistema')
root.geometry('500x350')
opened_pdf_file_location = ''


def open_file():
    global opened_pdf_file_location
    file = askopenfilename(
         title="Ikelti PDF", filetypes=(
            ('PDF failai', '*.pdf'),
        )
    )
    print(file)
    if file != '':
        # define actions what to do when file is opened
        # content = file.read()
        opened_pdf_file_location = file
        show_analize_button()

       # print(opened_pdf_file_location)
        # pass
    else:
        hide_analize_button()
        hide_selected_UI()
        tkinter.messagebox.showerror(title="Failo pasirinkimas", message="Prašome pasirinkti failą")


def get_data():
    global opened_pdf_file_location
    abstract = 0

    #(opened_pdf_file_location)
    print(opened_pdf_file_location)
    if opened_pdf_file_location != '':

        citations = citavimo_var.get()
        print(citations)
        citavimo_var.set("")

        selected_file_UI()
        content, abstract = con.get_filtered_text(opened_pdf_file_location)

        structure_score= con.structure_evaluation(content, abstract)
        print(structure_score)
        opened_pdf_file_location = ''
    #print(content)
    else:
        hide_selected_UI()
        tkinter.messagebox.showerror(title="Failo pasirinkimas", message="Joks failas nebuvo pasirinktas")


def selected_file_UI():
    print(":)")
    autorius_label.grid(row=1, column=0)
    autorius_laukelis.grid(row=1, column=1)

    saves_citavimas_checkbox.grid(row=2, column=1, padx=20, sticky=EW)

    struktura_label.grid(row=3, column=0)
    abstract_checkbox.grid(row=4, column=0, sticky=W)
    introduction_checkbox.grid(row=5, column=0, sticky=W)
    methods_checkbox.grid(row=6, column=0, sticky=W)
    conclusion_checkbox.grid(row=7, column=0, sticky=W)
    references_checkbox.grid(row=8, column=0, sticky=W)
    extra_structure_checkbox.grid(row=9, column=0, sticky=W)

    references_length_label.grid(row=10, column=0, pady=5, sticky=S)
    references_length_textbox.grid(row=10, column=1, pady=5, sticky=S)
    citation_label.grid(row=11, column=0, pady=5)
    citation_textbox.grid(row=11, column=1, pady=5)

    evaluation_button.grid(row=12, column=1)


def hide_selected_UI():
    print(":<")
    autorius_label.grid_forget()
    autorius_laukelis.grid_forget()

    saves_citavimas_checkbox.grid_forget()

    struktura_label.grid_forget()
    abstract_checkbox.grid_forget()
    introduction_checkbox.grid_forget()
    methods_checkbox.grid_forget()
    conclusion_checkbox.grid_forget()
    references_checkbox.grid_forget()
    extra_structure_checkbox.grid_forget()

    references_length_label.grid_forget()
    references_length_textbox.grid_forget()
    citation_label.grid_forget()
    citation_textbox.grid_forget()

    evaluation_button.grid_forget()

def show_analize_button():
    analize_button.grid(row=0, column=2, padx=20)

def hide_analize_button():
    analize_button.grid_forget()

frm = ttk.Frame(root, padding=10)
frm.grid()

abstract_var=StringVar()
introduction_var=StringVar()
methods_var=StringVar()
conclusion_var=StringVar()
references_var=StringVar()
extra_structure_var=StringVar()
references_length_var=StringVar()
citavimo_var = StringVar()
self_citation_var=StringVar()



file_label=ttk.Label(frm, text="Ikelkite mokslini straipsni")
file_button=ttk.Button(frm, text="Pasirinkite faila", command=lambda: open_file())

analize_button=ttk.Button(frm, text="Nuskaityti faila", command=lambda: get_data())


autorius_label=ttk.Label(frm, text="Straipsnio autorius(-iai)")
autorius_laukelis= ttk.Entry(frm)

saves_citavimas_checkbox=ttk.Checkbutton(frm, text="Savęs citavimas", variable=self_citation_var)

struktura_label=ttk.Label(frm, text="Failo struktūros kriterijai. Ar yra: ")

abstract_label=ttk.Label(frm, text="Abstraktas")
abstract_checkbox= ttk.Checkbutton(frm, text="Abstraktas", variable=abstract_var)

introduction_label=ttk.Label(frm, text="Įvadas")
introduction_checkbox= ttk.Checkbutton(frm, text="Ivadas", variable=introduction_var)

methods_label=ttk.Label(frm, text="Metodai, dėstymas")
methods_checkbox= ttk.Checkbutton(frm, text="Metodai/dėstymas", variable=methods_var)

conclusion_label=ttk.Label(frm, text="Išvados")
conclusion_checkbox= ttk.Checkbutton(frm, text="Išvados", variable=conclusion_var)

references_label=ttk.Label(frm, text="Literatūros sąrašas")
references_checkbox= ttk.Checkbutton(frm, text="Literatūros sąrašas", variable=references_var)

extra_structure_label=ttk.Label(frm, text="Neprivaloma struktūra")
extra_structure_explanation=ttk.Label(frm, text="Padėka, diskusija, tolimesni žingsniai")
extra_structure_checkbox= ttk.Checkbutton(frm, text="Neprivaloma struktūra", variable=extra_structure_var)

references_length_label=ttk.Label(frm, text="Literatūros sąrašo ilgis")
references_length_textbox= ttk.Entry(frm)

citation_label=ttk.Label(frm, text="Citavimo skaicius")
citation_textbox = ttk.Entry(frm, textvariable=citavimo_var)

evaluation_button=ttk.Button(frm, text="Įvertinti failą")

#creating grid
file_label.grid(row=0, column=0)
file_button.grid(row=0, column=1)



root.mainloop()
