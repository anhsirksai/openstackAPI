import os
import time
import novaclient.v1_1.client as nvclient
from credentials import get_nova_creds
from credentials import get_keystone_creds
from prettytable import PrettyTable
import pytz
from datetime import datetime
import keystoneclient.v2_0.client as ksclient
import glanceclient

class imageos(object):
    """docstring for imageos"""
    """def __init__(self, arg):
	super(Calculator, self).__init__()
	self.arg = arg"""

    creds = get_keystone_creds()
    keystone = ksclient.Client(**creds)
    creds1 = get_nova_creds()
    nova = nvclient.Client(**creds1)
		
    def add(self,x,y):
        return x+y

    # Create Image --------------------
    # glance.images.create returns json format details of the added image.
    @classmethod
    def create_image(cls,name):
        """
        Create an image.

        :param image: The name of the image to get.
        :rtype: :json: image details
        """
        glance_endpoint = cls.keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
        glance = glanceclient.Client('1', endpoint=glance_endpoint, token=cls.keystone.auth_token)

        with open('/home/cloud/Downloads/precise-server-cloudimg-amd64-disk1.img', 'rb') as fimage:
            image = glance.images.create(name=name, is_public=True, disk_format="qcow2", container_format="bare", data=fimage)
            return image

    # Delete Image --------------------  
    @classmethod
    def delete_image(cls,i):
        """
        delete an image.

        :param image: The name of the image to get.
        :rtype: NULL
        """
        im = cls.nova.images.find(name=i)     
        im.delete()   
        return
        

    # Get Image List -------------------- 
    @classmethod
    def get_image_list(cls):          
        """
        List images.

        :param image: The name of the image to get.
        :rtype: :dict: image details
        """
        images = cls.nova.images.list(detailed=True)

        image_list = {}
        for v in images:
            image = {}
            image["id"] = v.id
            image["name"] = v.name
            image["status"] = v.status
            image_list[v.name] = image
        return image_list
