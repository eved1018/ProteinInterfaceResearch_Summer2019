from pymol import cmd
from pymol.cgo import *
from pymol.vfont import plain

from pathlib import Path
import os

from PIL import Image, ImageOps, ImageDraw, ImageFont


class Rotate:
    def __init__(self, method, protein_name, correctly_predicted, wrongly_predicted):
        self.method= method
        self.protein_name = protein_name

        self.correctly_predicted = correctly_predicted
        self.wrongly_predicted = wrongly_predicted

        self.value_color_pairs = []

        self.mainDir = Path("../../Antogen/pymolimages/")


    """
    Returns a list of the coords of all the residues as floats
    so the return will look like this:
    return = [
    [x1, y1, z1],
    [x2, y2, z2],
    [x3, y3, z3],
    [x4, y4, z4],
    ]
    Each nested list is a set of coordinates for a residue

    """
    def get_xyz_coords_as_floats(self, resi_vals):
        
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

            if xyz_coords[0] == "[":
                xyz_coords.pop(0)
            if xyz_coords[-1] == "]":
                xyz_coords.pop()

            # The '[:-1]' is to fix formatting and properly obtain z coordinate
            z = (xyz_coords[2])[:-1]

            y = (xyz_coords[1])
            x = xyz_coords[0]

            # (fixes formatting) the first char of the value might be '['
            if x[0] == '[': 
                x = x[1:]

            all_resi_coords.append([float(x), float(y), float(z)])

        return all_resi_coords


    def get_avg_coord(self, all_coords):
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


    def get_coord_val(self, resi_vals, coord):
        all_resi_coords = self.get_xyz_coords_as_floats(resi_vals)

        avg_coord = self.get_avg_coord(all_resi_coords)

        if coord == 'x':
            return avg_coord[0]

        if coord == 'y':
            return avg_coord[1]

        if coord == 'z':
            return avg_coord[2]
    
    
    # returns if val1 is better than val2
    def isBetter(self, val1, val2, optimized_coord):
        if (optimized_coord == 'z'):
            return val1 < val2

        elif optimized_coord == 'x':
            center_x = float(cmd.get_position()[0])
            return abs(val1-center_x) < abs(val2-center_x)

        elif optimized_coord == 'y':
            center_y = float(cmd.get_position()[1])
            return abs(val1-center_y) < abs(val2-center_y)

    def optimize_rotation2(self, axis, resi_vals, optimized_coord):
    
        increment = 20


    # finds the 'optimal' coordinate value for 'optimized_coord' by rotating about 'axis'
    def optimize_rotation(self, rotation_axis, resi_vals, coord_to_optimize):

        # skip = ["1d7p", "2hmg.A"]     # antigens to skip taking a picture of (for debugging)
        skip = [""] # for debugging

        #if not "${proteinname}" in skip:
        #   return

        increment = 20    # how much to increment each time 

        current_angle = 0

        best_angle = 0    # default value
        best_val = -100000  # sets it to a default value that will always change

        # cycles through all possible angles (multiple of increment) and finds 
        # the greatest z-value 
        while current_angle < 360:

            

            cmd.rotate(rotation_axis, angle=increment)
            coord_val = self.get_coord_val(resi_vals, coord_to_optimize)

            if self.isBetter(coord_val, best_val, coord_to_optimize):
                best_val = coord_val
                best_angle = current_angle
            
            current_angle += increment  

            nearness = abs( coord_val - float(cmd.get_position()[0]) )

            
            # GIVES AN IMAGE FOR EACH ANGLE
            file_path = self.mainDir/self.method/self.protein_name

            if not os.path.exists(str(file_path)):
                os.makedirs(str(file_path))
            
            file_name = str(file_path/"{}_{}.png".format(self.protein_name, str(current_angle)))
            
            cmd.zoom(complete=1)
            cmd.png(file_name, width=900, height=900, dpi=500, ray=1, quiet=0)

            self.drawLegend(file_name)


        
        cmd.rotate(rotation_axis, angle=best_angle)
        cmd.zoom(complete=1)
        

    

    def drawLegend(self, file_name):
        img = Image.open(file_name, 'r')
        imgW = 1000
        imgH = 950

        bg = Image.new("RGB", (imgW, imgH))

        bg.paste(img, (0, 0))

        draw = ImageDraw.Draw(bg)

        
        
        font1 = ImageFont.truetype(str(self.mainDir/"Arial.ttf"), size=24)
        

        x, y = imgW-300, imgH-200

        # Legend outline rectangle
        draw.rectangle([x, y, imgW-10, imgH-10], outline="#fff", width=5)

        draw.text((x+20, y+20-3), self.method, font=font1)

        if len(self.value_color_pairs) >= 1:
            draw.rectangle([x+20, y+60, x+20+20, y+60+20], fill=self.value_color_pairs[0][1], outline="#fff", width=2)
            draw.text((x+50, y+60-3), self.value_color_pairs[0][0], font=font1)
        
        if len(self.value_color_pairs) >= 2:
            draw.rectangle([x+20, y+100, x+20+20, y+100+20], fill=self.value_color_pairs[1][1], outline="#fff", width=2)
            draw.text((x+50, y+100-3), self.value_color_pairs[1][0], font=font1)

        if len(self.value_color_pairs) >= 3:
            draw.rectangle([x+20, y+140, x+20+20, y+140+20], fill=self.value_color_pairs[2][1], outline="#fff", width=2)
            draw.text((x+50, y+140-3), self.value_color_pairs[2][0], font=font1)


        bg.save(file_name)

    def take_pictures(self):
        # protein = "$proteinname"
        protein = self.protein_name

        green_resi = self.correctly_predicted      # green residues
        blue_resi = self.wrongly_predicted        # blue residues

        # green_resi = "$correctly_predicted"   # green residues
        # blue_resi =  "$wrongly_predicted"    # blue residues

        
        self.value_color_pairs.append(("Annotated", "#f00"))
        self.value_color_pairs.append(("Incorrectly Predicted", "#00f"))

        if (green_resi == ""):
            resi_vals = blue_resi
        
        else:
            resi_vals = green_resi
            self.value_color_pairs.append(("Correctly Predicted", "#0f0"))


        # optimize_rotation('z', resi_vals, 'x')
        # optimize_rotation('y', resi_vals, 'x')
        # cmd.zoom(complete=1)


        # optimize_rotation('x', resi_vals, 'z')
        self.optimize_rotation('y', resi_vals, 'x')
        cmd.zoom(complete=1)


        # optimize_rotation('x', resi_vals, 'y')
        # optimize_rotation('z', resi_vals, 'y')
        # cmd.zoom(complete=1)

        cmd.zoom(complete=1)

        proteinPath = self.mainDir/self.method
        proteinDir = str(proteinPath/"{}.png".format(self.protein_name))

        cmd.png(proteinDir, width=900, height=900, dpi=500, ray=1)

        # Legend box START

        self.drawLegend(proteinDir)

        # Legend box END
