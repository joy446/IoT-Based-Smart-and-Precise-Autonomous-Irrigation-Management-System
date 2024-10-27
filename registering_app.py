import tkinter as tk
from tkinter import messagebox
import pandas as pd

def createexcel():
    crop = cropentry.get()
    try:
        area = float(areaentry.get())
        motorcap = float(motorcapentry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for field area and motor capacity")
        return

    data = {
        "Crop Name": [crop],
        "Field Area (acres)": [area],
        "Motor Pump Capacity (L/min)": [motorcap]
    }

    df = pd.DataFrame(data)
    filename = "myfield.xlsx"

    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Field Data', startrow=1, index=False)
        wb = writer.book
        ws = writer.sheets['Field Data']

        headerfmt = wb.add_format({
            'bold': True,
            'font_size': 14,
            'valign': 'center',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        ws.merge_range('A1:D1', "Field Data", headerfmt)

    messagebox.showinfo("Success", f"Excel sheet created: {filename}")

root = tk.Tk()
root.title("Field Data Application")
root.geometry("600x600")
root.configure(bg="#E0E0E0")

mainframe = tk.Frame(root, bg="#E0E0E0", bd=5, relief=tk.GROOVE)
mainframe.pack(pady=20, padx=10)

headfont = ("Helvetica", 36)
labelfont = ("Helvetica", 18)
btnfont = ("Helvetica", 18)

heading = tk.Label(mainframe, text="Field Data Entry", font=headfont, fg="#4B0082", bg="#E0E0E0")
heading.pack(pady=10)

def createbtn(txt, cmd):
    btnframe = tk.Frame(mainframe, bg="#E0E0E0")
    btnframe.pack(pady=10)

    btn = tk.Button(
        btnframe,
        text=txt,
        command=cmd,
        font=btnfont,
        bg="#4CAF50",
        fg="white",
        relief=tk.RAISED,
        bd=5,
        activebackground="#45A049",
        activeforeground="white"
    )
    btn.pack(padx=5, pady=5)
    return btn

croplabel = tk.Label(mainframe, text="Crop Name:", font=labelfont, bg="#E0E0E0")
croplabel.pack(pady=5)
cropentry = tk.Entry(mainframe, width=30, font=labelfont)
cropentry.pack(pady=5)

arealabel = tk.Label(mainframe, text="Field Area (acres):", font=labelfont, bg="#E0E0E0")
arealabel.pack(pady=5)
areaentry = tk.Entry(mainframe, width=30, font=labelfont)
areaentry.pack(pady=5)

motorcaplabel = tk.Label(mainframe, text="Motor Pump Capacity (L/min):", font=labelfont, bg="#E0E0E0")
motorcaplabel.pack(pady=5)
motorcapentry = tk.Entry(mainframe, width=30, font=labelfont)
motorcapentry.pack(pady=5)

submitbtn = createbtn("Create Excel", createexcel)

root.mainloop()
