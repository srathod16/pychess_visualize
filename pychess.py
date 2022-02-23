import os
os.chdir('my dir')

import chess
import chess.svg
import chess.pgn
import pandas as pd
import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap




board = chess.Board()

#my pgn file
xpgn = 'anand_kasparov_1991.pgn'

pgn = open(str(xpgn))

first_game = chess.pgn.read_game(pgn)
first_game.headers["Event"]
board = first_game.board()

moves = list() #this saves the moves list as initial and final chess.square destinations
for move in first_game.mainline_moves():
    moves.append(move)

moves_list = pd.DataFrame(moves) #slightly organized and only numbers


#read the lookup table for coordinate system
init_coord = pd.read_excel("init_lookup_for_x_y.xlsx",skiprows=0)
fina_coord = pd.read_excel("fina_lookup_for_x_y.xlsx",skiprows=0)

#do a VLOOKUP using pandas left join
init_results = moves_list.merge(init_coord, on='from_square', how = 'left')
fina_results = moves_list.merge(fina_coord, on='to_square', how = 'left')


#the cartesian coords to plot
init_x = init_results['init_x'] + 0.5
init_y = init_results['init_y'] + 0.5

fina_x = fina_results['fina_x'] + 0.5
fina_y = fina_results['fina_y'] + 0.5


#light and dark squares as rectangles
ds = pd.read_excel("chessboard_dark_squares.xlsx",skiprows=0)
ls = pd.read_excel("chessboard_light_squares.xlsx",skiprows=0)

dsi = ds['i']
dsj = ds['j']
lsi = ls['i']
lsj = ls['j']



#colors
whitep = 'darkgoldenrod'
blackp = 'k'
dsqc = 'k'
lsqc = 'lightgray'
boardec = 'none'
balpha = 0.35
palpha = 0.65
color = [whitep, blackp]

#plot !
fig = plt.figure(figsize=(5,5))
plt.style.use('default')


for i in range(0, len(init_x)):
    plt.plot([init_x[i], fina_x[i]], [init_y[i], fina_y[i]], lw = 4.2 if i%2==0 else 3.8, c = color[0] if i%2==0 else color[1], alpha = palpha,solid_capstyle='round')


for  i in range(0,32):
    drect = patches.Rectangle((dsi[i],dsj[i]),1,1,edgecolor = boardec, facecolor = dsqc, alpha = balpha)
    lrect = patches.Rectangle((lsi[i],lsj[i]),1,1,edgecolor = boardec, facecolor = lsqc, alpha = balpha)
    plt.gca().add_patch(drect)
    plt.gca().add_patch(lrect)


frame1 = plt.gca()
frame1.axes.xaxis.set_ticklabels([])
frame1.axes.yaxis.set_ticklabels([])
frame1.axes.xaxis.set_ticks([])
frame1.axes.yaxis.set_ticks([])

plt.title(str(xpgn) + '\n' + first_game.headers["Event"], fontname = 'Times New Roman', y=-0.1, loc = 'center', fontsize = 12)
plt.tight_layout()
plt.show()

