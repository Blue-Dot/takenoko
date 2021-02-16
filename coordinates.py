from math import sqrt

#NOTE these coordinates are for hexagons/tiles. Ie. q + r + s = 0. They are not for rivers

# --> = q coordinate

# \ 
#  \  = r coordinate
#   v

class Axial:
    def __init__(self, q, r):
        #q corresponds to x, r corresponds to z, s corresponds to y
        self.q, self.r = q, r
        self.s = - q - r
        self.coords = (self.q, self.r)
    
    def cartesian(self, size, center):
        x = ((self.q * sqrt(3)) + (self.r * (sqrt(3)/2))) * size
        y = (self.r * (3/2)) * size
        return (round(x + center[0]), round(y + center[1]))

    def sum(self, a): #Sum two axial coordinates together
        q = self.q + a.q
        r = self.r + a.r
        return Axial(q, r)
    
    def get_coords(self):
        return self.coords

class Cartesian(Axial): #Primarily for mouse... TESTED - works!
    def __init__(self, x, y, size, center):
        #Makes x and y relative to the center
        x = x - center[0]
        y = y - center[1]

        #Converts x and y to q, r and s
        q = (sqrt(3)/3 * x  -  1/3 * y) / size
        r = (2/3 * y) / size
        s = -q-r

        q, r, s = self.cube_round(q, r, s) #Rounds to the nearest hexagon where q + r + s = 0
        super().__init__(q, r)

    def cube_round(self, x, y, z): #CREDIT: 'https://www.redblobgames.com/grids/hexagons/#pixel-to-hex'
        rx = round(x)
        ry = round(y)
        rz = round(z)

        x_diff = abs(rx - x)
        y_diff = abs(ry - y)
        z_diff = abs(rz - z)

        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry-rz
        elif y_diff > z_diff:
            ry = -rx-rz
        else:
            rz = -rx-ry
        
        return rx, ry, rz

# ~ RIVER COORDINATES ~
# Ie. q + r + s != 0

class Cubic:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def sum(self, a):
        x = self.x + a.x
        y = self.y + a.y
        z = self.z + a.z
        return Cubic(x, y, z)

    def difference(self, a):
        '''Calculate the difference between two cubic coordinates (ie the vector between them). Returns a Cubic object'''
        x = abs(self.x - a.x)
        y = abs(self.y - a.y)
        z = abs(self.z - a.z)
        return Cubic(x, y, z)

    def cartesian(self, size, center):
        '''Returns the cartesian form of this object''' 
        cart_x = ((sqrt(3) / 2) * (self.x - self.y)) * size
        cart_y = ((1/2) * (- self.x - self.y) + self.z) * size
        return (round(cart_x + center[0]), round(cart_y + center[1]))

    def coords(self):
        return (self.x, self.y, self.z)

    def get_coords(self): #Alias for self.coords
        return self.coords()

    def axial(self):
        if self.x + self.y + self.z == 0:
            return Axial(self.x, self.z)
        raise Exception("Silly Max, you attempted to turn a Cubic object into an Axial object where x + y + z != 0")

#TESTING:
'''
a = Axial(0, 0)
c = Axial(1, 1)
b = a.sum(c)
print(c.q, c.r, c.s)
print(b.q, b.r, b.s)

#axial.sum(a) works :)

a = Cubic(1, 0, 1)
b = Cubic(1, 0, 0)
c = a.difference(b)
d = b.difference(a)
print(c.coords()) #Works :))
print(d.coords())
#These are the same (0, 0, 1) which means it works :)) yipee!
'''