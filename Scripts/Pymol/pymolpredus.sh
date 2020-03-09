#!/usr/bin/env bash

# Function 1 - takes in predus pdbs with prediction and filters out a list of predicted residues

# rm ../../Data_Files/PymolPredus/Scripts/script.pml
rm ../../Antogen/pymolscripts/script.pml # deletes the file if it already exists


find ../../Antogen/pymolimages/ -type f -name "*.png" -delete
 



# old directory: ../../Data_Files/Predus/predus_outputfiles/*

for file in ../../Antogen/Predus_antogens/*
do
  proteinname=`echo $file | awk -F/ '{print $5}'| awk -F. '{print $2}' | sed 's/\_/./g'`

  echo $file" ~~~~ "$proteinname

  #interfacefile="../../Annotated_Residues/Testquery30_Interface/$proteinname"

  # annotated files
  interfacefile="../../Antogen/InterfaceResidues/sorted/${proteinname}_sorted" 

  # interfaceoutput=../../Data_Files/PymolPredus/interfaceoutput/interfaceoutput_${proteinname}.txt
  
  interfaceoutput=../../Antogen/preduce_interface_output/interfaceoutput_${proteinname}.txt
  cat $interfacefile | awk '{print $1}' | sort > $interfaceoutput


  # outputfile=../../Data_Files/PymolPredus/predsort/predsort_${proteinname}.txt
  outputfile=../../Antogen/predsort/predsort_${proteinname}.txt

  # cat $file | awk '{print $6, $11}' | uniq |sort -k2 -nr| uniq | head -n"15" | awk '{print $1}' > $outputfile

  # outputfile=/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/predsort/predsort_${proteinname}.txt
  N=`cat "$interfaceoutput" | awk 'END{print NR}'`
  # cat $file | awk '{print $6, $11}' | uniq |sort -k2 -nr| uniq | head -n"$N" | awk '{print $1}'> $outputfile
  cat $file | awk '{print $6, $11}' | uniq | uniq | head -n"$N" | awk '{print $1}'> $outputfile
  
  #cat $outputfile | awk '{print $1}' | sort > $outputfile # just added
  # echo "UNSORTED1--------------"
  # cat $outputfile
  # echo "UNSORTED1--------------"
  
  # sort -on2 outputfile outputfile
  # ################## DEBUG
  # echo "SORTED--------------"
  # cat $outputfile
  # echo "FILE: $outputfile"
  # echo "--done--"
  ################## DEBUG

  # for debugging
  #cat $file | awk '{print $6, $11}' | uniq |sort -k2 -nr| uniq | head -n"$N" | awk '{print $1}'

  # printf "\n\n------------------------------------------------\n"
  # printf "FILE: $outputfile\n"

# Function 2 - comparison of predicted and annnotated residues
  #ispred_pred_comm
  #dock_pred_comm=
  predus_residue_comm=`comm -23 $outputfile $interfaceoutput | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  interface_residue_comm=`comm -13 $outputfile $interfaceoutput| awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  correct_residue_comm=`comm -12 $outputfile $interfaceoutput | awk '{printf $1"+"}'| awk '{print substr($1,1,length($1)-1)}'`
  correct_residue_comm_check=`test -z "$correct_residue_comm" && echo "" || echo "; color green, resi $correct_residue_comm"`
  correct_res_sphere=`test -z "$correct_residue_comm" && echo "" || echo "; select color green; show spheres, SEL"`
  correct_res_label=`test -z "$correct_residue_comm" && echo "" || echo "; label resi $correct_residue_comm, ID; set label_position,(3,2,1)"`

  # cat $outputfile
  # printf "~~~~~~~~~~~~~~\n"
  # cat $interfaceoutput

  
  # rm ../../Data_Files/PymolPredus/Images/${proteinname}.png
  # rm ../../Antogen/pymolimages/${proteinname}.png   # file in main folder
  

  # files_in_subfolders = ../../Antogen/pymolimages/${proteinname}/*.png  # files in subfolders
  # for f in $files_in_subfolders
  # do 
  #   rm $f
  # done
  

# Function 3- creation of pml script to image the proteins
  echo "
delete all
fetch $proteinname, async = 0

# Blue -- Predus ($predus_residue_comm)
# Red -- Annotated ($interface_residue_comm)

color white; color blue, resi $predus_residue_comm; color red, resi $interface_residue_comm $correrct_residue_comm_chek
color green, resi $correct_residue_comm

select color blue; show spheres, SEL
select color red; show spheres, SEL
$correct_res_sphere
$correct_res_label
set sphere_scale, 0.50, (all)
remove resn hoh
zoom complete=1
<<<<<<< HEAD

# blue
orient resi $predus_residue_comm 
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center $proteinname


python

from pymol import cmd
from pymol.cgo import *
from pymol.vfont import plain

from PIL import Image, ImageOps, ImageDraw, ImageFont
 
\"\"\"
Returns a list of the coords of all the residues as floats
so the return will look like this:
return = [
  [x1, y1, z1],
  [x2, y2, z2],
  [x3, y3, z3],
  [x4, y4, z4],
]
Each nested list is a set of coordinates for a residue

\"\"\"
def get_xyz_coords_as_floats(resi_vals):
  
  # gets the coordinates of all the residues, and stores it in xyz_coords as a
  # list of "numpy lists", which is then converted to a string and then split
  # each set of xyz_coords will end up equalling something like ["[", "x.xxx", "x.xxx", "x.xxx]"]
  # The opening and closing brackets in the list are not intended

  all_resi_coords_numpy = cmd.get_coords(resi_vals, 1)

  all_resi_coords = []

  if all_resi_coords_numpy is None:
    return [[0, 0, 0]]

  for i in range(len(all_resi_coords_numpy)):
    xyz_coords = str(all_resi_coords_numpy[i]).split()

    if xyz_coords[0] == \"[\":
      xyz_coords.pop(0)
    if xyz_coords[-1] == \"]\":
      xyz_coords.pop()

    # gets the z_value, since in the xyz_coords list there are brackets,
    # this adjusts for them
    
    z = (xyz_coords[2])[:-1]

    y = (xyz_coords[1])

    
    x = xyz_coords[0]

    if x[0] == '[':       # the first char of the value might be '['
      x = x[1:]

    all_resi_coords.append([float(x), float(y), float(z)])

  return all_resi_coords


def get_avg_coord(all_coords):
  avg_x = avg_y = avg_z = 0

  for coord in all_coords:
    avg_x += coord[0]
    avg_y += coord[1]
    avg_z += coord[2]

  total_coords = len(all_coords)

  avg_x /= total_coords
  avg_y /= total_coords
  avg_z /= total_coords

  return [avg_x, avg_y, avg_z]


def get_coord_val(resi_vals, coord):
  all_resi_coords = get_xyz_coords_as_floats(resi_vals)

  avg_coord = get_avg_coord(all_resi_coords)

  if coord == 'x':
    return avg_coord[0]

  if coord == 'y':
    return avg_coord[1]

  if coord == 'z':
    return avg_coord[2]
  
  
# returns if val1 is better than val2
def isBetter(val1, val2, optimized_coord):
    if (optimized_coord == 'z'):
      return val1 < val2

    elif optimized_coord == 'x':
      center_x = float(cmd.get_position()[0])
      return abs(val1-center_x) < abs(val2-center_x)

    elif optimized_coord == 'y':
      center_y = float(cmd.get_position()[1])
      return abs(val1-center_y) < abs(val2-center_y)

def optimize_rotation2(axis, resi_vals, optimized_coord):
  
  increment = 20


# finds the 'optimal' coordinate value for 'optimized_coord' by rotating about 'axis'
def optimize_rotation(rotation_axis, resi_vals, coord_to_optimize):

  skip = [\"1d7p\", \"2hmg.A\"]     # antigens to skip taking a picture of (for debugging)
  skip = [\"\"]

  #if not \"${proteinname}\" in skip:
   #   return

  increment = 180    # how much to increment each time 

  current_angle = 0

  best_angle = 0    # default value
  best_val = -100000  # sets it to a default value that will always change

  # cycles through all possible angles (multiple of increment) and finds 
  # the greatest z-value 
  while current_angle < 360:

    

    cmd.rotate(rotation_axis, angle=increment)
    coord_val = get_coord_val(resi_vals, coord_to_optimize)

    if isBetter(coord_val, best_val, coord_to_optimize):
      best_val = coord_val
      best_angle = current_angle
    
    current_angle += increment  

    nearness = abs( coord_val - float(cmd.get_position()[0]) )

    
    # GIVES AN IMAGE FOR EACH ANGLE
    file_name = (\"../../Antogen/pymolimages/${proteinname}/${proteinname}_\" +
      str(current_angle) + \".png\")
    
    print(\"File: \" + file_name)

    
    cmd.zoom(complete=1)
    cmd.png(file_name, width=900, height=900, dpi=500, ray=1, quiet=0)

    drawLegend(file_name, value_color_pairs)


  
  cmd.rotate(rotation_axis, angle=best_angle)
  cmd.zoom(complete=1)
  
  # file_name = (\"../../Antogen/pymolimages/${proteinname}/${proteinname}_\" +
  #    str(best_angle) + coord_to_optimize + \"-BEST-\" + rotation_axis + \".png\")

  

  # cmd.png(file_name, width=900, height=900, dpi=500, ray=1, quiet=0)

  

def drawLegend(file_name, value_color_pairs):
  img = Image.open(file_name, 'r')
  imgW = 1000
  imgH = 950

  bg = Image.new(\"RGB\", (imgW, imgH))

  bg.paste(img, (0, 0))

  draw = ImageDraw.Draw(bg)

  

  font1 = ImageFont.truetype(\"../../Antogen/pymolimages/Arial.ttf\", size=24)
  

  x, y = imgW-300, imgH-200

  # Legend outline rectangle
  draw.rectangle([x, y, imgW-10, imgH-10], outline=\"#fff\", width=5)

  if len(value_color_pairs) >= 1:
    draw.rectangle([x+20, y+30, x+20+20, y+30+20], fill=value_color_pairs[0][1], outline=\"#fff\", width=2)
    draw.text((x+50, y+30-3), value_color_pairs[0][0], font=font1)
  
  if len(value_color_pairs) >= 2:
    draw.rectangle([x+20, y+80, x+20+20, y+80+20], fill=value_color_pairs[1][1], outline=\"#fff\", width=2)
    draw.text((x+50, y+80-3), value_color_pairs[1][0], font=font1)

  if len(value_color_pairs) >= 3:
    draw.rectangle([x+20, y+130, x+20+20, y+130+20], fill=value_color_pairs[2][1], outline=\"#fff\", width=2)
    draw.text((x+50, y+130-3), value_color_pairs[2][0], font=font1)


  bg.save(file_name)


protein = \"$proteinname\"

green_resi = \"$correct_residue_comm\"   # green residues
blue_resi =  \"$predus_residue_comm\"    # blue residues

value_color_pairs = []

value_color_pairs.append((\"Predus\", \"#00f\"))
value_color_pairs.append((\"Annotated\", \"#f00\"))

if (green_resi == \"\"):
  print(\"\n\nGREEN_NOT_HERE\n\n\")
  resi_vals = \"resi \" + blue_resi
  
else:
  print(\"\n\nGREEN_HERE\n\n\")
  print(\"Green: \", green_resi)
  print(\"Blue: \", blue_resi)
  print(\"\n\n\")
  resi_vals = \"resi \" + green_resi
  value_color_pairs.append((\"Correctly Predicted\", \"#0f0\"))


# optimize_rotation('z', resi_vals, 'x')
# optimize_rotation('y', resi_vals, 'x')
# cmd.zoom(complete=1)


# optimize_rotation('x', resi_vals, 'z')
optimize_rotation('y', resi_vals, 'x')
cmd.zoom(complete=1)


# optimize_rotation('x', resi_vals, 'y')
# optimize_rotation('z', resi_vals, 'y')
# cmd.zoom(complete=1)

cmd.zoom(complete=1)

print(\"AAA\")

cmd.png(\"../../Antogen/pymolimages/\" + \"${proteinname}\" + \".png\", width=900, height=900, dpi=500, ray=1)

# Legend box START

drawLegend(\"../../Antogen/pymolimages/\" + \"${proteinname}\" + \".png\", value_color_pairs)

# Legend box END

python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/${proteinname}.png, width=900, height=900,ray=1, dpi=500



delete all" >> ../../Antogen/pymolscripts/script.pml



# zoom complete=1
# rotate x, 180
# orient resi ---
# unset opaque-background
# dpi = 300
# show spheres

  # open -a "Pymol" ../../Data_Files/PymolPredus/Scripts/script_${proteinname}.pml
  done
#
# for file in ../../Data_Files/PymolPredus/Scripts/* ;do
#   if [[ "$file" == script* ]];then
#     open -a "pymol" $file
#     echo "hi"
#   fi
# done


unameOut="$(uname -s)"

if [ "$unameOut" == "Linux" ]
then
  pymol ../../Antogen/pymolscripts/script.pml # if the script is run on linux
else
  open -a "Pymol" ../../Antogen/pymolscripts/script.pml # if it's run on windows/mac
fi

# ../../Data_Files/PymolPredus/Scripts/script.pml
=======
png ~/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/Images/${proteinname}.png, width=900, height=900,ray=1, dpi=500
delete all" >> ../../Data_Files/PymolPredus/Scripts/script.pml
done
>>>>>>> origin/E_Edelstein

open -a "Pymol" /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/PymolPredus/Scripts/script.pml

# label resi $predus_residue_comm, ID
# set label_position,(3,2,1)
# label resi $interface_residue_comm, ID
# set label_position,(3,2,1)
