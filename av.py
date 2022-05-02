import hashlib
import argparse
import os
import yaml
from urllib.request import urlopen
from urllib.error import HTTPError
from socket import create_connection
from os.path import isfile
from sys import exit


# Setup argparse
parser = argparse.ArgumentParser(
    description="Scan a specified path for viruses.")
parser.add_argument('-p', '--path', required=True, type=str,
                    help="Path to scan for viruses.")
args = parser.parse_args()


# Initialize all variables and stuff so they are global
infected_files = []
infected_hashes = []
fhashlist = []
vhashlist = []
file_dict = {}
config_dict = {}


# Load config.yml into config_dict
def loadConfig():
    global config_dict
    with open('config.yml', 'r') as config:
        config_dict = yaml.load(config, Loader=yaml.FullLoader)


# Check in config if the hash list is up to date
def hashUpdater():
    local_version = config_dict["virusshare_version"]
    print("Checking if Database of virus hashes is up to date.")

    # Check for an Internet connection
    try:
        create_connection(("www.github.com", 443))
    except OSError:
        print("Couldn't check & update Database. Please connect to the Internet.")

    # Check if local Database is up to date
    with open("virushashes.txt", "a") as f:
        try_version = local_version + 1
        while True:
            url = "https://virusshare.com/hashfiles/VirusShare_{}.md5".format(
                str(try_version).zfill(5))
            try:
                with urlopen(url) as response:
                    f.write("\n".join(
                        str(response.read()).strip("b'").split("\\n")[6:]
                    ))
                    print("Downloaded {} and added to local Database.".format(url))
                    try_version = try_version +1
            
            except HTTPError as e:
                # Check if a 404 was received which means Database is up to date
                if e.code == 404:
                    print("Database up to date.")

                    # Put the number of the ltest version in config.yml
                    local_version = try_version - 1
                    data = dict(
                        virusshare_version = local_version
                    )
                    with open('config.yml', 'w') as f:
                        yaml.dump(data, f, default_flow_style=False)

                    break



# Load all files in path and calculate MD5 hashes
def loadFiles():
    global file_dict
    global fhashlist
    for path, currentDirectory, files in os.walk(args.path):
        for f in files:
            file = os.path.join(path, f)
            try:
                with open(file, "rb") as f2:
                    bytes = f2.read()
                    # Calculate hash for file
                    hash = hashlib.md5(bytes).hexdigest()
            except OSError:  # Ignore files that are found but can`t be read because that made the program exit
                pass
            file_dict[file] = hash  # Put files and their hashes in file_dict
            fhashlist = list(file_dict.values())


# Load hashes from the virushashes.txt file
def loadVirusHashes():
    global vhashlist
    with open('virushashes.txt', 'r') as datafile:
        vhashlist = list(datafile)
        vhashlist = [vhash.rstrip("\n") for vhash in vhashlist]


# Start the Scan by comparing all hashes of files to the virus hashes
def scan():
    global infected_hashes
    global infected_files
    print("Scan on {} files started.".format(str(len(fhashlist))))
    infected_hashes = (set(fhashlist).intersection(set(vhashlist)))
    print("Scan on {} files finished.".format(str(len(fhashlist))))


def showResults():
    print("Found {} infected files!".format(str(len(infected_hashes))))
    for inf_hash in infected_hashes:
        infected_files.append(list(file_dict.keys())[
                              list(file_dict.values()).index(inf_hash)])
    for inf in infected_files:
        print("[VIRUS FOUND] the file {} contains a virus!".format(inf))


def delete():
    while True:
        answer = input("Should the found infected files be deleted ? [y/n]: ")
        if answer == "y":
            for inf in infected_files:
                os.remove(inf)
                print("Removed {}.".format(inf))
            exit()
        elif answer == "n":
            exit()        
        else:
            print("Invalid input.")


# Having all functions in the correct order so everything will actually work
def main():
    print("--- silityAV 1.0 ---")
    loadConfig()
    hashUpdater()
    loadFiles()
    loadVirusHashes()
    scan()
    showResults()
    if len(infected_files) != 0:
        delete()


main()  # Finally make the program do something
