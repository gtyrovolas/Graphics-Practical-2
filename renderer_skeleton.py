from PIL import Image
import math

from helpers import *

#
#   Renderables
#

class Renderable:
    # Should return a RayIntersection for the intersection between
    # the ray from origin with direction
    def intersect(self, origin, direction): pass

    # Should return the normal at the given location
    def normal(self, location): pass

class Sphere(Renderable):
    def __init__(self, origin, radius):
        self.origin = origin
        self.radius = radius

    # origin (vec3) represents the start of the ray
    # direction (vec3) represents the direction of the ray
    #
    # should return a RayIntersection representing the point where
    # the input ray intersects the sphere
    def intersect(self, origin, direction):
        #
        # ! implement this
        #
        
        return RayIntersection(origin, direction, self, intersection, ray_length)

    # location (vec3) is a point on the sphere
    # 
    # should return a vec3 representing the normal at that point
    def normal(self, location):
        #
        # ! implement this
        #
        
        return normal

#
#   Lights
#

class Light:
    def __init__(self, pos, colour=None):
        self.position = pos
        self.colour = colour if colour else vec3(1)

    # return the colour of renderable at location according to 
    # renderer's camera
    def illumination(self, renderable, location, renderer):
        return self.colour

class PhongLight(Light):
    def __init__(self, pos, specular=None, diffuse=None):
        self.position = pos
        self.specular = specular if specular else vec3(1)
        self.diffuse = diffuse if diffuse else vec3(1)

    # renderable (Renderable) is the object being lit
    # location (vec3) is the point on the object
    # renderer (Renderer) is a reference to the renderer
    #
    # should return a vec3 (red, green, blue) of the colour
    # and brightness that the point is illuminated to by
    # this light (each colour channel should be 0-1)
    def illumination(self, renderable, location, renderer):
        #
        # ! implement this
        #
        
        return vec3(0,1,0)

#
#   Renderer
#

class Renderer:
    def __init__(self):
        self.camera = vec3(0,0,0)
        self.lights = []
        self.renderables = []

    # origin (vec3) and direction (vec3) describe the ray
    # exclude (list) is a list of renderables to ignore
    #
    # returns the nearest intersection between the ray
    # and any renderables
    def raycast(self, origin, direction, exclude=None):
        if not exclude: exclude = []

        d_norm = direction.norm()
        intersections = [
            r.intersect(origin, d_norm)
            for r in self.renderables
            if r not in exclude
        ]
        intersections = [r for r in intersections if r]
        if not intersections: return False
        return min(intersections, key=lambda x:x.length)

    # ray_intersection (RayIntersection) is an intersection
    #
    # should return the colour (vec3) at that intersection
    def get_lighting(self, ray_intersection):
        output = vec3(0)

        for light in self.lights:
            output += light.illumination(ray_intersection.renderable, ray_intersection.location, self)

        return output / len(self.lights)

    # x (int), y (int), screen coordinates
    # width (int), height (int), screen size
    #
    # should return the colour of the pixel at
    # x,y on a screen of width x height
    def render(self, x, y, width, height):
        result = self.raycast(
            self.camera,
            vec3(
                x/width - 0.5,
                y/height - 0.5,
                1
            )
        )

        if result:
            lighting = self.get_lighting(result)
            return (int(lighting.x*255),int(lighting.y*255),int(lighting.z*255))
        else:
            return (255,255,255)   

if __name__ == '__main__':
    #
    #   Scene is described here
    #

    width = 2**7
    height = 2**7

    img = Image.new( 'RGB', (width,height), "black")
    pixels = img.load()

    renderer = Renderer()
    renderer.lights = [
        PhongLight(vec3(0.5,-1,3.5), vec3(0,0,1), vec3(0,0,1))
    ]
    renderer.renderables = [
        # ! add some renderables here
    ]

    for i in range(img.size[0]):
        print(f"Rendering column ({i}/{img.size[0]})")
        for j in range(img.size[1]):
            pixels[i,j] = renderer.render(i,j,width,height)

    img.save('output.png')