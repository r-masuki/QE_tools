import sys
import re

args = sys.argv

# args[1] : pw.material.bands.in
# args[2] : bands.material.out
# args[3] : output filename

flag_kpoints = 0

# list of high-symmetry points
n_kpoints = 0
kpoint_names = []
kpoint_coordinates = []

# read kpoint names from pw.material.bands.in
fin = open(args[1], "rt")
while True:
  line = fin.readline()
  if not line:
    break

  # if K_POINTS
  if flag_kpoints:
    line_split = line.split("!")
    line_split[-1] = (line_split[-1])[:-1]
    kpoint_names.append(line_split[-1])

  # if K_POINTS start
  match_K_POINTS = re.match("K_POINTS", line)
  if match_K_POINTS:
    flag_kpoints = 1
    line = fin.readline()
    n_kpoints = int(line)
    
fin.close()

# read kpoint coordinates from bands.material.out
fin = open(args[2], "rt")
while True:
  line = fin.readline()
  if not line:
    break

  # if K_POINTS
  match_K_POINTS = re.match("     high-symmetry point:", line)

  if match_K_POINTS:
    line_split = line.split(" ")
    line_split[-1] = (line_split[-1])[:-1]
    kpoint_coordinates.append(line_split[-1])  
  
fin.close()
     
# write output
fout = open(args[3], "wt")
fout.write('set xtics (')
for i in range(n_kpoints):
  fout.write('"' + kpoint_names[i] + '" ' + kpoint_coordinates[i])
  if(i < n_kpoints-1):
    fout.write(', ')

fout.write(')')

fout.close()


