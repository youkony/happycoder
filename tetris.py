
import random
import pygame
import copy



######### 
# colors []     : 10 random [r,g,b] colors
#                 color[0] is white as eraser

colors = [[random.randint(1,255) for n in range(3)] for m in range(10)]
colors[0] = [255,255,255]

########
# cBrick class   : brick class
#                 created when new brick is necessary
#       shapes []   : 4 types of brick shape. prime number 
#       bricks []   : store the brick images per rotations. multiplication of prime numbers (shapes)
#       x , y   : position of brick. when created, x = random, y = 0
#       r       : rotation. random in rotations when created
#       c       : colors. random in colors when created
#       s       : shape. random in shapes when created
#       image []    : the image of the brick. extracted from bricks using shape (s)    
#       __init__ () : initialize a brick when brick() is called
#       rotate ()   : update r. update the image of the rotation
#       move ()     : update x, y

class cBrick:

    shapes = [2,3,5,7] #I, Z, T, O
    bricks = [
        [ # rotation-0
            [1*3*5*7, 2*3*5*7, 1*1*5*1], 
            [1*1*1*7, 2*3*5*7, 1*1*1*1], 
            [1*1*1*1, 2*3*5*1, 1*3*1*1], 
        ],
        [ # rotation-1
            [1*1*1*7, 1*1*1*7, 1*3*5*1], 
            [2*3*5*7, 2*3*5*7, 2*3*5*1], 
            [1*3*1*1, 1*1*1*1, 1*1*5*1], 
        ],
        [ # rotation-2
            [1*3*1*7, 2*3*5*7, 1*1*1*1], 
            [1*1*1*7, 2*3*5*7, 1*1*1*1], 
            [1*1*5*1, 2*3*5*1, 1*3*5*1], 
        ],
        [ # rotation-3
            [1*1*5*7, 1*1*1*7, 1*3*1*1], 
            [2*3*5*7, 2*3*5*7, 2*3*5*1], 
            [1*3*5*1, 1*1*1*1, 1*1*1*1], 
        ],
    ]    
    
    x = 0
    y = 0
    r = 0 # rotation
    c = 0 # color
    s = 2 # shape
    image = None # [][]
    
    def __init__(self): 
        self.x = random.randint(0, 7)
        self.y = 0
        self.c = random.randint(1, len(colors)-1)
        self.s = self.shapes[random.randint(0, len(self.shapes)-1)]
        self.r = random.randint(0, 3)
        tmp = self.bricks[self.r]
        self.image = [[int(tmp[i][j] % self.s == 0) * self.c for j in range(3)] for i in range(3)] 
        
    def rotate(self, dr):
        self.r += dr
        self.r %= 4
        tmp = self.bricks[self.r]
        self.image = [[int(tmp[i][j] % self.s == 0) * self.c for j in range(3)] for i in range(3)] 
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

########
# cTetris class    : tetris class.  
#       h, w   : size of game board
#       brick *  : instance of cBrick
#       board [] : game board.
#       __init__ () : initialize Tetris when instance is created      
#       newBrick () : make new brick instance
#       moveBrick ()
#       rotateBrick ()
#       dropBrick ()
#       freezeBrick ()  : when brick meets bottom, brick image is merged to board.
#       intersact () : decide the brick meets obstacles.
#       composite () : merge the brick image to board image
#       getImage () : get image that is displayed 
#       removeRows () : remove the filled rows in board

