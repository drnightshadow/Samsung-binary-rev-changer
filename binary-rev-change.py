#!/usr/bin/python

import os
import argparse

verbose = 0

binRevOffset = 8 # ********X****

def parseArgs():
    parser = argparse.ArgumentParser(description="change the binary version of Samsung firmware [v0.2]")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("filename", help="Filename (WITHOUT LZMA (NOT .LZ4))")
    parser.add_argument("target", help="Target binary revision")
    args = parser.parse_args()
    return args

def printVerbose(text):
    if verbose == 1:
        print("[D] ", text)

def askForModelString():
    print("For some reason, the script couldn't find your model string.")
    modelString = input("You need to enter it manually. (ex. A528BXXS6EWK1):")
    return modelString

def tryFindModelString(_content):
    modelString = _content.decode('ascii', errors='replace').rfind("SM-") # This should be last, in the firmwares that I've seen at least.

    # Try to fix this up soon
    if modelString == -1:
        finModelString = _content.decode('ascii', errors='replace').rfind(askForModelString())
        if modelString == -1:
            print("Can't find your model string. Sorry!")
            exit(1)
    else:
        finModelString = modelString - 48 # Hopefully try to dehardcode this soon? Maybe from SignerVer offset?

    return finModelString

def main():
    global verbose

    args = parseArgs()

    if args.verbose == True:
        verbose = 1

    if "super" in args.filename:
        print("WARNING WARNING WARNING")
        print("This tool won't work on super.imgs.")
        print("They're too big for the tool to handle.")
        exit(2)

    printVerbose("Trying to open file")

    # This should be reworked for huge images!
    file = open(args.filename, "rb")

    fileContent = file.read()
    file.close() 

    modelStringOffset = tryFindModelString(fileContent)

    currentBinRev = chr(fileContent[modelStringOffset + binRevOffset])

    printVerbose(currentBinRev)
    printVerbose(hex(modelStringOffset))

    if currentBinRev == args.target:
        print("Target binary revision is the same as current binary revision.")
        exit(1)
    
    fullBinRevOffset = modelStringOffset + binRevOffset

    newFileContent = fileContent[:fullBinRevOffset] + args.target.encode('ascii') + fileContent[(fullBinRevOffset + 1):]
    
    file = open(args.filename, "wb")
    file.seek(0)
    file.write(newFileContent)
    file.close()

    print("[*] Done!")
    exit(0)

main()
