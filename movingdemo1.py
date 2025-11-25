import dearpygui.dearpygui as dpg
import comp151Colors
dpg.create_context()
ship_x = 200
ship_y = 300
ship_w, ship_h, channels, ship_raw_data = dpg.load_image("ship.png")
gold_w, gold_h, channels, gold_raw_data = dpg.load_image("gold-pile.png")
with dpg.texture_registry():
    dpg.add_static_texture(ship_w, ship_h, ship_raw_data, tag="ship_pict")
    dpg.add_static_texture(gold_w, gold_h, gold_raw_data, tag="gold_pict")
dpg.create_viewport(title='ImageDemo', width=800, height=800)
with dpg.window(label="Image Demo", width=800, height=800):
    with dpg.drawlist(width=800, height=800):
        dpg.draw_rectangle((0,0), (800, 800), fill=comp151Colors.BLUE)
        dpg.draw_image("ship_pict", (ship_x, ship_y), (ship_x+ship_w, ship_y+ship_h))


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()