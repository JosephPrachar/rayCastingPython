import sys
import commandline
import cast

def main(argv):
    # todo: take comandline input
    args = commandline.process_args(argv)
    # tuple
    # 0: sphere list
    # 1: eye point
    # 2: view info (min_x, max_x, min_y, max_y, width, height)
    # 3: point light
    # 4: ambient color

    # todo: run cast_all_rays with cl input
    with open('image.ppm', 'w') as output_file:
        output_file.write('P3\n' + str(args[2][4]) + ' ' + str(args[2][5]) + '\n255\n')
        #print 'P3\n' + str(args[2][4]) + ' ' + str(args[2][5]) + '\n255'
        cast.cast_all_rays(args[2][0], args[2][1], args[2][2], args[2][3], args[2][4], args[2][5],
                           args[1], args[0], args[4], args[3], output_file)


if __name__ == "__main__":
    main(sys.argv)