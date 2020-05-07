'''
	28/4/2020
	Made by Alejandro Pinel Martínez
    In quarentine
	Tuenti Challenge 10
	Challenge 6 - Knight Labyrinth
'''

# telnet program example
import socket, select, string, sys

def OrderByDistance(m):
    return m.distance

class Movement:
    def __init__(self, nx, ny, dst, lastmove):
        self.x = nx
        self.y = ny
        self.distance = dst
        self.path = []

        if (lastmove <> None):
            for i in lastmove.path:
                self.path.append(i)

        self.path.append([self.x, self.y])

class Knight:
    def __init__(self):
        self._height = 110
        self._width = 110

        self.x = int(self._height/2)
        self.y = int(self._width/2)

        self.princessx = self.x
        self.princessy = self.y + 1

        self.map = [[0 for x in range(self._height)] for y in range(self._width)]
        self.visited = [[0 for x in range(self._height)] for y in range(self._width)]
        self.plan = []

        for i in range (self._height):
            for j in range(self._width):
                self.map[i][j] = '-'
                self.visited[i][j] = False

    def DistanceToPrincess(self, x, y):
        dx = abs(x - self.princessx)
        if (dx > self._height):
            dx = self._height - dx
        dy = abs(y - self.princessy)
        if (dy > self._width):
            dy = self._width - dy
        return dx*dx + dy*dy

    def MakePlan(self):
        for i in range (self._height):
            for j in range(self._width):
                self.visited[i][j] = False

        self.plan = []
        self.plan.append(Movement(self.x, self.y, 0, None))

        selectplan = None
        while (len(self.plan) > 0 and selectplan == None):
            #print len(self.plan)
            nextmove = self.plan[0]
            self.plan.pop(0)

            if (self.map[nextmove.x][nextmove.y] == 'P'):
                selectplan = nextmove.path
            else:
                self.ProccessMovement(nextmove)

        self.plan = selectplan
        print 'A new plan has been calculated'
        print selectplan
        self.plan.pop(0)

    def ProccessMovement(self, move):
        self.visited[move.x][move.y] = True

        px = [-2, -2, -1, -1, 1, 1, 2, 2]
        py = [-1, 1, -2, 2, -2, 2, -1, 1]

        #print "Processing node: " + str(move.x) + " " + str(move.y)

        for i in range(8):
            x = (move.x + px[i]) % self._height
            y = (move.y + py[i]) % self._width
            if self.CellIsValid(x, y) and (self.visited[x][y] == False):
                self.visited[x][y] = True
                nextmove = Movement(x, y, self.DistanceToPrincess(x, y), move)
                self.plan.append(nextmove)
                #print "accepted: " + str(x) + " " + str(y)
            #else:
                #print "not accepted: " + str(x) + " " + str(y)

        self.plan.sort(key=OrderByDistance)

    def FormatSenses(self, senses):
        mapfragment = [[0 for x in range(5)] for y in range(5)]

        for i in range (5):
            for j in range(5):
                mapfragment[i][j] = senses[i*6 + j]

        return mapfragment

    def CellIsValid(self, x, y):
        return x >= 0 and x < self._height and y >= 0 and y < self._width and self.map[x][y] <> '#'

    def AddToMap(self, fragment):
        for i in range (5):
            for j in range(5):
                x = (self.x - 2 + i) % self._height
                y = (self.y - 2 + j) % self._width
                self.map[x][y] = fragment[i][j]

    def LoadMap(self, filename):
        for i in range (self._height):
            for j in range(self._width):
                self.map[i][j] = '-'

        f = open(filename, "r")
        for i in range(self._height):
            line = f.readline()
            for j in range(self._width):
                self.map[i][j] = line[j]

        f.close()

    def WriteMap(self):
        f = open("map.txt", "w")
        for i in range (self._height):
            for j in range(self._width):
                f.write(self.map[i][j])
            f.write('\n')
        f.close()

    def TranslateMov(self, x, y):
        if x > 2:
            x = x - self._height
        elif x < -2:
            x = x + self._height

        if y > 2:
            y = y - self._width
        elif y < -2:
            y = y + self._width

        if (x == -2 and y == -1):
            return '2U1L'
        elif (x == -2 and y == 1):
            return '2U1R'
        elif (x == -1 and y == -2):
            return '1U2L'
        elif (x == -1 and y == 2):
            return '1U2R'
        elif (x == 1 and y == -2):
            return '1D2L'
        elif (x == 1 and y == 2):
            return '1D2R'
        elif (x == 2 and y == -1):
            return '2D1L'
        elif (x == 2 and y == 1):
            return '2D1R'
        else:
            return 'NOMOVE'

    def WorkOnPlan(self):
        while True:
            if self.plan <> [] and len(self.plan) > 0:
                nextpos = self.plan[0]
                self.plan.pop(0)

                if self.CellIsValid(nextpos[0], nextpos[1]):
                    action = self.TranslateMov(nextpos[0] - self.x, nextpos[1] - self.y)
                    self.x = nextpos[0]
                    self.y = nextpos[1]
                    print 'Moved to ' + str(nextpos[0]) + " " + str(nextpos[1]) + " " + action
                    print self.plan
                    return action
                else:
                    self.MakePlan()
            else:
                self.MakePlan()

    def Play(self, vision):
        if (self.x == self.princessx and self.y == self.princessy):
            return 'NOMOVE'
        else:
            self.AddToMap(self.FormatSenses(vision))
            self.WriteMap()

            return self.WorkOnPlan()

#main function
if __name__ == "__main__":
    host = '52.49.91.111'
    port = 2003

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try :
      s.connect((host, port))
    except :
      print 'Unable to connect'
      sys.exit()

    print 'Connected to remote host ' + host + ' : ' + str(port)

    mapfile = "map.txt"
    knight = Knight()
    if (mapfile <> None):
        knight.LoadMap(mapfile)

    princessrescued = False
    while not princessrescued:
        read_sockets, write_sockets, error_sockets = select.select([s] , [], [])
        if (read_sockets <> []) :
            data = s.recv(4096)
            if not data :
                print 'Connection closed'
                sys.exit()

            sys.stdout.write(data)
            msg = knight.Play(data)
            if (msg == 'NOMOVE'):
                princessrescued = True
            else:
                s.send(msg)


    print 'End of the algorithm, manual control now'

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print 'Connection closed'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)

            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg)
