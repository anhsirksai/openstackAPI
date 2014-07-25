import unittest
from imagescript import imageos
#import script as adapter

class TddInPython(unittest.TestCase):
    def test_get_image_list(self):
        adapter = imageos()
        prev_image_list = adapter.get_image_list()
        assert("test" not in prev_image_list)
        print prev_image_list
        print ("\n")
        image = adapter.create_image("test")
        print ("\n")
        cur_image_list = adapter.get_image_list()
        assert(image.name in cur_image_list)
        print cur_image_list
        print ("\n")
        #adapter.delete_image("test")
        new_image_list = adapter.get_image_list()
        assert("test" not in new_image_list)
        print ("\n")
        print "get_image_list() function passed"
    



"""def test_create_image():
    pass

def test_create_vm():
    pass

def test_start_vm():
    pass

def test_resume_vm():
    pass

def test_stop_vm():
    pass

def test_destroy_vm():
    pass

def test_reconfigure_vm():
    pass


def main():
    test_get_image_list() 

if __name__ == '__main__':
    main() """
    