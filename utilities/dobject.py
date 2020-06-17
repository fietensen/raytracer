from utilities import vector, intersections, lighteffects

class dObject:
    def __init__(self, obj_id=None, extra=None, position=vector.Vec3(.0, .0, .0), style=None, obj_type=None, radius=None, color=None, material=None, plane_point=vector.Vec3(.0, .0, .0), effects=None):
        self.ID       = obj_id
        self.position = position
        self.obj_type = obj_type
        self.radius   = radius
        self.material = material
        self.color    = color
        self.plane_point = plane_point
        self.effects     = effects
        self.style = style
        self.extra = extra if extra != None else {}

        if obj_type == "Plane":
            if type(self.color) == list and lighteffects.effects["planestyle-chess"][0] not in self.effects:
                self.color = self.color[0]
    def intersects(self, ray):
        if self.obj_type == "Sphere":
            return intersections.Sphere(self, ray)
        elif self.obj_type == "Plane":
            return intersections.Plane(self, ray)
