import threading
import keyboard
import bot
import gui
import captcha_debugger as cd

# FUTURE PROJECTS
#
# call or mail user if messaged by an admin
# look into multi scaling template matching
#


def toggle_bot_keypress():
    keyboard.wait("Ctrl+A")
    gui.bot_switch.toggle()
    threading.Thread(target=toggle_bot_keypress).start()
    run_bot()


def toggle_debug_monitor_keypress():
    keyboard.wait("Ctrl+D")
    gui.debug_switch.toggle()
    threading.Thread(target=toggle_debug_monitor_keypress).start()
    cd.toggle_debug_monitor()


def run_bot():
    max_counter = 500
    current_min_distance = 5000
    offset, nearest_target_vid, counter,  = 0, 0, 0
    while gui.bot_switch_var.get() == 1:
        counter += 1
        offset += 4
        print(counter)
        result = bot.search_nearest_target(offset)
        if result:
            distance, entity_vid = result
            if distance < current_min_distance:
                current_min_distance = distance
                nearest_target_vid = entity_vid

        if counter == max_counter:
            bot.attack_nearest_target(nearest_target_vid)
            current_min_distance = 5000
            offset, nearest_target_vid, counter = 0, 0, 0
            print("reset")


if __name__ == "__main__":
    threading.Thread(target=toggle_bot_keypress).start()
    threading.Thread(target=toggle_debug_monitor_keypress).start()
    gui.app.mainloop()
