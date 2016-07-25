import random
#Abstract Entity
class Entity:
    def __init__(self, ascii, x, y):
        self.ascii = ascii
        self.x = x
        self.y = y

class PerminantEntity:
    def __init__(self, ascii):
        self.ascii = ascii


class Tile(PerminantEntity):
    def __init__(self, ascii , blocked, blocked_sight):
        PerminantEntity.__init__(self, ascii)
        #super(Tile, self).__init__(ascii)

        self.blocked = blocked
        self.blocked_sight = blocked_sight
    
    def set_invisible(self):
        self.blocked_sight = True

    def set_visible(self):
        self.blocked_sight = False


class NPC(Entity):
    def __init__(self, ascii, x, y, hp):
        self.ascii = ascii
        self.x = x
        self.y = y
        self.hp = hp

    def Move(self, dx, dy, nmap, tmap):
        if tmap[self.y+dy][self.x+dx] is not None and tmap[self.y+dy][self.x+dx].blocked == True:
            return
        else:
            if nmap[self.y+dy][self.x+dx] is not None:
                return
            else:
                self.x += dx
                self.y += dy

#Defined entities

class Wall(Tile):
    def __init__(self):
        Tile.__init__(self, "#", True, False)
        #super(Wall, self).__init__("#", True, False)

class Door(Tile):
    def __init__(self):
        Tile.__init__(self, "!", True, True)
        #super(Door, self).__init__("!", True, False)
        
        #Statuses
        #0 = Open
        #1 = Closed

        self.status = 1

    def open_door(self):
        if self.blocked == True and self.status == 1: # Open
            self.blocked = False
            self.status = 0
            self.ascii = "_"
            #self.blocked_sight = True
        else: # Close
            self.blocked = True
            #self.blocked_sight = False
            self.ascii = "!"
            self.status = 1
            
class Exit(Tile):
    def __init__(self):
        Tile.__init__(self, ">", False, False)

    def Activate(self, i):
        self.i.status = 1
        
class Player(NPC):
    def __init__(self, ascii, x, y, hp):
        NPC.__init__(self, ascii, x, y, hp)
        self.status = 0
        #Statuses
        # 0 = In-Game
        # 1 = Exited
        
    def handle_input(self, i, nmap, tmap):
        i = i.upper()
        if i == "N":
            self.Move(0, -1, nmap, tmap)
        elif i == "S":
            self.Move(0, 1, nmap, tmap)
        elif i == "E":
            self.Move(-1, 0, nmap, tmap)
        elif i == "W":
            self.Move(1, 0, nmap, tmap)
    

class Enemy(NPC):
    def __init__(self, name, ascii, x, y, hp):
        NPC.__init__(self, ascii, x, y, hp)
        self.name = name

        

