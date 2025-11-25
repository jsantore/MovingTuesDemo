import dearpygui.dearpygui as dpg
import comp151Colors
dpg.create_context()
ship_x = 200
ship_y = 300
ship_speed = 5
ship_w, ship_h, channels, ship_raw_data = dpg.load_image("ship.png")
gold_w, gold_h, channels, gold_raw_data = dpg.load_image("gold-pile.png")

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

with dpg.texture_registry():
    dpg.add_static_texture(ship_w, ship_h, ship_raw_data, tag="ship_pict")
    dpg.add_static_texture(gold_w, gold_h, gold_raw_data, tag="gold_pict")
with dpg.handler_registry():
    dpg.add_key_press_handler(callback=move_ship)
dpg.create_viewport(title='ImageDemo', width=800, height=800)
with dpg.window(label="Image Demo", width=800, height=800):
    with dpg.drawlist(width=800, height=800):
        dpg.draw_rectangle((0,0), (800, 800), fill=comp151Colors.BLUE)
        dpg.draw_image("ship_pict", (ship_x, ship_y), (ship_x+ship_w, ship_y+ship_h), tag="ship_update")


dpg.setup_dearpygui()
dpg.show_viewport()
while dpg.is_dearpygui_running():
    # ship_x += ship_speed
    # if ship_x > 800 or ship_x < 0:
    #     ship_speed = -ship_speed
    # # if ship_x > 800:    # ship loops around
    # #     ship_x = -ship_w
    # dpg.configure_item("ship_update", pmin=(ship_x, ship_y), pmax=(ship_x+ship_w, ship_y+ship_h))
    dpg.render_dearpygui_frame()
dpg.start_dearpygui()
dpg.destroy_context()