
import random
import pygame
import copy

colors = [[random.randint(1,255) for n in range(3)] for m in range(10)]
colors[0] = [255,255,255]

class brick:

    shapes = [2,3,5,7] #I, 2, T, O
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

class board:
    h = 0
    w = 0
    b = None # brick
    grid = None # [][]

    def __init__(self, h, w):
        self.h = h 
        self.w = w
        self.grid = [[0 for i in range(w)] for j in range(h)]
            
    def newBrick(self):
       self.b = brick()

    def moveBrick(self, dx, dy):
        self.b.move(dx, dy)

    def rotateBrick(self, dr):
        self.b.rotate(dr)    
        
    def dropBrick(self):
        for j in range(self.b.y, len(self.grid)):
            self.moveBrick(0, 1)
            if self.intersect() == True:
                self.moveBrick(0, -1)
                break        
    
    def freezeBrick(self):
        self.composite(self.grid, self.b) 
    
    def composite(self, grid, brick):
        y = brick.y
        x = brick.x
        for j in range(y, y+len(brick.image)):
            if j >= 0 and j < len(grid):
                for i in range(x, x+len(brick.image[j-y])):
                    if i >= 0 and i < len(grid[j]) and brick.image[j-y][i-x] != 0:
                        grid[j][i] = brick.image[j-y][i-x]
                
    def intersect(self):
        s1 = 0
        for j in range(len(self.grid)):
            s1 += sum(self.grid[j])
        for j in range(len(self.b.image)):
            s1 += sum(self.b.image[j])

        s2 = 0
        tmp = self.getImage()          
        for j in range(len(tmp)):
            s2 += sum(tmp[j])
        
        return (s1 != s2)
    
    def getImage(self):
        tmp = copy.deepcopy(self.grid)
        if self.b is not None:   
            self.composite(tmp, self.b)
        return tmp
                    
    def removeRows(self):
        for j in range(len(self.grid)):
            m = 1
            for i in range(len(self.grid[j])):
                m *= self.grid[j][i]
            if m != 0:
                for jj in range(j, 0, -1):
                    self.grid[jj] = copy.deepcopy(self.grid[jj-1]) 
                self.grid[0] = [0 for i in range(len(self.grid[jj]))]    

#
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

tetris = board(20, 10)

while not done:
    
    if tetris.b is None:
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
