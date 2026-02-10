import os
import ctypes
import hashlib

def createGit():
    directory = f"{os.curdir}/.xgit"
    if not os.path.isdir(directory):
        os.mkdir(directory)
        print(f"Directory created at {directory}")
        if os.name == 'nt':
            ctypes.windll.kernel32.SetFileAttributesW(directory, 0x02)
    return

def blobFile(f):
    data = f.read().encode('utf-8')
    header = f"BLOB {len(data)}\0".encode('utf-8')
    print(header)
    finalData = header + data
    print(finalData)
    finalHash = hashlib.sha1(finalData).hexdigest()
    print(finalHash)
    return

createGit()
with os.scandir(os.curdir) as files:
    for file in files:
        if file.is_file():
            with open(file, 'r') as fileObj:
                blobFile(fileObj)