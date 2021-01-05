from math import sqrt

class Axial:
    def __init__(self, q, r):
        self.q, self.r = q, r
        self.s = - q - r
        self.coords = (self.q, self.r)
    
    def cartesian(self, size, center):
        x = ((self.q * sqrt(3)) + (self.r * (sqrt(3)/2))) * size
        y = (self.r * (3/2)) * size
        return (round(x + center[0]), round(y + center[1]))

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
