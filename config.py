#Imports rgb values for common colours
import colours

background_image = 'images/asanoha-400px.png' #CREDIT: https://www.toptal.com/designers/subtlepatterns/japanese-asanoha/ - Accessed 1 Jan 2021
caption = 'Takenoko'
frame_rate = 30

image_tile_pond = 'images/tiles/tile.png'
tile_colours = ['green', 'yellow', 'pink']
image_tiles = ['images/tiles/green.png', 'images/tiles/yellow.png', 'images/tiles/pink.png']
image_tiles_hover = ['images/tiles/green_hover.png', 'images/tiles/yellow_hover.png', 'images/tiles/pink_hover.png']
image_tiles_click = ['images/tiles/green_click.png', 'images/tiles/yellow_click.png', 'images/tiles/pink_click.png']

image_bamboo = ['images/bamboo/green.png', 'images/bamboo/yellow.png', 'images/bamboo/pink.png']

width, height = 1400, 800
board_center = (width / 2, height / 2)

number_of_players = 2

top_bar_colour = colours.TAN
top_bar_height = 40
top_bar_outline_colour = colours.DARKSLATEGRAY
top_bar_outline_thickness = 4

font_name = 'HelveticaNeue'
font_size = 20

player_label_colour = colours.BLACK

button_text_colour = colours.BLACK
button_colour = colours.CADETBLUE1
button_hover_colour = colours.CADETBLUE2
button_click_colour = colours.CADETBLUE3

hexagon_size = 70 #Radius (ie distance from point of hexagon to center)

bamboo_height = 15
bamboo_width = 20
max_bamboo = 4

bamboo_location_x = 20
bamboo_location_y = hexagon_size - ((bamboo_height * max_bamboo) / 2)

panda_image = 'images/panda.png'
panda_width = 40
panda_height = 40

gardener_image = 'images/gardener.png'
gardener_width = panda_width
gardener_height = panda_height