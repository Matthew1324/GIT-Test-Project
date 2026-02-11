import os
import ctypes
import hashlib
import zlib

def createGit():
    directory = f"{os.curdir}/.xgit"
    if not os.path.isdir(directory):
        os.mkdir(directory)
        print(f" - Directory created at {directory}")
        if os.name == 'nt':
            ctypes.windll.kernel32.SetFileAttributesW(directory, 0x02)
    return

def blobFile(f):
    data = f.read()
    header = f"BLOB {len(data)}\0".encode('utf-8')
    finalData = zlib.compress(header + data)
    finalHash = hashlib.sha1(finalData).hexdigest()
    os.makedirs(f"{os.curdir}/.xgit/{finalHash[:2]}", exist_ok=True)
    with open(f"{os.curdir}/.xgit/{finalHash[:2]}/{finalHash}", 'wb') as blob: blob.write(finalData)
    return

def createIgnoreFile():
    ignoreList = [".xgit", ".git"] #Default ignored files
    with open(f"{os.curdir}/.xgit/ignore.dat", 'w') as f: f.write('\n'.join(ignoreList))
    return ignoreList



createGit()
ignoreList = list()
try:
    with open(f"{os.curdir}/.xgit/ignore.dat", 'r') as f: ignoreList = f.read().split("\n")
    print(ignoreList)
except OSError:
    print(" - Regenerating ignore.dat")
    ignoreList = createIgnoreFile()


with os.scandir(os.curdir) as files:
    for file in files:
        if file.is_file() and not file.name in ignoreList:
            print(f"file {file.name}")
            with open(file, 'rb') as fileObj:
                blobFile(fileObj)
        elif file.is_dir() and not file.name in ignoreList:
            print(f"folder {file.name}")