import time
import nmap
from termcolor import colored
from visuals import visuals

# A List of Items
items = list(range(0, 57))
l = len(items)

p1 = visuals
# Initial call to print 0% progress
p1.printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
time.sleep(3)
p1.printProgressBar(57, l, prefix='Progress:', suffix='Complete', length=50)
time.sleep(3)





print("Testing.....")
for i, item in enumerate(items):

    time.sleep(0.1)
    # Update Progress Bar
    p1.printProgressBar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)