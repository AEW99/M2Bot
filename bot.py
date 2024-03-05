import pymem.process
from ReadWriteMemory import ReadWriteMemory
import math
import time

rwm = ReadWriteMemory()
process = rwm.get_process_by_name("Zenit-55.exe")
process.open()


pm = pymem.Pymem("Zenit-55.exe")

base = pm.base_address

entitylist_base = 0x01E9BE10
# offsets
entity_type_offset = 0x1ab0
entity_vid_offset = 0x1c24
x_cords_offset = 0x364
y_cords_offset = 0x368

player_base = 0x01E9964C
# offsets
current_player_offset = 0x14

mouse_base = 0x01E99678
# offsets
vid_offset = 0x29210
target_offset = 0x4C

entitylist = process.read(base + entitylist_base)
playerlist = process.read(base + player_base)
mousemanager = process.read(base + mouse_base)

current_player = process.read(playerlist + 0x14)


def search_nearest_target(offset):
    current_entity = process.read(entitylist + offset)
    entity_type_address = current_entity + entity_type_offset
    if entity_type_address > 4294967295:
        return None
    entity_type = process.read(entity_type_address)

# get player cords and target cords to calcuate distance
    if entity_type == 2:
        x_cords_player = pm.read_float(current_player + x_cords_offset)
        y_cords_player = abs(pm.read_float(current_player + y_cords_offset))
        x_cords_entity = pm.read_float(current_entity + x_cords_offset)
        y_cords_entity = abs(pm.read_float(current_entity + y_cords_offset))
        distance = math.sqrt((x_cords_entity - x_cords_player) ** 2 + (y_cords_entity - y_cords_player) ** 2)
        entity_vid = process.read(current_entity + entity_vid_offset)
        return distance, entity_vid
    return None


def attack_nearest_target(nearest_target_vid):
    process.write(mousemanager + target_offset, nearest_target_vid)
    time.sleep(2) # To do : search for some kind of "is_running offset" and check for that
    is_attacking = process.read(current_player + 0x1AAC)
    while is_attacking != 0:
        is_attacking = process.read(current_player + 0x1AAC)
