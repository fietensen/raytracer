class Scene:
    def __init__(self, objects, camera, light, width, height, AA):
        self.objects = objects
        self.camera = camera
        self.light = light
        self.width = width
        self.height = height
        self.AA = AA
