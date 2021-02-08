from math import sqrt

#NOTE these coordinates are for hexagons/tiles. Ie. q + r + s = 0. They are not for rivers

'''
--> = q coordinate
\ 
 \  = r coordinate
  v
'''


class Axial:
    def __init__(self, q, r):
        self.q, self.r = q, r
        #self.s = - q - r
        self.coords = (self.q, self.r)
    
    def cartesian(self, size, center):
        x = ((self.q * sqrt(3)) + (self.r * (sqrt(3)/2))) * size
        y = (self.r * (3/2)) * size
        return (round(x + center[0]), round(y + center[1]))

    def sum(self, a): #Sum two axial coordinates together
        q = self.q + a.q
        r = self.r + a.r
        return Axial(q, r)

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

#TESTING:
'''
a = Axial(0, 0)
c = Axial(1, 1)
b = a.sum(c)
print(c.q, c.r, c.s)
print(b.q, b.r, b.s)
'''
#axial.sum(a) works :)

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

    def cartesian(self, size, center):
        '''Returns the cartesian form of this object''' 
        cart_x = ((sqrt(3) / 2) * (self.x - self.y)) * size
        cart_y = ((1/2) * (- self.x - self.y) + self.z) * size
        return (round(cart_x + center[0]), round(cart_y + center[1]))
