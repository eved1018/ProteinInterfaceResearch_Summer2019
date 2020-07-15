from pymol import cmd
# from pymol.cgo import *
# from pymol.vfont import plain

from pathlib import Path
import os
from PIL import Image, ImageOps, ImageDraw, ImageFont
import imageio
import moviepy.editor as mp
import cv2

class LegendItem:
    def __init__(self, label, color):
        self.label = label
        self.color = color

class Rotator:
    def __init__(self, output_dir, method, protein_name, correctly_predicted, wrongly_predicted):
        self.method = method
        self.protein = protein_name

        self.correctly_predicted = correctly_predicted
        self.wrongly_predicted = wrongly_predicted

        # self.value_color_pairs = []
        self.legend_items = []

        self.main_dir = output_dir
        # self.file_path = self.main_dir/self.method.dir/self.protein
        self.file_path = self.main_dir/self.protein/self.method.dir

        self.images_for_gif = []
        self.images_for_mp4 = []


    # finds the 'optimal' coordinate value for 'optimized_coord' by rotating about 'axis'
    def rotate_and_capture(self, rotation_axis, increment, res_width, res_height):
        self.images_for_gif = []
        self.images_for_mp4 = []

        # cycles through all possible angles (multiple of increment)
        for current_angle in range(0, 360, increment):
            cmd.rotate(rotation_axis, angle=increment)

            # creates the file folder if it doesn't exist
            if not os.path.exists(str(self.file_path)):
                os.makedirs(str(self.file_path))
            
            # file_name = str(self.file_path/"{}_{}.png".format(self.protein, str(current_angle)))
            file_name = str(self.file_path/f"{self.method.name}_{str(current_angle)}.png")
            
            cmd.zoom(complete=1)
            cmd.png(file_name, width=res_width, height=res_height, dpi=500, ray=1, quiet=0)

            self.drawLegend(file_name, res_width, res_height)

            self.images_for_gif.append(imageio.imread(file_name))
            self.images_for_mp4.append(cv2.imread(file_name))
    

    def drawLegend(self, file_name, res_width, res_height):
        img = Image.open(file_name, 'r')
        imgW = res_width + 100
        imgH = res_height + 50

        bg = Image.new("RGB", (imgW, imgH))
        bg.paste(img, (0, 0))

        draw = ImageDraw.Draw(bg)
        
        font1 = ImageFont.truetype(str(self.main_dir/"Arial.ttf"), size=imgH//40)
        
        # Draw protein name
        draw.text((5, imgH-imgH/30), self.protein, font=font1)
        
        # Legend outline rectangle
        legend_w, legend_h = imgW/3, imgH/4
        x, y = imgW-legend_w-10, imgH-legend_h-10   # the -10 is for extra pixels for padding
        draw.rectangle([x, y, x+legend_w, y+legend_h], outline="#fff", width=5)

        draw.text((x+20, y+20-3), self.method.name.upper(), font=font1)

        for i, item in enumerate(self.legend_items):
            offset = imgH//12 + imgH//20 * i

            draw.rectangle([x+20, y+offset, x+20+20, y+offset+20], fill=item.color, outline="#fff", width=2)
            draw.text((x+50, y+offset), item.label, font=font1)

        bg.save(file_name)

    def image_to_video(self):
        height, width, layer = self.images_for_mp4[0].shape
        size = (int(width), int(height))
        # file_name = self.main_dir/self.method.dir/f"{self.protein}.mp4"
        file_name = self.main_dir/f"{self.protein}"/f"{self.method.dir}.mp4"
        
        # out = cv2.VideoWriter(file_name, cv2.VideoWriter_fourcc(*'DIVX'), 5, size)
        # creates a video writer object
        out = cv2.VideoWriter(str(file_name), cv2.VideoWriter_fourcc(*'DIVX'), 5, size)

        for img in self.images_for_mp4:
            out.write(img)  # adds the images to the video
        out.release()       # saves the video

    def generate_images(self, increment, width, height):
        protein = self.protein

        green_resi = self.correctly_predicted      # green residues
        blue_resi = self.wrongly_predicted        # blue residues

        self.legend_items.append(LegendItem("Annotated", "#00f"))
        self.legend_items.append(LegendItem("True Positive", "#0f0"))
        self.legend_items.append(LegendItem("False Postive", "#f00"))        

        self.rotate_and_capture('y', increment, width, height)    # rotate about the y axis

        # proteinPath = self.main_dir/self.method.dir
        proteinPath = self.main_dir/self.protein
        proteinDir = str(proteinPath/f"{self.method.dir}.png")


        # UNDO
        self.image_to_video()

        gif_file_name = str(proteinPath/f"{self.method.dir}.gif")
        imageio.mimsave(gif_file_name, self.images_for_gif, fps=5)

        mp4_file_name = self.main_dir/self.protein/f"{self.method.dir}.mp4"
        # UNDO END

        # clip = (mp.VideoFileClip(str(mp4_file_name)))
        # clip.write_gif(gif_file_name)

        

        # mp4_file_name = str(proteinPath/f"{self.protein_name}.mp4")
        # clip = mp.VideoFileClip(gif_file_name)
        # clip.write_videofile(mp4_file_name)

        # Legend box START

        # self.drawLegend(proteinDir)

        # Legend box END



# def stitch_photos(protein_path):
