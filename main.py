import pygame
import random

GRID_WIDTH=GRID_HEIGHT=4
PADDING=15
FONT="fonts/ClearSans-"

tileColors={
 "grid":"#bbada0",
   "bg":"#faf8ef",
   "fg":"#776e65",
"score":"#eee4da",
"empty":("#cdc1b4","#000000"),
     -2:("#d9e3ee","#776e65"),
     -4:("#b1c8e0","#776e65"),
     -8:("#78b9f2","#f9f6f2"),
    -16:("#198edd","#f9f6f2"),
    -32:("#2374e4","#f9f6f2"),
    -64:("#1d22e2","#f9f6f2"),
   -128:("#4f27db","#f9f6f2"),
   -256:("#441ec9","#f9f6f2"),
   -512:("#3a18b3","#f9f6f2"),
  -1024:("#4a18b3","#f9f6f2"),
  -2048:("#5b18a0","#f9f6f2"),
  -4096:("#8218c4","#f9f6f2"),
  -8192:("#ab1ed6","#f9f6f2"),
 -16384:("#ed1adf","#f9f6f2"),
 -32768:("#f00ea8","#f9f6f2"),
 -65536:("#f5077a","#f9f6f2"),
      0:("#504b44","#f9f6f2"),
      1:("#f5f2e7","#776e65"),
      2:("#eee4da","#776e65"),
      4:("#ede0c8","#776e65"),
      8:("#f2b179","#f9f6f2"),
     16:("#f59563","#f9f6f2"),
     32:("#f67c5f","#f9f6f2"),
     64:("#f65e3b","#f9f6f2"),
    128:("#edcf72","#f9f6f2"),
    256:("#edcc61","#f9f6f2"),
    512:("#edc850","#f9f6f2"),
   1024:("#edc53f","#f9f6f2"),
   2048:("#edc22e","#f9f6f2"),
   4096:("#2eed72","#f9f6f2"),
   8192:("#2ef547","#f9f6f2"),
  16384:("#22ff27","#f9f6f2"),
  32768:("#20f7c0","#f9f6f2"),
  65536:("#20f7f0","#f9f6f2"),
"super":("#3c3a32","#f9f6f2"),
}

score=3932028
grid=[
[     4,   512,  1024,131072],
[     8,   256,  2048, 65536],
[    16,   128,  4096, 32768],
[    32,    64,  8192, 16384]
]

grid=[
[  None,  2,     16,  2048],
[  None,  2,     32,  1024],
[  None,  2,     64,   512],
[  None,     2,    128,   256]
]

def getVector(direction):
  map={
    0:{"x": 0, "y":-1},
    1:{"x": 1, "y": 0},
    2:{"x": 0, "y": 1},
    3:{"x":-1, "y": 0}
  }
  return map[direction]

def buildTraversals(vector):
    traversals={"x":[],"y":[]}
    for pos in range(GRID_WIDTH): traversals["x"].append(pos)
    for pos in range(GRID_HEIGHT): traversals["y"].append(pos)
    if vector["x"]==1: traversals["x"].reverse()
    if vector["y"]==1: traversals["y"].reverse()
    return traversals


def moveTile(grid,x,y,tx,ty):
    value=grid[x][y]
    grid[x][y]=None
    grid[tx][ty]=value
    return grid

def findFarthestPosition(grid,x,y,vector):
    px,py=x,y
    while True:
        px,py=x,y
        x,y=px+vector["x"],py+vector["y"]
        if not (withinBounds(x,y) and grid[x][y]==None): break
    return {
        "farthest":{"x":px,"y":py},
        "next":{"x":x,"y":y}
        }

