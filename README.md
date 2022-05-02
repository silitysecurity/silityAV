# silityAV

## About

silityAV is a antivirus witten in Python. It works by comparing MD5 hashes of known viruses to MD5 hashes of files on your system in a specified path. The list of known virus hashes comes from virusshare.com and is frquently updated. The program automatically downloads the full list on first start and checks for updates on each start and downloads them.

***

## Usage

Running a scan on a folder:
```
$ python av.py -p <path>
```

So scanning your full system would work like this:
```
$ python av.py -p ~/
```

The program will then check if the local list of virus hashes is up to date and update it if necessary. It will then start scanning the system and at the end print out if it found any files that may contain a virus. If the program found a virus it will ask you if you want to delete the file and do so if you wish to. Before deleting files always check if they aren't any of your personal files that you don't want to delete.

***

## Contributing



We would love your improvements or feedback!
If you have any improvements in the code or fixed any bugs make a Pull Request. If you found a bug and can't fix it, open an Issue. If you have any ideas for new features open an Issue or write us an email to silitysecurity@protonmail.com.

***

#### Warning!
This prorgram is developed and maintained by a 17 year old student. Don't expect the program to find every virus on your system. Don't expect a suspected virus to actually be a virus. Don't kill me for any viruses not found by this program or any files that you accidently deleted. Thanks.

