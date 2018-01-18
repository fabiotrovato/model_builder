## Some lessons on python usage.



## Import modules 
## The name of a module is stored in the variable __name__

import sys


def ver(v):
    print "in funct ver: v is", v
    print "v is of type",type(v)
    if v == "1" or v == 1:
    ## version 1
    ## Whenever an import command, like the one below, is encountered (usually, but non necessarily at the beginning)
    ## the current module's symbol table is updated with the name of the imported module.
        import os

        print "os.__name__ = ",os.__name__
        mypath = os.getcwd()
        print "version 1: mypath = os.getcwd()", mypath

    if v == "2" or v == 2:
    ## version 2
    ## Whenever a from ... import command, like the one below, is encountered (usually, but non necessarily at the beginning)
    ## the current module's symbol table is updated with the name of the method imported from the specified module.
    ## Therefore, the module name is not known, but only the method name.
        from os import listdir, getcwd
        from os.path import isfile, join

        ## print "os.__name__ = ",os.__name__  # gives error because os is not defined

        print "getcwd.__name__ = ",getcwd.__name__
        mypath = getcwd()
        print "version 2: mypath = getcwd()", mypath

    return
#onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

## Types and names of imported modules

print "when v = sys.argv[1]"
v = sys.argv[1]
print "in main: v is",type(v)
ver(v)

print "when v = 1"
v = 1
print "in main: v is",type(v)
ver(v)
