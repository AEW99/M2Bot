from customtkinter import *
from PIL import Image

app = CTk()
app.geometry("300x200")
app.title("M2Bot")
app.resizable(False, False)

background_img_date = Image.open("background-img.png")
background_img = CTkImage(dark_image=background_img_date, light_image=background_img_date, size=(300, 200))

background_label = CTkLabel(master=app, image=background_img, text="")
background_label.place(x=0, y=0, relwidth=1, relheight=1)

frame = CTkFrame(app, height=130)
frame.pack_propagate(False)
frame.place(anchor="w", y=100, x=50)

bot_switch_var = IntVar()
captcha_switch_var = IntVar()
debug_switch_var = IntVar(value=0)
bot_switch = CTkSwitch(frame, text="Farmbot", variable=bot_switch_var, onvalue=1, offvalue=0, command=bot_switch_var.set(0))
captcha_switch = CTkSwitch(frame, text="Solve Captcha", variable=captcha_switch_var, onvalue=1, offvalue=0)  # future feature, nearly done
debug_switch = CTkSwitch(frame, text="Captcha Debugger", variable=debug_switch_var, onvalue=1, offvalue=0)
bot_switch.pack(anchor="w", padx=10)
captcha_switch.pack(anchor="w", padx=10)
debug_switch.pack(anchor="w", padx=10)

y = 0
label1 = CTkLabel(master=frame, text=f"Metins killed: {y}")
label1.pack(anchor="w", padx=10)
button1 = CTkButton(master=frame, text="Configure")
button1.pack(pady=5)

version = "Beta 0.5"
label2 = CTkLabel(master=app, height=10, text=f"v. {version}", font=("font", 12))
label2.pack(side="bottom", anchor="e", padx=2)


def open_debugger():
    debug = CTkToplevel()
    label_sc = CTkLabel(master=debug, text="")
    label_sc.pack()

    return debug, label_sc