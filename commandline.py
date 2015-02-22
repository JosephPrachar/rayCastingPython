import data
import sys

def process_args(args):
    if (len(args) == 1):
        print >> sys.stderr, "no input file specified"
        exit(1)
    spheres = input_spheres(args[1])
    eye_point = data.Point(0.0,0.0,-14.0)
    view = (-10, 10, -7.5, 7.5, 1024, 768)
    point_light = data.Light(data.Point(-100.0, 100.0, -100.0), data.Color(1.5, 1.5, 1.5))
    ambient = data.Color(1.0, 1.0, 1.0)

    index = 2
    while index < len(args):
        if args[index][0] == '-':
            index += 1
            if args[index - 1] == '-eye':
                eye_point = process_point(args[index:index+3], eye_point)
                index += 2
                pass
            elif args[index - 1] == '-view':
                view = process_view(args[index:index+6], view)
                index += 5
                pass
            elif args[index - 1] == '-light':
                point_light = process_light(args[index:index + 6], point_light)
                index += 5
                pass
            elif args[index - 1] == '-ambient':
                ambient = process_color(args[index:index + 3], ambient)
                index += 2
                pass
        else:
            index += 1

    return spheres, eye_point, view, point_light, ambient

def process_point(nums, default):
    try:
        return data.Point(float(nums[0]), float(nums[1]), float(nums[2]))
    except:
        print >> sys.stderr, "Problem with input point, reverting to default value"
        return default

def process_color(nums, default):
    try:
        return data.Color(float(nums[0]), float(nums[1]), float(nums[2]))
    except:
        print >> sys.stderr, "Problem with input color, reverting to default value"
        return default

def process_light(nums, default):
    return data.Light(process_point(nums[0:3], default.pt), process_color(nums[3:6], default.color))

def process_view(nums, default):
    try:
        return float(nums[0]), float(nums[1]), float(nums[2]), float(nums[3]), int(nums[4]), int(nums[5])
    except:
        print >> sys.stderr, "Problem with input view settings, reverting to default value"
        print >> sys.stderr, nums
        return default

def input_spheres(file_name):
    spheres = []
    with open_file(file_name) as f:
        count = 0
        for line in f:
            count += 1 # gives a 1 based index instead of 0 based
            try:
                strs = line.split(' ')
                if len(strs) == 11:
                    n = [float(a) for a in strs]
                    spheres.append(data.Sphere(data.Point(n[0], n[1], n[2]), n[3],
                                   data.Color(n[4], n[5], n[6]),
                                   data.Finish(n[7], n[8], n[9], n[10])))
                else:
                    print >> sys.stderr, "malformed sphere on line ", str(count) + " ... skipping"
            except:
                print >> sys.stderr, "malformed sphere on line ", str(count) + " ... skipping"
    return spheres



def open_file(file_name):
    try:
        return open(file_name, 'rb')
    except:
        print >> sys.stderr, "incorrect input file"
        exit(1)
