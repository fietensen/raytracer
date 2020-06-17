import math

class Vec3:
    def __init__(self, x=.0, y=.0, z=.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        
    def __str__(self):
        return "Vector(%.4f, %.4f, %.4f)" % (self.x, self.y, self.z)

    def __add__(self, vec):
        return Vec3(self.x+vec.x, self.y+vec.y, self.z+vec.z)

    def __sub__(self, vec):
        return Vec3(self.x-vec.x, self.y-vec.y, self.z-vec.z)

    def __mul__(self, num):
        return Vec3(self.x*num, self.y*num, self.z*num)

    def __rmul__(self, num):
        return self.__mul__(num)
    
    def __truediv__(self, num):
        return Vec3(self.x/num, self.y/num, self.z/num)

    def dotproduct(self, vec):
        return self.x*vec.x + self.y*vec.y + self.z*vec.z

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        return self/self.magnitude()
