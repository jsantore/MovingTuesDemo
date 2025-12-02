import random

import dearpygui.dearpygui as dpg
import comp151Colors

#boiler plate
dpg.create_context()
#here I'm setting up all of the variables we want through the entire program
ship_x = 200
ship_y = 300
ship_speed = 5
number_piles_collected = 0
#loading the pictures from the disk and setting up variables for image width.height
#the unused color channel information and the raw images
ship_w, ship_h, channels, ship_raw_data = dpg.load_image("ship.png")
gold_w, gold_h, channels, gold_raw_data = dpg.load_image("gold-pile.png")

#here I put the functions - below the variables, but above the rest of the program that
#will use the variables
def move_ship(sender, app_data):
    global ship_x, ship_y, ship_speed, ship_w, ship_h
    key = app_data
    if key == dpg.mvKey_Left:
        ship_x -= ship_speed
    elif key == dpg.mvKey_Right:
        ship_x += ship_speed
    elif key == dpg.mvKey_Up:
        ship_y -= ship_speed
    elif key == dpg.mvKey_Down:
        ship_y += ship_speed
    with dpg.mutex():
        dpg.configure_item("ship_update", pmin=(ship_x, ship_y), pmax=(ship_x+ship_w, ship_y+ship_h))

def create_gold_pile(number):
    piles = []
    for i in range(number):
        current_x = random.randint(0, 720)
        current_y = random.randint(0, 720)
        current_pile = {
            "x": current_x,
            "y": current_y
        }
        piles.append(current_pile)
    return piles

def do_overlap(l1, r1, l2, r2):

    # If one rectangle is to the left of the other
    if l1.get('x') > r2.get('x') or l2.get('x') > r1.get('x'):
        return False

    # If one rectangle is above the other
    if r1.get('y') < l2.get('y') or r2.get('y') < l1.get('y'):
        return False

    return True

coin_piles = create_gold_pile(5)

#This creates the texture registry which holds all of the drawable images
#it absolutately has to be after the create context call
with dpg.texture_registry():
    dpg.add_static_texture(ship_w, ship_h, ship_raw_data, tag="ship_pict")
    dpg.add_static_texture(gold_w, gold_h, gold_raw_data, tag="gold_pict")
#put any an all event handling here. For our programs that will probably only be
# the keyboard handler, but theoretically we could do mouse or buttons as well
with dpg.handler_registry():
    dpg.add_key_press_handler(callback=move_ship)
#now the standard viewport, window and drawlist creation
dpg.create_viewport(title='ImageDemo', width=800, height=800)
with dpg.window(label="Image Demo", width=800, height=800):
    with dpg.drawlist(width=800, height=800):
        #everything needs to be drawn for the first time here in the drawlist
        dpg.draw_rectangle((0,0), (800, 800), fill=comp151Colors.BLUE)
        #when drawing images, the first argument is the tag from the texture registry
        #the second and third are the coordinates of the top left and bottom right corners
        # of the image and the tag argument is the tag you will used later to update/move
        #every one has to be unique
        dpg.draw_image("ship_pict", (ship_x, ship_y), (ship_x+ship_w, ship_y+ship_h), tag="ship_update")
        count = 0
        for pile in coin_piles:
            dpg.draw_image("gold_pict", (pile["x"], pile["y"]),
                           (pile["x"]+gold_w, pile["y"]+gold_h), tag = f"gold_update{count}")
            count += 1
        dpg.draw_text((20,20), f"You've collected {number_piles_collected} gold piles",
                      color = comp151Colors.WHEAT, size=20, tag="score_update")

#now we put the boiler plate for dearpy gui
dpg.setup_dearpygui()
dpg.show_viewport()
#between the show_viewport and the start_dearpygui, we can put this while loop to move things
while dpg.is_dearpygui_running():
    #here we first move and then draw the coin piles one by one
    counts = 0
    for pile in coin_piles:
        pile["y"]+=1
        if pile["y"] > 800:
            pile["y"] = 0 - gold_h
        dpg.configure_item(f"gold_update{counts}", pmin=(pile["x"], pile["y"]), pmax=(pile["x"]+gold_w, pile["y"]+gold_h))
        counts += 1
        #now we are getting the top left and bottom right corners of the ship
        # and the bottom right corner of the pile to use to check for overlap
        ship_top_left = {
            "x": ship_x,
            "y": ship_y
        }
        ship_bottom_right = {
            "x": ship_x+ship_w,
            "y": ship_y+ship_h
        }
        bottom_right_pile = {
            "x": pile["x"]+gold_w,
            "y": pile["y"]+gold_h
        }
        # if there is an overlap, we add one to the count of collected piles
        # and remove the pile from the list - removing it means we won't move it again, nor will
        # we count it for overlap checks
        if do_overlap(ship_top_left, ship_bottom_right, pile, bottom_right_pile):
            number_piles_collected += 1
            coin_piles.remove(pile)
            break #after removing one pile, break so we don't run off the list in the for loop
    #here we are updating the displayed text, otherwise it will just stay as initially drawn
    dpg.configure_item("score_update", text=f"You've collected {number_piles_collected} gold piles")
    dpg.render_dearpygui_frame() # render frame is vital, it will allow us to see the moves we made
dpg.start_dearpygui()
dpg.destroy_context()

def do_overlap(l1, r1, l2, r2):
    # If one rectangle is to the left of the other
    if l1.get('x') > r2.get('x') or l2.get('x') > r1.get('x'):
        return False

    # If one rectangle is above the other
    if r1.get('y') < l2.get('y') or r2.get('y') < l1.get('y'):
        return False

    return True







