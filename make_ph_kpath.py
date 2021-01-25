import sys
import re
import math

args = sys.argv

# args[1] : kpath input file
# args[2] : output file
# args[3] : output filename

flag_kpoints = 0

# list of high-symmetry points
high_sym_kpoints = []


# read high-symmetry kpoint names from pw.material.bands.in
fin = open(args[1], "rt")

while True:
  #line2_split = line
  line = fin.readline()

  if not line:
    break

  line_split_tmp = line.split(" ")
  line_split_str = []
  for s in line_split_tmp:
    if(s != ""):
      if(s[-1] != "\n"):
        line_split_str.append(s)
      else:
        line_split_str.append(s[:-1])
  
  high_sym_kpoint = []

  for i in range(3):
    high_sym_kpoint.append(float(line_split_str[i]))
  
  high_sym_kpoint.append(int(line_split_str[3]))
  high_sym_kpoint.append(line_split_str[4].replace("_", " "))

  print(high_sym_kpoint)

  high_sym_kpoints.append(high_sym_kpoint)

fin.close()

# generate kpath

n_kpoints = 0
kpath = []
for i in range(len(high_sym_kpoints)-1):
  n_kp_tmp = high_sym_kpoints[i][3]
  n_kpoints += n_kp_tmp
  for j in range(n_kp_tmp):
    kx = high_sym_kpoints[i][0] + j/n_kp_tmp * (high_sym_kpoints[i+1][0]-high_sym_kpoints[i][0])
    ky = high_sym_kpoints[i][1] + j/n_kp_tmp * (high_sym_kpoints[i+1][1]-high_sym_kpoints[i][1])
    kz = high_sym_kpoints[i][2] + j/n_kp_tmp * (high_sym_kpoints[i+1][2]-high_sym_kpoints[i][2])

    kpath.append([kx, ky, kz])

# print phonon kpath

fout = open("ph_kpath.txt", "wt")
fout.write("{nk}\n".format(nk=n_kpoints))
for i in range(n_kpoints):
  fout.write("{kx:.5f} {ky:.5f} {kz:.5f} 1.0\n".format(kx=kpath[i][0], ky=kpath[i][1], kz=kpath[i][2]))

fout.close()
# print xtics for plot
k = 0.0
fout = open("xtics.txt", "wt")
fout.write('set xtics (')

for i in range(len(high_sym_kpoints)):
  fout.write('"' + high_sym_kpoints[i][4] + '" ' + "{k_coord:.5f}".format(k_coord=k))
  if(i != len(high_sym_kpoints)-1):
    fout.write(', ')
    dkx = high_sym_kpoints[i+1][0] - high_sym_kpoints[i][0]
    dky = high_sym_kpoints[i+1][1] - high_sym_kpoints[i][1]
    dkz = high_sym_kpoints[i+1][2] - high_sym_kpoints[i][2]

    k += math.sqrt(dkx**2 + dky**2 + dkz**2)
fout.write(')')

fout.close()