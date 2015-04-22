import re


def read_cameras(filename):
    """Read a text file as list of camera names and create a list"""
    f = file(filename, mode='r')
    camera_list = [name.strip() for name in f.readlines()]
    return camera_list


def map_cameras(camera_set):
    """Maps a set of data to a cleaned data set by prompting user"""

    camera_map = dict()
    camera_vv = set()

    while camera_set:
        ## First prompt user to create a new valid camera, not a camera, or view list.
        camera_name = camera_set.pop()
        while True:
            print "Cameras left to map:", len(camera_set)
            print("Camera name: '%s'" % (camera_name, ))
            prompt = raw_input("Type a new camera name or [ENTER] to use '%s'\nOR choose from existing list (l)\nOR not a camera (n)\n" % (camera_name, ))

            if prompt == 'l':
                if camera_vv:
                    for vv in camera_vv:
                        print vv
                    vv_cname = raw_input("Which camera name should '%s' be assigned to? (enter to cancel) " % (camera_name, ))
                    if vv_cname in camera_vv:
                        camera_map.setdefault(camera_name, vv_cname)
                        print "Mapped: {'%s': '%s'}" % (camera_name, vv_cname)
                        break
                    else:
                        print "No value mapped"
                        pass
                else:
                    print "No valid camera names exist yet. Please create one."
                    pass

            elif prompt == 'n':
                print "%s not a camera name" % (camera_name, )
                break

            else:
                if not prompt:
                    new_name = camera_name
                else:
                    new_name = prompt
                camera_vv.add(new_name)
                camera_map.setdefault(camera_name, new_name)
                print "Mapped: {'%s': '%s'}" % (camera_name, new_name)

                # Attempt to map others to new name & verify.
                map_new_name(camera_name, new_name, camera_set, camera_map)

                break

    return camera_map


def map_new_name(old_name, new_name, camera_set, camera_map):
    """Prompt user to verify possible matches"""
    print "Let's see if '%s' matches anythign else in the list" % (new_name, )

    camera_list = list(camera_set)  # so we can pop off the set w/o altering loop
    for camera in camera_list:
        # strip out any white space or non-alphanumeric chars in both old name
        # and new name to see if any other cameras look the same.
        if re.sub(r'[^a-zA-Z0-9]', '', old_name).lower() in camera.lower() or \
                re.sub(r'[^a-zA-Z0-9]', '', new_name).lower() in camera.lower() or \
                camera.lower() in re.sub(r'[^a-zA-Z0-9]', '', old_name).lower() or \
                camera.lower() in re.sub(r'[^a-zA-Z0-9]', '', new_name).lower():
            # allow user to verify if it is a match or not
            prompt = raw_input("Does '%s' match '%s'? (y/n): " % (camera, new_name))
            if prompt == 'y':
                camera_set.discard(camera)
                camera_map.setdefault(camera, new_name)
                print "Mapped: {'%s': '%s'}" % (camera, new_name)
    print "... end of list"
    print "---------------"


if __name__ == '__main__':
    ## Read in file and get a list of distinct names
    camera_list = read_cameras('camera_list.txt')
    camera_set = set(camera_list)
    ## Map the cameras with input from user
    camera_map = map_cameras(camera_set)
    while True:
        print_or_save = raw_input("Print or Save mapping? (p/s)")
        if print_or_save == 'p':
            print camera_map
            break
        if print_or_save == 's':
            f = file('camera_map.txt', 'w')
            f.write(str(camera_map))
            f.close()
            print "Mapping written to file 'camera_map.txt'"
