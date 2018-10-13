#!/bin/bash/python

from fabric.api import *
from fabric.context_managers import cd

env.hosts = ['ubuntu_server_ip_address']
env.user = 'ubuntu' # default is the local user
env.password = 'ubuntu' # can be used both for SSH authentication and sudo


@task
def local_info():
        sudo('uname -a')

@task
def create():
		env.warn_only = True
		condition = ""
		while condition != "NO":
			print("\n\n-------------  Creating user on remote machine -------------:\n")
			username = prompt("Enter the Username to create:")
			print(username)
			try:
				sudo("adduser %s" %username)
				print("\n---------------user created----------------\n")
			except:
				pass
			with cd("/home/%s" %username):
				sudo("mkdir .ssh")
				sudo("ssh-keygen -f %s -t rsa -N '' " %username)

				print("\n------------- Keys created  -------------\n")
				print("\n---------------------------\n")
				sudo("pwd")
				sudo("chmod -R 700 .ssh")
				sudo("cat %s.pub >> .ssh/authorized_keys" %username)
				sudo("chmod 600 .ssh/authorized_keys")
				sudo("pwd")
				sudo("chown %s .ssh/" %username)
				sudo("pwd")
				sudo("chmod 600 %s.pub" %username)

			condition = prompt("Do you want to create another user (Y/n):")
			if condition == "N" or condition == "n" or condition == "no" or condition == "No":
				break
			else:
				continue

@task
def download():
	print("\n------------------------------\n")
	print("\n---------username that you want to get keys----------:\n")
	username=prompt("Enter the username:")
	get("home/%s/%s.pub" % (username, username) , "~/desktop")
	


@task
def do_all():
	local_info()
	create()
	download()
	

