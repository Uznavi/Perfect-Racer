#General information
fps = 60
game_width, game_height = 1300, 720
#Sprite Sheet Information and Text Color
textColor = (255,255,255)
#Animation process
animationLoop = 5
animationCooldown = 10
FRAME_WIDTH = 100
FRAME_HEIGHT = 100
HEIGHT_MULTIPLIER = 1.1

LANE_X_POSITION = [540, 625, 665, 705, 791]
#                 F.L  C.L  C  C.R  F.R
LANE_X_POSITION_BOXES = [540, 625, 705, 791]
#LEGEND: 
# F.L = Far left
# F.M.L = Far Middle Left
# C.L = Center Left
# C = Center
# C.R = Center Rigth
# F.M.R = Far Middle Right
# F.R = Far Right
POWER_UPS = ["shield", "bullets", "bomb"]


#CONTROLLER INPUTS
NS_A = 0
NS_B = 1
NS_Y = 3
NS_START = 6
NS_SELECT = 4
NS_HOME = 5
NS_D_PAD_LEFT = 13
NS_D_PAD_RIGHT = 14
NS_D_PAD_UP = 11
NS_D_PAD_DOWN = 12

PS_SQUARE = 2
PS_X = 0
PS_O = 1

CHEAT_CODE = ["up", "up", "down", "down", "left", "right", "left", "right", "b","a"]
FLASHING_COLORS = [(255,0,0), (0,255,0), (0,0,255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]