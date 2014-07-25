Table

:name: saikrishna
:Topic: openstack notes

.. contents:: **Table of contents**

.. sectnum::
   :suffix: .
   
   
   
Installation
============
devstack - clone - ./stack.sh

working with the commands
=========================
+ For openstack commands to work , when installed with devstack:
+ source openrc admin admin
+ source openrc demo demo

Get the cloud image
===================

+ `images`_  Chapter 2. Get images
.. _`images`: http://docs.openstack.org/image-guide/content/ch_obtaining_images.html

Launching a VM
==============
+ add a ssh key to vm:
   - Do this on my local machene : ssh-keygen -t rsa -f OPenstack_MAchine
   - copy the key to dashboard while creating if it is being done from dashboard.

+ add a image to openstack: glance image-create --name ubuntu_qcow --disk-format qcow2 --container-format bare --file /home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img 
+ boot a vm from nova:  nova boot --flavor 2 --key_name OPenstack_MAchine --image dd47f229-5769-4265-96bf-f085282f77fb myinstance
+ once instance is **Active** in nova-list, login with ssh -i cloud.key.pub ubuntu@10.0.0.3

Working with the python api's
=============================
+ In credentials.py 
  -  file:: 
     #!/usr/bin/env python
     import os
     def get_keystone_creds():
         d = {}
         d['username'] = os.environ['OS_USERNAME']
         d['password'] = os.environ['OS_PASSWORD']
         d['auth_url'] = os.environ['OS_AUTH_URL']
         d['tenant_name'] = os.environ['OS_TENANT_NAME']
         return d
     def get_nova_creds():
         d = {}
         d['username'] = os.environ['OS_USERNAME']
         d['api_key'] = os.environ['OS_PASSWORD']
         d['auth_url'] = os.environ['OS_AUTH_URL']
         d['project_id'] = os.environ['OS_TENANT_NAME']
         return d
    
+  This file should be in devstack/ directory.
+  Once this is written and saved,
   -  do source openrc admin admin
+  Using openstack python bindings:
   - Example1::
     from novaclient import client as novaclient
     from credentials import get_nova_creds
     creds = get_nova_creds()
     nova = novaclient.Client("1.1", **creds)
     
+    This will show the list of servers on openstack.::
       - nova.servers.list()
       - nova.image.list()
       - nova.flavor.list()

Creating an instance with python bindings:
==========================================

+  Using openstack python bindings to create a VM:
   - Example2::
     import os
     import time
     from novaclient import client as nvclient
     from credentials import get_nova_creds
     creds = get_nova_creds()
     nova = nvclient.Client("1.1",**creds)
     if not nova.keypairs.findall(name="mykey"):
         with open(os.path.expanduser('~/.ssh/cloud.key.pub')) as fpubkey:
             nova.keypairs.create(name="mykey", public_key=fpubkey.read())
     image = nova.images.find(name="ubuntu_qcow")
     flavor = nova.flavors.find(name="m1.small")
     instance = nova.servers.create(name="test", image=image, flavor=flavor, key_name="mykey")
     # Poll at 5 second intervals, until the status is no longer 'BUILD'
     status = instance.status
     while status == 'BUILD':
         time.sleep(5)
         # Retrieve the instance again so the status field updates
         instance = nova.servers.get(instance.id)
         status = instance.status
     print "status: %s" % status
