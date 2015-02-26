import sys
import commandline
import cast
import datetime

def main(argv):
    args = commandline.process_args(argv)
    # tuple
    # 0: sphere list
    # 1: eye point
    # 2: view info (min_x, max_x, min_y, max_y, width, height)
    # 3: point light
    # 4: ambient color

    start = datetime.datetime.now()

    with open('image.ppm', 'w') as output_file:
        output_file.write('P3\n' + str(args[2][4]) + ' ' + str(args[2][5]) + '\n255\n')

        cast.cast_all_rays(args[2][0], args[2][1], args[2][2], args[2][3], args[2][4], args[2][5],
                           args[1], args[0], args[4], args[3], output_file)

    end = datetime.datetime.now()
    delta = end - start
    print 'Time: ', str(delta)



if __name__ == "__main__":
    main(sys.argv)