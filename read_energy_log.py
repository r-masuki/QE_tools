import sys
import re

args = sys.argv

fin = open(args[1], "rt") 
fout = open(args[2], "wt") # add to existing file

i = 1 #iteration number

while True:
  line = fin.readline()
  if not line:
    break

  match_pattern = re.match("     total energy", line)
  if match_pattern:
    line_split = line.split(" ")
    fout.write(str(i) + " " + line_split[-2] + "\n")
    i = i+1

fin.close()
fout.close()


