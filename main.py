import os
import ctypes
import hashlib
import zlib

def createGit():
    directory = f"{os.curdir}/.xgit"
    if not os.path.isdir(directory):
        os.mkdir(directory)
        print(f"Directory created at {directory}")
        if os.name == 'nt':
            ctypes.windll.kernel32.SetFileAttributesW(directory, 0x02)
    return

def blobFile(f):
    data = f.read()
    header = f"BLOB {len(data)}\0".encode('utf-8')
    print(header)
    finalData = zlib.compress(header + data)
    print(finalData)
    finalHash = hashlib.sha1(finalData).hexdigest()
    print(finalHash)
    os.makedirs(f"{os.curdir}/.xgit/{finalHash[:2]}")
    with open(f"{os.curdir}/.xgit/{finalHash[:2]}/{finalHash}", 'wb') as blob: blob.write(finalData)
    return

createGit()

with os.scandir(os.curdir) as files:
    for file in files:
        if file.is_file():
            with open(file, 'rb') as fileObj:
                blobFile(fileObj)