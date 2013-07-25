'''
Game of Life

'''

import random
import pygame
from pygame.locals import *

ROWS = 100
COLUMNS = 100 
START_POPULATION = 700

def get_neighbours(row,column,current_gen):
    '''
    Return neighbours of cell at ROW, COLUMN.
    Neighbours are horizontally, vertically 
    or diagonally adjacent cells.
    '''
    lower_col = column - 1 if column > 0 else 0
    upper_col = column + 2 if column < COLUMNS - 1 else COLUMNS
    lower_row = row - 1 if row > 0 else 0
    upper_row = row + 2 if row < ROWS -1 else ROWS

    return [current_gen[x][y] for x in range(lower_row,upper_row) 
            for y in range(lower_col,upper_col) 
            if x != row or y != column]

def live_cells(neighbours):
    '''
    Returns the amount of live cells in 
    NEIGHBOURS.
    '''
    live = 0
    for n in neighbours:
        if n == 1:
            live += 1
    return live

def one_tick(current_gen, next_gen):
        
    for row in range(ROWS):

        for column in range(COLUMNS):

            cells = get_neighbours(row,column,current_gen)
            live = live_cells(cells)

            # Rules for Game of Life
            # 1. A live cell with fewer than 2 live neighbours dies
            if live < 2 and current_gen[row][column] == 1:
                next_gen[row][column] = 0
                
            # 2. A live cell with two or three live neighbours lives
            elif live > 2 and live < 4 and current_gen[row][column] == 1:
                next_gen[row][column] = 1

            # 3. A live cell with more than 3 live neigbours dies
            elif live > 3 and current_gen[row][column] == 1:
                next_gen[row][column] = 0

            # 4. A dead cell with 3 live neighbours becomes a live one    
            elif current_gen[row][column] == 0 and live == 3:
                next_gen[row][column] = 1

'''

Functions for drawing on a terminal

def draw_screen(gen):
    for row in range(ROWS):
        for column in range(COLUMNS):
            if gen[row][column] == 1:
                print '@'
            else:
                print ' ',
        print

def draw_blank(gen):
    #because sometimes 'clear' worked weirdly
    for row in range(ROWS):
        for column in range(COLUMNS):
            print ' ',
        print 

'''

def random_init(gen, start_population):
    '''
    Sets cells in random places as live.
    @param start_population: number of live cells
    in the beginning

    TODO: most calls give unfeasible seeds for the game, as
    cells are set too far apart.
    Maybe we should ensure there are at least some neighbours.
    '''
    for i in range(start_population):
        x = random.randrange(ROWS)
        y = random.randrange(COLUMNS)
        gen[x][y] = 1

def is_empty(gen):
    empty = True
    for row in range(ROWS):
        for column in range(COLUMNS):
            if gen[row][column] == 1:
                empty = False
                return empty
    return empty

def draw_pixarray(surface,gen,color):
    ''' 
    Another way to draw on screen
    '''
    pixarr = pygame.PixelArray(surface)
    for x in range(ROWS):
        for y in range(COLUMNS):
            if gen[x][y] == 1:
                   pixarr[x][y] = color
    del pixarr

def draw_rect(surface,gen,color):
     for x in range(ROWS):
        for y in range(COLUMNS):
            if gen[x][y] == 1:
                pygame.draw.rect(surface,color,(x*5,y*5,5,5))

if __name__ == '__main__':
    
    # Initialise graphics
    pygame.init()
    fpsClock = pygame.time.Clock()
    white = pygame.Color(255,255,255)
    black = pygame.Color(0,0,0)
    screen = pygame.display.set_mode((800,600))
    mousex, mousey = 0,0
    
    #Current generation is stored here
    current_gen = [[ r*0 for r in range(ROWS)] for c in range(COLUMNS)]

    #Next generation is calculated into this matrix and then drawn
    next_gen = [[ r*0 for r in range(ROWS)] for c in range(COLUMNS)]
   
    #Text on screen
    msg = 'Click to create initial conditions. Press q to start, or r for random conditions.'
    font_object = pygame.font.SysFont("monospace", 15)
    label = font_object.render(msg, 1, black)
    
    start_game = False

    while True:
        screen.fill(white)
        screen.blit(label, (0, 0))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_r:
                    random_init(current_gen,START_POPULATION)
                    start_game = True
                    break
                if event.key == K_q:
                    start_game= True
                    break
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mousex = mousex/5
                mousey = mousey/5
                if current_gen[mousex][mousey] == 0:
                    current_gen[mousex][mousey] = 1
                else:
                    current_gen[mousex][mousey] = 0
        draw_rect(screen,current_gen,black)
            
	
        pygame.display.update()
        if start_game:
            break

    while True:
        #Loop forever (quit with ctrl-c)
        screen.fill(white)
        one_tick(current_gen,next_gen)
        draw_rect(screen,next_gen,black)
        
        current_gen = next_gen
        if is_empty(current_gen):
            break
        
        
        pygame.display.update()
        fpsClock.tick(5)
       