class cTetris:
    h = 0
    w = 0
    brick = None
    board = None # [][]

    def __init__(self, h, w):
        self.h = h 
        self.w = w
        self.board = [[0 for i in range(w)] for j in range(h)]
            
    def newBrick(self):
       self.brick = cBrick()

    def moveBrick(self, dx, dy):
        self.brick.move(dx, dy)

    def rotateBrick(self, dr):
        self.brick.rotate(dr)    
        
    def dropBrick(self):
        for j in range(self.brick.y, len(self.board)):
            self.moveBrick(0, 1)
            if self.intersect() == True:
                self.moveBrick(0, -1)
                break        
    
    def freezeBrick(self):
        self.composite(self.board, self.brick) 
    
    def composite(self, board, brick):
        y = brick.y
        x = brick.x
        for j in range(y, y+len(brick.image)):
            if j >= 0 and j < len(board):
                for i in range(x, x+len(brick.image[j-y])):
                    if i >= 0 and i < len(board[j]) and brick.image[j-y][i-x] != 0:
                        board[j][i] = brick.image[j-y][i-x]
                
    def intersect(self):
        s1 = 0
        for j in range(len(self.board)):
            s1 += sum(self.board[j])
        for j in range(len(self.brick.image)):
            s1 += sum(self.brick.image[j])

        s2 = 0
        tmp = self.getImage()          
        for j in range(len(tmp)):
            s2 += sum(tmp[j])
        
        return (s1 != s2)
    
    def getImage(self):
        tmp = copy.deepcopy(self.board)
        if self.brick is not None:   
            self.composite(tmp, self.brick)
        return tmp
                    
    def removeRows(self):
        for j in range(len(self.board)):
            m = 1
            for i in range(len(self.board[j])):
                m *= self.board[j][i]
            if m != 0:
                for jj in range(j, 0, -1):
                    self.board[jj] = copy.deepcopy(self.board[jj-1]) 
                self.board[0] = [0 for i in range(len(self.board[jj]))]    

#########
# game routine
# 
# pygame.init() 
# pygame.display.set_mode()
# pygame.time.clock()
# create cTetris isntance
# while 
#   move_down
#   for event in pygame.event.get()
#       if key-down & UP : rotate
#       if key-down & SPACE : drop
#       if key-down & LEFT : move_left
#       if key-down & RIGHT : move_right
#       if quit : do quit
#   gameover decision    
#   redraw board
#   redraw text
# pygame.quit()        

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)

X = 100
Y = 60
ZOOM = 20
SCREEN_SIZE = (400, 500)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
    
done = False
clock = pygame.time.Clock()
fps = 10
counter = 0
pressing_down = False
state = "start"

tetris = cTetris(20, 10)

while not done:
    
    if tetris.brick is None:
        tetris.newBrick()
        
    counter += 1
    if counter > 100000:
        counter = 0
    if counter % fps == 0 or pressing_down:
        if state == "start":
            tetris.moveBrick(0, 1)
            if tetris.intersect():
                tetris.moveBrick(0, -1)
                tetris.freezeBrick()
                tetris.removeRows()
                tetris.newBrick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                tetris.rotateBrick(1)
                if tetris.intersect():
                    tetris.rotateBrick(-1)
            if event.key == pygame.K_DOWN:
                pressing_down = True              
            if event.key == pygame.K_LEFT:
                tetris.moveBrick(-1, 0)
                if tetris.intersect():
                    tetris.moveBrick(1, 0)
            if event.key == pygame.K_RIGHT:
                tetris.moveBrick(1, 0)
                if tetris.intersect():
                    tetris.moveBrick(-1, 0)
            if event.key == pygame.K_SPACE:
                tetris.dropBrick()
                tetris.freezeBrick()
                tetris.removeRows()
                tetris.newBrick()
            if event.key == pygame.K_ESCAPE:
                state = "start"
                tetris.__init__(20, 10)
                tetris.newBrick()
                continue

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    if tetris.intersect():
        state = "gameover"
        
    for i in range(tetris.h):
        for j in range(tetris.w):
            pygame.draw.rect(screen, GRAY, [X + ZOOM * j, Y + ZOOM * i, ZOOM, ZOOM], 1)
            image = tetris.getImage()
            pygame.draw.rect(screen, colors[image[i][j]],
                                 [X + ZOOM * j + 1, Y + ZOOM * i + 1, ZOOM - 2, ZOOM - 1])

    font1 = pygame.font.SysFont('Calibri', 40, True, False)
    text_game_over = font1.render("Game Over", True, (0, 0, 0))
    text_game_over1 = font1.render("Press ESC", True, (0, 0, 0))

    if state == "gameover":
        screen.blit(text_game_over, [105, 200])
        screen.blit(text_game_over1, [110, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
