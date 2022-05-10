import threading
import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import re


import api
import controller as con

opened_pdf_file_location = ''
is_thread_running  = 0

# declaration
root = Tk()
root.title('Mokslinių straipsnių kokybės vertinimo sistema')
root.geometry('560x360')

frm = ttk.Frame(root, padding=10)
frm.grid()

abstract_var = IntVar()
introduction_var = IntVar()
methods_var = IntVar()
conclusion_var = IntVar()
references_var = IntVar()
extra_structure_var = IntVar()
# references_length_var = StringVar()
citation_var = StringVar()
references_number_var = StringVar()
self_citation_var = IntVar()
selected_file_var = StringVar()

abstract_var.set(0)
introduction_var.set(0)
methods_var.set(0)
conclusion_var.set(0)
references_var.set(0)
extra_structure_var.set(0)
# references_length_var.set(0)
citation_var.set(0)
references_number_var.set(0)
self_citation_var.set(0)

selected_file_label = ttk.Label(frm, textvariable=selected_file_var)

file_label = ttk.Label(frm, text="Įkelkite mokslinį straipsnį")
file_button = ttk.Button(frm, text="Pasirinkite failą", command=lambda: change_file_selection_buttons_action())

analize_button = ttk.Button(frm, text="Nuskaityti failą", command=lambda: change_file_analize_button_acction())

autorius_label = ttk.Label(frm, text="Straipsnio autorius(-iai)")
autorius_laukelis = ttk.Entry(frm)

saves_citavimas_checkbox = ttk.Checkbutton(frm, text="Savęs citavimas", variable=self_citation_var)

struktura_label = ttk.Label(frm, text="Failo struktūros kriterijai. Ar yra: ")

abstract_label = ttk.Label(frm, text="Santrauka")
abstract_checkbox = ttk.Checkbutton(frm, text="Santrauka", variable=abstract_var)

introduction_label = ttk.Label(frm, text="Įvadas")
introduction_checkbox = ttk.Checkbutton(frm, text="Ivadas", variable=introduction_var, onvalue=1, offvalue=0)

methods_label = ttk.Label(frm, text="Metodai, dėstymas")
methods_checkbox = ttk.Checkbutton(frm, text="Metodai/dėstymas", variable=methods_var)

conclusion_label = ttk.Label(frm, text="Išvados")
conclusion_checkbox = ttk.Checkbutton(frm, text="Išvados", variable=conclusion_var)

references_label = ttk.Label(frm, text="Literatūros sąrašas")
references_checkbox = ttk.Checkbutton(frm, text="Literatūros sąrašas", variable=references_var)

extra_structure_label = ttk.Label(frm, text="Neprivaloma struktūra")
extra_structure_explanation = ttk.Label(frm, text="-padėka, diskusija, tolimesni žingsniai ir pan.")
extra_structure_checkbox = ttk.Checkbutton(frm, text="Neprivaloma struktūra", variable=extra_structure_var)

references_length_label = ttk.Label(frm, text="Literatūros sąrašo ilgis")
references_length_textbox = ttk.Entry(frm, textvariable=references_number_var)

citation_label = ttk.Label(frm, text="Citavimo skaicius")
citation_textbox = ttk.Entry(frm, textvariable=citation_var)

evaluation_button = ttk.Button(frm, text="Įvertinti failą", command=lambda: get_UI_data())

pb = ttk.Progressbar(frm, orient='horizontal', mode='indeterminate')
pb_text = ttk.Label(frm, text="Analizuojamas failas")

# creating grid
file_label.grid(row=0, column=0)
file_button.grid(row=0, column=1)



