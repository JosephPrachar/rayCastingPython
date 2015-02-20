import data
import cast

def main():
    # create scene
    eye = data.Point(0.0, 0.0, -14.0)
    spheres = [data.Sphere(data.Point(.5, 1.5, -3.0), 0.5, data.Color(1, 0, 0), data.Finish(.4, .4, .5, .05)),
               data.Sphere(data.Point(1.0, 1.0, 0.0), 2.0, data.Color(0, 0, 1), data.Finish(.2, .4, .5, .05))]
    ambientColor = data.Color(1.0,1.0,1.0)
    pointLight = data.Light(data.Point(-100.0, 100.0, -100.0), data.Color(1.5,1.5,1.5))

    # easy scaling of final image size
    scale = 1
    width = 1024 / scale
    height = 768 / scale

    # ppm p3 header
    print "P3"
    print width, " ", height
    print 255

    cast.cast_all_rays(-10, 10, -7.5, 7.5, width, height, eye, spheres, ambientColor, pointLight)

if __name__ == "__main__":
    main()