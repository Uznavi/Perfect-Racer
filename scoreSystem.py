import os

HIGH_SCORE_FILE = "highscore.txt"

def loadHighScore():
    if not os.path.exists(HIGH_SCORE_FILE):
        return 0
    with open(HIGH_SCORE_FILE, "r") as f:
        return int(f.read())
    
def saveHighScore(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))