def open_file():
    global opened_pdf_file_location
    file = askopenfilename(
        title="Ikelti PDF", filetypes=(
            ('PDF failai', '*.pdf'),
        )
    )
    hide_selected_UI()
    # print(file)

    if file != '':
        # define actions what to do when file is opened
        # content = file.read()
        extention = file[-3:]
        if extention != 'pdf':
            tkinter.messagebox.showerror(title="Netinkamas failo tipas", message="Prašome pasirinkti tik pdf failus")
            opened_pdf_file_location = ''
            hide_analize_button()
            return

        opened_pdf_file_location = file
        print(opened_pdf_file_location)
        show_analize_button()
        show_selected_file()
    else:
        hide_analize_button()
        tkinter.messagebox.showerror(title="Failas nėra pasirinktas", message="Prašome pasirinkti failą")


def get_data_from_file():
    global opened_pdf_file_location
    abstract = 0
    global is_thread_running

    # (opened_pdf_file_location)
    print(opened_pdf_file_location)
    if opened_pdf_file_location != '':

        hide_selected_UI()
        #start progress
        show_progress_bar()
        pb.start()
        # threading
        getting_information_thread = threading.Thread(target=update_UI,
                                                      args=(pb, pb_text, opened_pdf_file_location), daemon=True)
        is_thread_running=1
        getting_information_thread.start()

        # content = con.get_filtered_text(opened_pdf_file_location)

        # structure_score= con.structure_evaluation(content, 1)
        # print(structure_score)
        #opened_pdf_file_location = ''
        # selected_file_UI()
    # print(content)
    else:
        hide_selected_UI()
        tkinter.messagebox.showerror(title="Failo pasirinkimas", message="Joks failas nebuvo pasirinktas")

def change_file_selection_buttons_action():
    global is_thread_running
    if is_thread_running == 1:
        tkinter.messagebox.showerror(title="Vyksta analizė", message="Kol failas yra analizuojamas, kito failo pasirinkti negalima")
    else:
        open_file()

def change_file_analize_button_acction():
    global is_thread_running
    if is_thread_running == 1:
        tkinter.messagebox.showerror(title="Vyksta analizė",
                                     message="Kol failas yra analizuojamas, kito failo analizuoti negalima")
    else:
        get_data_from_file()

def selected_file_UI():
    show_selected_file()
    autorius_label.grid(row=2, column=0)
    autorius_laukelis.grid(row=2, column=1)

    saves_citavimas_checkbox.grid(row=3, column=1, padx=20, sticky=EW)

    struktura_label.grid(row=4, column=0)
    abstract_checkbox.grid(row=5, column=0, sticky=W)
    introduction_checkbox.grid(row=6, column=0, sticky=W)
    methods_checkbox.grid(row=7, column=0, sticky=W)
    conclusion_checkbox.grid(row=8, column=0, sticky=W)
    references_checkbox.grid(row=9, column=0, sticky=W)
    extra_structure_checkbox.grid(row=10, column=0, sticky=W)
    extra_structure_explanation.grid(row=10, column=1, sticky=W)

    references_length_label.grid(row=11, column=0, pady=5, sticky=S)
    references_length_textbox.grid(row=11, column=1, pady=5, sticky=S)
    citation_label.grid(row=12, column=0, pady=5)
    citation_textbox.grid(row=12, column=1, pady=5)

    evaluation_button.grid(row=13, column=1)


def hide_selected_UI():
    selected_file_label.grid_forget()

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
    extra_structure_explanation.grid_forget()

    references_length_label.grid_forget()
    references_length_textbox.grid_forget()
    citation_label.grid_forget()
    citation_textbox.grid_forget()

    evaluation_button.grid_forget()


def show_selected_file():
    file_name_index = opened_pdf_file_location.rfind('/')
    file_name = opened_pdf_file_location[file_name_index + 1:]
    selected_file_var.set(file_name)
    selected_file_label.grid(row=1, column=0, columnspan=3, pady=10)


def show_analize_button():
    analize_button.grid(row=0, column=2, padx=20)


def hide_analize_button():
    selected_file_label.grid_forget()
    analize_button.grid_forget()


