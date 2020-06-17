# raytracer
### An experimental raytracer written in Python(3)

I created this raytracer on a weekend because I just saw someone talking about raytracing. That got me interested.

Big thanks to [Arun Ravindran](https://www.youtube.com/channel/UCj7bqdW_FLpzUIzlSbXLp_A) and [James Bowman](https://github.com/jamesbowman) for demonstrating formulas and vector/ray maths.

![alt text](https://i.imgur.com/MWXSCeo.png "The example model included in the Repository")

The usage is pretty simple...
`python3 raytrace.py [name of model file]`
the contents of the model.json are pretty straight forward:
Project: the name of the output file
fileformat: (not required) if fileformat is not specified, it's defaulting to ppm. Any other fileformats than ppm require the Pillow library

resolution: output resolution / antialiasing (AA only works with Pillow installed)
objects: contains all objects in the scene, it's type, the coordinates and specific information like sphere-radius. dX/Y/Z coords for the Plane set the rotation of the plane. Also, the Planes color can be a list if the effect planestyle-chess is used.

then there are only camera and light left, camera being the point the viewer is looking from and light the source of light


example_models includes some extra models:

![alt text](https://i.imgur.com/nhujUx0.png "chessuniverse.json")
