## Progress bar
import sys

def startProgress(title):
    """Creates a progress bar 40 chars long on the console
    and moves cursor back to beginning with BS character"""
    global progress_x
    sys.stdout.write("\r"+title + ": [" + "-" * 40 + "]")# + chr(8) * 41)
    sys.stdout.flush()
    progress_x = 0


def progress(x,title):
    """Sets progress bar to a certain percentage x.
    Progress is given as whole percentage, i.e. 50% done
    is given by x = 50"""
    global progress_x
    x = int(x * 40 // 100)                      
    sys.stdout.write("\r"+title + ": [" +"#" * x + "-" * (40 - x) + "]") #+ chr(8) * 41)
    sys.stdout.flush()
    progress_x = x


def endProgress(title):
    """End of progress bar;
    Write full bar, then move to next line"""
    sys.stdout.write("\r"+title + ": ["+"#" * 40 + "]\n")
    sys.stdout.flush()
    
    # call startProgress passing the description of the operation,
    #then progress(x) where x is the percentage and finally endProgress()
##=============================================================================
## END OF PROGRAM
##=============================================================================