def show_progress_bar():

    pb_text.grid(row=1, column=1, sticky=EW, pady=(80, 0), columnspan=3)
    pb.grid(row=2, column=1, sticky=EW, pady=5, columnspan=3)


def update_UI(pb: ttk.Progressbar, pb_label: ttk.Label, opened_pdf_file_location):
    global is_thread_running
    global abstract_var, introduction_var, methods_var, \
        conclusion_var, references_var, extra_structure_var, references_number_var

    # get filtered text

    abstract, introduction, methods, conclusion, references, extra_structure, \
    max_reference_number = con.structure_evaluation(opened_pdf_file_location)
    # print(con.structure_evaluation(opened_pdf_file_location))
    print(abstract, introduction, methods, conclusion, references, extra_structure, max_reference_number)
    # start thread
    pb.grid_forget()
    pb_label.grid_forget()

    is_thread_running = 0
    # redeclare the checkboxes

    abstract_var.set(abstract)
    introduction_var.set(introduction)
    methods_var.set(methods)
    conclusion_var.set(conclusion)
    references_var.set(references)
    extra_structure_var.set(extra_structure)
    references_number_var.set(max_reference_number)

    #show file selection
    file_label.grid(row=0, column=0)
    file_button.grid(row=0, column=1)

    show_analize_button()
    selected_file_UI()


def get_UI_data():
    # TODO check if references number and citavimo var

    ref_is_all_numbers = re.search('\D', references_number_var.get())
    cit_is_all_numbers = re.search('\D', citation_var.get())
    if ref_is_all_numbers is not None:
        tkinter.messagebox.showerror(title="Literatūros sąrašo klaida",
                                     message="Literatūros sąrašo ilgis gali būti tik iš skaičių")
        return
    if cit_is_all_numbers is not None:
        tkinter.messagebox.showerror(title="Citavimo skaičiaus klaida",
                                     message="Citavimų skaičius gali būti tik skaitinė reikšmė")
        return

    structure_score = abstract_var.get() + introduction_var.get() + methods_var.get() + conclusion_var.get() + \
                      references_var.get()

    normalized_citations, normalized_structure, normalized_references = data_normalization(int(citation_var.get()),
                                                                                           int(structure_score),
                                                                                           int(references_number_var.get()))
    prediction_data = [normalized_citations, normalized_structure, int(extra_structure_var.get()),
                       int(self_citation_var.get()), normalized_references]

    data_dictionary = {
        'data': prediction_data
    }
    print(abstract_var.get(), introduction_var.get(), methods_var.get(), conclusion_var.get(), references_var.get(),
          extra_structure_var.get(), references_number_var.get())

    prediction_score = api.quality_value(data_dictionary)

    show_quality(prediction_score)



def data_normalization(cit, struct, refer):
    min_cit = 54
    max_cit = 6196
    min_struct = 1
    max_struct = 5
    min_ref = 0
    max_ref = 341
    if cit < min_cit:
        min_cit = cit
    if cit > max_cit:
        max_cit = cit
    if refer > max_ref:
        max_ref = refer
    normalized_cit = (cit - min_cit) / (max_cit - min_cit)
    normalized_struct = (struct - min_struct) / (max_struct - min_struct)
    normalized_refer = (refer - min_ref) / (max_ref - min_ref)
    return normalized_cit, normalized_struct, normalized_refer

def show_quality(quality_number):

    newWindow=Toplevel()
    newWindow.title(selected_file_var.get())
    newWindow.geometry("300x150")
    newWindow.grid()

    quality_var=StringVar()
    quality_var.set(quality_number)
    quality_Text_Label=ttk.Label(newWindow, text="Mokslinio straipsnio kokybė: ")
    text_Quality=ttk.Label(newWindow, text=quality_var.get())

    quality_Text_Label.grid(row=0, column=0, columnspan=3, sticky=EW, pady=(20, 5), padx=75)
    text_Quality.grid(row=1, column=0, columnspan=3, sticky=EW, padx=125)

root.mainloop()