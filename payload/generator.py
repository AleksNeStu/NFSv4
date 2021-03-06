#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""The test data generator for testing NFSv4 and ACLs (run via call functions)

@Developed by AleksNeStu

"""

import random    #Random variable generators
import commands	 #Execute shell commands via os.popen() and return status, output
import re		 #Support for regular expressions (RE)

class full_generator(object):


#Generate range for groups (group names, gid (7000 + g range) according input data "g - number of groups"
#GID - values between 0 and 999 are typically reserved for system accounts
	def create_groups_n(self, g):
		for i in range(1,g+1):
			gname = "nfs_group" + str(i)
			gid = str(7000 + i)
			self.create_groups(gname, gid)

#Generate groups according the data from "create_groups_n" [consistently in range]
#groupadd -f -g 7000(range) nfs_group(range)
# -f - force	-g GID
	def create_groups(self, gname, gid):
		cmd = commands.getoutput("groupadd -f -g " + gid + " " + gname)
		print "    Group: " + gname + " / GID: " + gid + " / has been created"
		if cmd != "":
			print "    Group: " + gname + " / GID: " + gid + " / with errors"

#Generate range for users (user names, uid (7000 + g range) according input data "u - number of users"
#UID - values between 0 and 999 are typically reserved for system accounts
	def create_users_n(self, u):
		for i in range(1,u+1):
			uname = "nfs_user" + str(i)
			uid = str(7000 + i)
			self.create_users(uname, uid)

#Generate users according the data from "create_users_n" [random group select]
#useradd -f -g 7000(range) nfs_group(range)
#UID The numerical value of the user's ID.
#useradd -g "random_from_exist" -m uname -u uid -p nfs
#-g - the group name for a new user's initial group
#-m - create the user's home directory and new user name
#-u - UID
#-p - the encrypted password
 	def create_users(self, uname, uid):
		rgname = self.groups_list[random.randint(0, len(self.groups_list) - 1)][0]  #random select from  the previous created groups
		cmd = commands.getoutput("useradd " + "-g " + rgname + " -p nfs" + " -m " + uname + " -u " + uid)
		print "    User: " + uname + " / UID: " + uid + " / GID: " + rgname + " / has been created"
		if cmd != "":
			print "    User: " + uname + " / UID: " + uid + " / GID: " + rgname + " / with errors"

# List of groups
	groups_list = []  # empty list of groups for start
	groups_list_len = len(groups_list)
# List of files
	users_list = []  # empty list of users for start
	users_list_len = len(users_list)

########################Get list of groups created for testing############################
	def get_groups(self):
		fin = open("/etc/group", "r")
		strs = fin.readlines()
		for str in strs:
			splitedline = str.split(":")
			gname = splitedline[0]
			gid = splitedline[2]
			name_true = re.match("nfs_group", gname)
			if name_true != None:
				self.groups_list.append([gname, gid])
		fin.close()

	def get_groups_n(self, gg):
		fin = open("/etc/group","r")
		strs = fin.readlines()
		n = 0
		for str in strs:
			splitedline = str.split(':')
			gname = splitedline[0]
			gid = splitedline[2]
			name_true = re.match("nfs_group", gname)
			if name_true != None:
				self.groups_list.append([gname, gid])
				n = n + 1
			if n == gg:
				break
		fin.close()

########################Get list of users created for testing############################
#Get the list of all users from file /etc/passwd
	def get_users(self):
		f = open("/etc/passwd", "r")
		strs = f.readlines()
		for str in strs:
			splitedline = str.split(":")
			uname = splitedline[0]
			gid = splitedline[3]
			name_true = re.match("nfs_user", uname)			#nfs_userxxx - created by generator
			if name_true != None:
				self.users_list.append(uname)
		f.close()

	def get_users_n(self, gu):
		f = open("/etc/passwd", "r")
		strs = f.readlines()
		n = 0
		for str in strs:
			splitedline = str.split(":")
			uname = splitedline[0]
			gid = splitedline[3]
			name_true = re.match("nfs_user", uname)			#nfs_userxxx - created by generator
			if name_true != None:
				self.users_list.append(uname)
				n = n + 1
			if n == gu:
				break
		f.close()