def move(grid,direction):
    vector=getVector(direction)
    traversals=buildTraversals(vector)
    moves=[]
    merges=[]
    moveScore=0
    moved=False
    merged=[[False for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    for x in traversals["x"]:
        for y in traversals["y"]:
            value=grid[x][y]
            if value:
                positions=findFarthestPosition(grid,x,y,vector)
                nextX=positions["next"]["x"]
                nextY=positions["next"]["y"]
                farX=positions["farthest"]["x"]
                farY=positions["farthest"]["y"]
                next=None
                if withinBounds(nextX,nextY): next=grid[nextX][nextY]
                if next!=None and next==value and not merged[nextX][nextY]:
                    moved=True
                    grid[x][y]=None
                    newValue=value+next
                    grid[nextX][nextY]=newValue
                    moveScore+=newValue
                    merged[nextX][nextY]=True
                    moves.append(((x,y),(nextX,nextY),value,0))
                    merges.append(((nextX,nextY),newValue))
                elif (farX!=x or farY!=y) and withinBounds(farX,farY):
                    moved=True
                    grid=moveTile(grid,x,y,farX,farY)
                    moves.append(((x,y),(farX,farY),value,0))
                elif next==None:
                    print("tile: ",x,y,",",nextX,nextY)
                    moves.append(((x,y),(farX,farY),value,-6))


    newTiles=[]
    if moved:
        grid,ntX,ntY,ntValue=addRandomTile(grid)
        newTiles.append(((ntX,ntY),ntValue))
        print("Move score:",moveScore)
        moveAnims.clear()
        mergeAnims.clear()
        newTileAnims.clear()
    startAnimations(moves,merges,newTiles)

    return grid

moveAnims=[]
mergeAnims=[]
newTileAnims=[]

def startAnimations(moves,merges,newTiles):
    for move in moves:
        moveAnims.append({
            "start":move[0],
            "end":move[1],
            "value":move[2],
            "frames":move[3],
        })
    for merge in merges:
        mergeAnims.append({
            "pos":merge[0],
            "value":merge[1],
            "frames":-6,
        })
    for tile in newTiles:
        newTileAnims.append({
            "pos":tile[0],
            "value":tile[1],
            "frames":-6,
        })


def avg(*values): return sum(values)/len(values)
def wavg(values,weights):
    if len(values)!=len(weights): raise ValueError("Values and weights must be the same length")
    return sum(v*w for v,w in zip(values,weights))/sum(weights)

def easeInOut(t): return t*t*(3-2*t)

def popAnimation(progress):
    eased=easeInOut(progress)
    if eased<0.5: scale=(eased/0.5)*1.2
    else: scale=1.2-((eased-0.5)/0.5)*0.2
    return scale

MOVE_ANIM_FRAMES=6
MERGE_ANIM_FRAMES=12
NEWTILE_ANIM_FRAMES=12

def animationStep():
    for idx,anim in enumerate(moveAnims):
        anim["frames"]+=1
        startX,startY=getTileStartCoords(anim["start"][0],anim["start"][1])
        endX,endY=getTileStartCoords(anim["end"][0],anim["end"][1])
        progress=easeInOut(max(0,min(1,anim["frames"]/MOVE_ANIM_FRAMES)))
        finalX=wavg((startX,endX),(1-progress,progress))
        finalY=wavg((startY,endY),(1-progress,progress))
        drawTile(anim["value"],finalX,finalY)
        if anim["frames"]>=MOVE_ANIM_FRAMES+1: moveAnims.pop(idx)

    for idx,anim in enumerate(mergeAnims):
        anim["frames"]+=1
        if anim["frames"]>=0:
            tileX,tileY=getTileStartCoords(anim["pos"][0],anim["pos"][1])
            tileScale=tileWidth*popAnimation(min(1,anim["frames"]/NEWTILE_ANIM_FRAMES))
            centerX,centerY=tileX+(tileWidth/2),tileY+(tileHeight/2)
            newTileX,newTileY=centerX-(tileScale/2),centerY-(tileScale/2)
            drawTile(anim["value"],newTileX,newTileY,tileScale,tileScale)
            if anim["frames"]>=MERGE_ANIM_FRAMES+1: mergeAnims.pop(idx)

    for idx,anim in enumerate(newTileAnims):
        anim["frames"]+=1
        if anim["frames"]>=0:
            tileX,tileY=getTileStartCoords(anim["pos"][0],anim["pos"][1])
            progress=easeInOut(min(1,anim["frames"]/NEWTILE_ANIM_FRAMES))
            tileScale=tileWidth*progress
            centerX,centerY=tileX+(tileWidth/2),tileY+(tileHeight/2)
            newTileX,newTileY=centerX-(tileScale/2),centerY-(tileScale/2)
            drawTile(anim["value"],newTileX,newTileY,tileScale,tileScale)
            if anim["frames"]>=NEWTILE_ANIM_FRAMES+1: newTileAnims.pop(idx)



def addRandomTile(grid):
    empty=[]
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y]==None: empty.append((x,y))
    x,y=random.choice(empty)
    value=2 if random.random()<0.9 else 4
    grid[x][y]=value
    return grid,x,y,value

def withinBounds(x,y):
    return 0<=x<GRID_WIDTH and 0<=y<GRID_HEIGHT


def updateSizes():
    global gridWidth,gridHeight,gridSX,gridSY,padding,tileWidth,tileHeight
    padding=maxGridWidth/8/max(GRID_WIDTH,GRID_HEIGHT)
    totalPaddingX=padding*(GRID_WIDTH+1);
    totalPaddingY=padding*(GRID_HEIGHT+1);
    availableWidth=maxGridWidth-totalPaddingX;
    availableHeight=maxGridHeight-totalPaddingY;
    tileWidth=min(availableWidth/GRID_WIDTH,availableHeight/GRID_HEIGHT)
    tileHeight=tileWidth
    gridWidth=totalPaddingX+tileWidth*GRID_WIDTH
    gridHeight=totalPaddingY+tileHeight*GRID_HEIGHT
    gridSX,gridSY=(canvasWidth-gridWidth)/2,200


def drawTile(value,startX,startY,tw=None,th=None):
    if value==None: return
    if tw==None: tw=tileWidth
    if th==None: th=tileHeight
    bg,fg=tileColors["empty" if value==None else ("super" if value>65536 else value)]
    fontSize=int((tw*0.6)/((max(len(str(value)),2)+1.3)*0.33))
    pygame.draw.rect(screen,bg,pygame.Rect(startX,startY,tw,th),0,3)
    tileText=pygame.font.Font(FONT+"Bold.ttf",fontSize).render(str(value),True,fg)
    tileRect=tileText.get_rect(center=(startX+tw/2,startY+th/2))
    screen.blit(tileText,tileRect)

def getTileStartCoords(x,y):
    return gridSX+x*tileWidth+padding*(x+1),gridSY+y*tileHeight+padding*(y+1)

def drawGrid(grid):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            bg,fg=tileColors["empty"]
            startX,startY=getTileStartCoords(x,y)
            pygame.draw.rect(screen,bg,pygame.Rect(startX,startY,tileWidth,tileHeight),0,3)
            draw=True
            for anim in moveAnims:
                if anim["end"][0]==x and anim["end"][1]==y and anim["frames"]<MOVE_ANIM_FRAMES-1: draw=False
                #print("  move",draw,anim)
            for anim in mergeAnims:
                if anim["pos"][0]==x and anim["pos"][1]==y and anim["frames"]<MERGE_ANIM_FRAMES-1: draw=False
                #print("  merge",draw,anim)
            for anim in newTileAnims:
                if anim["pos"][0]==x and anim["pos"][1]==y and anim["frames"]<NEWTILE_ANIM_FRAMES-1: draw=False
                #print("  new",draw,anim)
            if draw: drawTile(grid[x][y],startX,startY)

def newGame():
    grid=[[None for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    for _ in range(2):
        grid,x,y,v=addRandomTile(grid)
    return grid

def tileClick(x,y):
    print(f"tile clicked at {x},{y}, value: {grid[x][y]}")

key2name={
    pygame.K_UP:   0,
    pygame.K_RIGHT:1,
    pygame.K_DOWN: 2,
    pygame.K_LEFT: 3,
    pygame.K_w:    0,
    pygame.K_d:    1,
    pygame.K_s:    2,
    pygame.K_a:    3,
    pygame.K_m:"toggleAuto",
    pygame.K_r:"restart",
    pygame.K_u:"undo",
}

canvasWidth,canvasHeight=540,800
maxGridWidth,maxGridHeight=500,500

pygame.init()
screen=pygame.display.set_mode((canvasWidth,canvasHeight),pygame.RESIZABLE)
pygame.display.set_caption("2048")
clock=pygame.time.Clock()
screen.fill("#faf8ef")

mainText=pygame.font.Font(FONT+"Bold.ttf",80).render("2048",True,tileColors["fg"])
screen.blit(mainText,(20,40))
gameIntroText=pygame.font.Font(FONT+"Regular.ttf",18).render("Join the numbers to get the 2048 tile!",True,tileColors["fg"])
screen.blit(gameIntroText,(20,140))

GRID_WIDTH,GRID_HEIGHT=4,4
#GRID_WIDTH,GRID_HEIGHT=3,3

#grid=newGame()

updateSizes()


pygame.key.set_repeat(400,50)

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        elif event.type==pygame.KEYDOWN:
            key=event.key
            n=key2name.get(key)
            if n=="restart": grid=newGame()
            elif type(n)==int:
                grid=move(grid,n)
    canvasWidth,canvasHeight=screen.get_size()
    updateSizes()
    screen.fill("#faf8ef")

    mainText=pygame.font.Font(FONT+"Bold.ttf",80).render("2048",True,tileColors["fg"])
    screen.blit(mainText,(20,40))
    gameIntroText=pygame.font.Font(FONT+"Regular.ttf",18).render("Join the numbers to get the 2048 tile!",True,tileColors["fg"])
    screen.blit(gameIntroText,(20,140))
    pygame.draw.rect(screen,tileColors["grid"],pygame.Rect(gridSX,gridSY,gridWidth,gridHeight),0,6)

    drawGrid(grid)
    animationStep()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()



"""
app.bind("<Up>",lambda event: guiMove(0))
app.bind("<Right>",lambda event: guiMove(1))
app.bind("<Down>",lambda event: guiMove(2))
app.bind("<Left>",lambda event: guiMove(3))

drawGrid(grid)



app.mainloop()
"""
