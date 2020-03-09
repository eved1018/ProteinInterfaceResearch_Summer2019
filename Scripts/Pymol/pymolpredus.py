from pymol import cmd
from pymol.cgo import *
from pymol.vfont import plain

from PIL import Image, ImageOps, ImageDraw, ImageFont


class Rotate:
    def __init__(self, protein_name, correct_residue_comm, predus_residue_comm):
            self.protein_name = protein_name

            self.correct_residue_comm = correct_residue_comm
            self.predus_residue_comm = predus_residue_comm

            self.value_color_pairs = []


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

            # gets the z_value, since in the xyz_coords list there are brackets,
            # this adjusts for them
            
            z = (xyz_coords[2])[:-1]

            y = (xyz_coords[1])

            
            x = xyz_coords[0]

            if x[0] == '[':       # the first char of the value might be '['
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

        skip = ["1d7p", "2hmg.A"]     # antigens to skip taking a picture of (for debugging)
        skip = [""]

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
            file_name = ("../../Antogen/pymolimages/{}/{}_{}.png".format(
                self.protein_name, self.protein_name, str(current_angle)))
            
            
            # file_name = ("../../Antogen/pymolimages/${proteinname}/${proteinname}_" +
            # str(current_angle) + ".png")
            
            print("File: " + file_name)

            
            cmd.zoom(complete=1)
            cmd.png(file_name, width=900, height=900, dpi=500, ray=1, quiet=0)

            self.drawLegend(file_name)


        
        cmd.rotate(rotation_axis, angle=best_angle)
        cmd.zoom(complete=1)
        
        # file_name = ("../../Antogen/pymolimages/${proteinname}/${proteinname}_" +
        #    str(best_angle) + coord_to_optimize + "-BEST-" + rotation_axis + ".png")

        

        # cmd.png(file_name, width=900, height=900, dpi=500, ray=1, quiet=0)

    

    def drawLegend(self, file_name):
        img = Image.open(file_name, 'r')
        imgW = 1000
        imgH = 950

        bg = Image.new("RGB", (imgW, imgH))

        bg.paste(img, (0, 0))

        draw = ImageDraw.Draw(bg)

        

        font1 = ImageFont.truetype("../../Antogen/pymolimages/Arial.ttf", size=24)
        

        x, y = imgW-300, imgH-200

        # Legend outline rectangle
        draw.rectangle([x, y, imgW-10, imgH-10], outline="#fff", width=5)

        if len(self.value_color_pairs) >= 1:
            draw.rectangle([x+20, y+30, x+20+20, y+30+20], fill=self.value_color_pairs[0][1], outline="#fff", width=2)
            draw.text((x+50, y+30-3), self.value_color_pairs[0][0], font=font1)
        
        if len(self.value_color_pairs) >= 2:
            draw.rectangle([x+20, y+80, x+20+20, y+80+20], fill=self.value_color_pairs[1][1], outline="#fff", width=2)
            draw.text((x+50, y+80-3), self.value_color_pairs[1][0], font=font1)

        if len(self.value_color_pairs) >= 3:
            draw.rectangle([x+20, y+130, x+20+20, y+130+20], fill=self.value_color_pairs[2][1], outline="#fff", width=2)
            draw.text((x+50, y+130-3), self.value_color_pairs[2][0], font=font1)


        bg.save(file_name)

    def take_pictures(self):
        # protein = "$proteinname"
        protein = self.protein_name

        green_resi = self.correct_residue_comm      # green residues
        blue_resi = self.predus_residue_comm        # blue residues

        # green_resi = "$correct_residue_comm"   # green residues
        # blue_resi =  "$predus_residue_comm"    # blue residues

        

        self.value_color_pairs.append(("Predus", "#00f"))
        self.value_color_pairs.append(("Annotated", "#f00"))

        if (green_resi == ""):
            print("\n\nGREEN_NOT_HERE\n\n")
            resi_vals = "resi " + blue_resi
        
        else:
            print("\n\nGREEN_HERE\n\n")
            print("Green: ", green_resi)
            print("Blue: ", blue_resi)
            print("\n\n")
            resi_vals = "resi " + green_resi
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

        print("AAA")

        "../../Antogen/pymolimages/{}.png".format(self.protein_name)

        cmd.png("../../Antogen/pymolimages/{}.png".format(self.protein_name), width=900, height=900, dpi=500, ray=1)

        # Legend box START

        self.drawLegend("../../Antogen/pymolimages/{}.png".format(self.protein_name))

        # Legend box END
