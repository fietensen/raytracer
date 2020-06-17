from utilities import color

class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[None for _ in range(width)] for _ in range(height)]
    def set_pixel(self, x, y, color_):
        def to_byte(nval):
            return round(max(min(nval*255, 255), 0))
        self.pixels[y][x] = color.Color(to_byte(color_.x), to_byte(color_.y), to_byte(color_.z))
    def save(self, name):
        with open(name, "w") as fp:
            fp.write("P3 %d %d\n255\n" % (self.width, self.height))
            for row in self.pixels:
                for pnum, pixel in enumerate(row):
                    fp.write("%d\t%d\t%d" % (pixel.x, pixel.y, pixel.z))
                    fp.write("\t\t" if pnum < len(row)-1 else "")
                fp.write("\n")
    def getdata(self):
        pixels = []
        for row in self.pixels:
            for pixel in row:
                pixels.append((int(pixel.x), int(pixel.y), int(pixel.z)))
        return pixels
