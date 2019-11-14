# 370A3
psql assignment 

# CONFIG FILE
Input your credentials to log into your database, the config file has hints, just replace the hints with you information.

# GETTING THE FILES TO THE LINUX SERVERS
make sure all the files from github are in a single folder then execute the following command in the directory with the folder:
scp -r FOLDERNAME NETLINK_ID@linux.csc.uvic.ca:/home/NETLINK_ID

if this is your first time type yes and then enter your netlinkid password
# BUILDING DATABASE AND LOADING FROM CSV
when you are in: cd FOLDERNAME
then type: python3 db_setup.py
make sure you updated the config file with your information. 

to build the database hit press b once then hit enter.
Then hit 1 enter then 6 enter. You should be able to access the student database that has our tables. 

you can now practice sql queries on your student. 

# NOTE
if you use mockaroo you will notice they will add a header line above the data, when i wrote the program i didn't account for this for so make sure to remove the first line if you want to use files from mockaroo.

the other functions in the program are not needed for practicing but if you want i will have information on how to run them soon.
