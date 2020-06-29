from pymol import cmd

file_name = "/home/shahar/Desktop/test.png"

cmd.fetch("2vpf", async_=0)


cmd.set("opaque_background", "on")


cmd.zoom(complete=1)
cmd.mset("1 x 12")

cmd.mview("store", 1)

cmd.mview("store", 12, power=1)


cmd.turn("y", "180")
cmd.mview("store", 6, power=1)
# cmd.movie.produce("/home/shahar/Desktop/test.mpg", quality=100)
cmd.mpng("/home/shahar/Desktop/pymol_test/out", width=900, height=900)

"""
python

cmd.zoom(complete=1)
cmd.scene("001", "store")

python end

"""

"""
python

cmd.rotate("y", "180")
cmd.movie.produce("/home/shahar/Desktop/test.mpg")


python end

"""

"""
python
cmd.zoom(complete=1)
cmd.mset("1 x 12")

cmd.mview("store", 1)

cmd.mview("store", 12, power=1)


cmd.turn("y", "180")
cmd.mview("store", 6, power=1)
cmd.movie.produce("/home/shahar/Desktop/test.mpg")

python end

"""



"""
python
cmd.scene("001", "delete")

python end
"""