class Map:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.tile_map = [[ Wall() for x in range(0, self.width)] for y in range(0, self.height)]
        self.npc_map = [[ None for x in range(0, self.width)] for y in range(0, self.height)]
        self.npc = []

    def clear_space(self, xpoint, ypoint, height, width):
        for y in range(ypoint, ypoint+height):
            for x in range(xpoint, xpoint+width):
                self.tile_map[y][x] = None

        
    def AddTile(self, item, x, y, overwrite=1):
        point = self.tile_map[y][x]
        if point is Tile:
            if overwrite == 1:
                self.tile_map[y][x] = item
            else:
                return
        else:
            self.tile_map[y][x] = item

    def AddNPC(self, item, overwrite=1):
        point = self.npc_map[item.y][item.x]
        if point is NPC:
            if overwrite == 1:
                self.npc_map[item.y][item.x] = item
            else:
                return
        else:
            self.npc_map[item.y][item.x] = item
            
    def Generate_ascii(self, skipchar="."):
        ascii_map = [[ " " for x in range(0, self.width)] for y in range(0, self.height)]

        #Convert tile map first
        for y in range(0, self.height):
            ypoint = self.tile_map[y]
            for x in range(0, self.width):
                xpoint = ypoint[x]
                if xpoint is not None:
                    ascii_map[y][x] = xpoint.ascii
                else:
                    ascii_map[y][x] = skipchar

        for y in range(0, self.height):
            ypoint = self.npc_map[y]
            for x in range(0, self.width):
                xpoint = ypoint[x]
                if xpoint is not None:
                    ascii_map[y][x] = xpoint.ascii
                    
        return ascii_map


    def Convert2Displayable(self, ascii_map):
        displayable = []
        temp = ""
        for y in range(0, self.height):
            ypoint = ascii_map[y]
            for x in range(0, self.width):
                xpoint = ypoint[x]
                temp += xpoint
            displayable.append(temp)
            temp = ""
        return displayable

    def ReInitializeNpc_map(self, i):
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.npc_map[y][x] = None

        for w in i:
            self.npc_map[w.y][w.x] = w
            
    def CreateVerticalLine(self, x, y, length):
        for x in range(x, x+length):
            self.tile_map[y][x] = None

    def CreateHorizontalLine(self, x, y, length):
        for y in range(y, y+length):
            self.tile_map[y][x] = None

    def GenNCmp(self, cmp1, range1, range2):
        r1 = None
        equal = False
        while equal != True:
            r1 = random.randint(range1, range2)
            if r1 == cmp1:
                continue
            else:
                equal = True
                break
        return r1
        
    def GenerateDungeon(self, P):
        
            
        #defined constants
        min_size_room = 5
        max_size_room = 25
        
        # Get starting point for first room or spawning room
        starting_y = random.randint(0, self.height)
        starting_x = random.randint(0, self.width)
        
        #Calculate the size of the room
        starting_height = random.randint(min_size_room, max_size_room)
        starting_width = random.randint(min_size_room, max_size_room)
        
        # Create the first room or known as the spawn room
        self.clear_space(starting_x, starting_y, starting_width, starting_height)

        #Set player position
        pos_y = random.randint(starting_y, starting_y+starting_y)
        pos_x = random.randint(starting_x, starting_x+starting_x)

        P.y = pos_y
        P.x = pos_x

        self.AddNPC(P)
        epos_y = self.GenNCmp(pos_y, starting_y, starting_y+starting_y)
        epos_x = self.GenNCmp(pos_x, starting_x, starting_x+starting_x)

        E = Exit()
        self.AddTile(E, epos_x, epos_y)
            

    def SquareCamera(self, ascii_map, P):
        px = P.x
        py = P.y
        return_map = [[ " " for x in range(0, px)] for y in range(0, py)]

        
        if px == self.width or py == self.height:
            if px == self.width:
                pass
        for y in range(py, py+py):
            ypoint = ascii_map[y]
            for x in range(px, px+px):
                xpoint = ypoint[x]
                return_map[y][x] = xpoint

        return return_map

class Game:
    def __init__(self, h=None, w=None):
        self.h = h
        self.w = w
        
        self.levels = []
        self.current_level = 0
        self.mainplayer = Player("@", 0, 0, 100) # Main player
        self.exit_flag = 0 # 1 = Exit

        
        #Load up with a map
        if h == None and w == None:
            self.levels.append(Map(random.randint(20, 30), random.randint(20, 30)))
        else:
            self.levels.append(Map(self.w, self.h))
        
    def Run(self):
        running = True
        current = True

        #vars
        self.levels[self.current_level].GenerateDungeon(self.mainplayer)
        while running != False:
            current = True
            while current != False:
                self.levels[self.current_level].ReInitializeNpc_map(self.levels[self.current_level].npc)
                ascii_map = self.levels[self.current_level].Convert2Displayable(self.levels[self.current_level].Generate_ascii())
                for u in ascii_map:
                    print u

                i = raw_input(">>")
                self.mainplayer.handle_input(i, self.levels[self.current_level].npc_map, self.levels[self.current_level].tile_map)
                if i == "/Exit":
                    self.exit_flag = 1

                if self.exit_flag == 1:
                    current == False
                    break
            if self.exit_flag == 1:
                running = False
                break
            else:
                self.current_level += 1
            

if __name__ == "__main__":
    G = Game(20, 20)
    G.Run()
    
"""       
if __name__ == "__main__":
    M = Map(50, 50)
    #D = Door()
    #E = Exit()
    #M.AddTile(E, 17, 5)
    P = Player("@", 8, 5, 100)
    M.AddNPC(P)
    #M.AddTile(D, 3, 4)
    M.GenerateDungeon(P)
    npc = [P]

    M.CreateVerticalLine(10, 7, 5)
    M.CreateHorizontalLine(7, 2, 3)
    running = False
    while running != True:
        M.ReInitializeNpc_map(npc)
        dmap = M.Convert2Displayable(M.Generate_ascii())
        for u in dmap:
            print u
        i = raw_input()
        P.handle_input(i, M.npc_map, M.tile_map)
        if i == "/Exit":
            running = True
            
        if running == True:
            break

"""
