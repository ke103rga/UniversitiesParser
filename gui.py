import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk
import pandastable
import susu_parser
import urfu_parser
import pandas as pd


class TestApp(tk.Frame):
    """Basic test frame for the table"""
    def __init__(self, data, parent=None):
        self.parent = parent
        tk.Frame.__init__(self)
        self.main = self.master
        self.main.geometry('800x400+200+100')
        self.main.title('Рейтинг абитурьента')
        f = tk.Frame(self.main)
        f.pack(fill=tk.BOTH,expand=1)
        df = data
        self.table = pt = pandastable.Table(f, dataframe=df,
                                           showtoolbar=True, showstatusbar=True)
        pt.show()
        return


def show_table(window):
    entrant_info = []
    entrant_info.extend(susu_parser.parser())
    entrant_info.extend(urfu_parser.parser())

    ratings = pd.DataFrame(entrant_info)
    ratings.rename(columns={"univercity": "Университет",
                            "speciality": "Направление",
                            "rate": "Рейтинг",
                            "agreement_rate": "Рейтинг среди давших согласие",
                            "plan": "План набора"}, inplace=True)

    window.destroy()
    app = TestApp(ratings)
    app.mainloop()


def show_result():
    window = tk.Tk()
    window.title("Рейтинг поступающего в разных университетах")
    window.geometry('850x400')
    window.resizable(width=0, height=0)

    instruction = "После нажатия на кнопку 'Обновиить рейтинг'\n" \
                  "перед вами появится таблица,\n" \
                  "содержащая информацию о рейтинге поступающего в разных университетах\n" \
                  "*Рейтинг - позиция абитурьента в всех списке людей, подавших документы;\n" \
                  "*Рейтинг среди давших согласие - позиция абитурьента в том же списке,\n" \
                  "но только среди людей подавших согласие(более актуальная информация);\n" \
                  "*План набора - Количество людей, набираемых в этом году по данному направлению."

    lbl = tk.Label(window, text=instruction, font=('Times', 15))
    lbl.place(x=70, y=50)

    btn = tk.Button(window, text="Обновить рейтинг",
                 height=5, width=20,
                 bg="Gray", fg='White', command=lambda: show_table(window))
    btn.place(x=340, y=250)

    window.mainloop()






