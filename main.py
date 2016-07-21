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
    def __init__(self, ascii, x, y):
        self.ascii = ascii
        self.x = x
        self.y = y

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

class Player(NPC):
    def __init__(self, ascii, x, y):
        NPC.__init__(self, ascii, x, y)

    def handle_input(self, i, nmap, tmap):
        i = i.upper()
        if i == "N":
            self.Move(0, 1, nmap, tmap)
        elif i == "S":
            self.Move(0, -1, nmap, tmap)
    
        

class Map:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.tile_map = [[ Wall() for x in range(0, self.width)] for y in range(0, self.height)]
        self.npc_map = [[ None for x in range(0, self.width)] for y in range(0, self.height)]

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

    

if __name__ == "__main__":
    M = Map(20, 20)
    #D = Door()
    P = Player("@", 8, 5)
    M.AddNPC(P)
    #M.AddTile(D, 3, 4)
    M.clear_space(5, 5, 5, 5)
    

    running = False
    while running != True:
        dmap = M.Convert2Displayable(M.Generate_ascii())
        for u in dmap:
            print u
        i = raw_input()
        P.handle_input(i, M.npc_map, M.tile_map)
        if i == "/Exit":
            running = True
            
        if running == True:
            break

