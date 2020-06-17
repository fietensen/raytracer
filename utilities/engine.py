from utilities import image, ray, vector, color

class RenderEngine:
    def __init__(self):
        pass
    def render(self, scene):
        width = scene.width
        height = scene.height
        aspect_ratio = float(width) / height
        x0 = -1.0
        x1 = 1.0
        xstep = (x1-x0) / (width-1)
        y0 = -1.0 / aspect_ratio
        y1 = 1.0 / aspect_ratio
        ystep = (y1 - y0) / (height-1)

        camera = scene.camera
        pixels = image.Image(width, height)
        lastpercent = .0

        for i in range(height):
            y = y0+i*ystep
            for j in range(width):
                x = x0+j*xstep
                r = ray.Ray(camera, vector.Vec3(x,y)-camera)
                pixels.set_pixel(j,i, self.ray_trace(r, scene))
            if (float((i+1)*100) / float(height)) != lastpercent:
                lastpercent = float((i+1)*100) / float(height)
                print("Rendered %.4f%%" % lastpercent)
        return pixels
    def ray_trace(self, r, scene):
        color_ = color.Color(.0,.0,.0)
        dist_hit, obj_hit = self.find_nearest(r, scene)
        if obj_hit is None:
            return color_
        hit_pos = r.origin + r.direction * dist_hit
        color_ += self.color_at(obj_hit, hit_pos, scene)
        return color_
    def find_nearest(self, r, scene, exclude=None):
        dist_min = None
        obj_hit = None
        for obj in scene.objects:
            if not obj == exclude:
                dist = obj.intersects(r)
                if dist is not None and (obj_hit is None or dist < dist_min):
                    dist_min = dist
                    obj_hit = obj
        return (dist_min, obj_hit)
    
    def color_at(self, obj_hit, hit_pos, scene):
        color_ = obj_hit.color
        for effect in obj_hit.effects:
            color_ = effect(self, color_, hit_pos, obj_hit, scene)
        return color_
