import cv2
import numpy as np
import pyautogui
import gui
from PIL import Image, ImageTk

# TO DO LIST
#
# add commands to both switches, so they can be toggled by hand
# add png, jpeg and more support
#

# Work in progress
# makes sure the window ratio is always 16:9
# def on_resize(debug, event):
#     if debug.winfo_height() != int(debug.winfo_width() / 16 * 9):  # if GUI height is not in scale of 16:9 to its width
#         print("resize triggered")  # information for debugging
#         debug.wm_geometry(f"{debug.winfo_width()}x{int(debug.winfo_width() / 16 * 9)}")  # set height to 16:9 ratio of current width


def toggle_debug_monitor():
    if gui.debug_switch_var.get() == 1:  # Open Debug Monitor
        debug, label_sc = gui.open_debugger()
        debug.wm_geometry("900x506")
        debug.resizable(False, False)  # user can only resize the width by, not the height
        # debug.bind("<Configure>", on_resize(debug)) Not working rn
        template_matching(debug, label_sc)


def update_debug_monitor(screenshot_np, debug, label_sc):
    screenshot = Image.fromarray(screenshot_np)  # convert np-array-screenshot so we can resize it in the next step
    screenshot = screenshot.resize((debug.winfo_width(), int(debug.winfo_width() / 16 * 9)))  # resize screenshot to fit the gui and leave some space on the edges
    screenshot_tk = ImageTk.PhotoImage(screenshot)  # convert screenshot into TKImage so we can put it into the label
    label_sc.configure(image=screenshot_tk)
    label_sc.image = screenshot_tk  # extra reference to avoid garbage collection
    debug.update()


def template_matching(debug, label_sc):
    while gui.debug_switch_var.get() == 1:
        screenshot_np = np.array(pyautogui.screenshot())  # grab and convert screenshot into np array for template matching
        screenshot_np_grey = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        template = cv2.imread("template.jpg", cv2.IMREAD_GRAYSCALE)

        # Actual matching process
        matching_data = cv2.matchTemplate(screenshot_np_grey, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(matching_data)

        if max_val >= 0.5:
            template_height, template_width = template.shape  # get template height and width
            top_left = max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

            # Draw rectangle in size of template around match and display match max_val of match
            if max_val >= 0.8:
                color = (0, 255)

                # this part is for clicking the found template
                # either way, clicking has to be done on the captcha, not in the middle of the match
                #
                # if debug_switch.get() == 1:
                #     middle_x = (top_left[0] + bottom_right[0]) // 2
                #     middle_y = (top_left[1] + bottom_right[1]) // 2
                #     pyautogui.click(middle_x, middle_y)

            else:
                color = 255

            cv2.rectangle(screenshot_np, top_left, bottom_right, color, 2)  # (image, top left, bottem right, color, thickness)
            cv2.putText(screenshot_np, f"{round(max_val, 3)}", (top_left[0], top_left[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            # org: It is the coordinates of the bottom-left corner of the text string in the image represented by a tuple

        else:
            cv2.putText(screenshot_np, "no match >0.5", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, 255, 4)

        update_debug_monitor(screenshot_np, debug, label_sc)

        if gui.debug_switch_var.get() == 0:
            debug.destroy()
