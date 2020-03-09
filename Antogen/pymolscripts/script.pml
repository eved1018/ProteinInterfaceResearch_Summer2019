
delete all
fetch 1d7p, async = 0

# Blue -- Predus (33.266+33.732+32.928+33.154+35.223+35.957+35.887+37.406+31.985+31.138+31.468+31.999+29.664+28.898+29.159)
# Red -- Annotated (2196+2197+2198+2199+2200+2215+2220+2222+2250+2251+2252+2253+2255+2315+2316)

color white; color blue, resi 33.266+33.732+32.928+33.154+35.223+35.957+35.887+37.406+31.985+31.138+31.468+31.999+29.664+28.898+29.159; color red, resi 2196+2197+2198+2199+2200+2215+2220+2222+2250+2251+2252+2253+2255+2315+2316 
color green, resi 

select color blue; show spheres, SEL
select color red; show spheres, SEL


remove resn hoh
zoom complete=1

# blue
orient resi 33.266+33.732+32.928+33.154+35.223+35.957+35.887+37.406+31.985+31.138+31.468+31.999+29.664+28.898+29.159 
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center 1d7p


python

import pymolpredus

rotator = pymolpredus.Rotate("1d7p", "", "33.266+33.732+32.928+33.154+35.223+35.957+35.887+37.406+31.985+31.138+31.468+31.999+29.664+28.898+29.159")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/1d7p.png, width=900, height=900,ray=1, dpi=500



delete all

delete all
fetch 1hrc, async = 0

# Blue -- Predus (1+2+3+4+5+6+7+8+9+10)
# Red -- Annotated (100+103+104+36+37+60+61+62+96+99)

color white; color blue, resi 1+2+3+4+5+6+7+8+9+10; color red, resi 100+103+104+36+37+60+61+62+96+99 
color green, resi 

select color blue; show spheres, SEL
select color red; show spheres, SEL


remove resn hoh
zoom complete=1

# blue
orient resi 1+2+3+4+5+6+7+8+9+10 
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center 1hrc


python

import pymolpredus

rotator = pymolpredus.Rotate("1hrc", "", "1+2+3+4+5+6+7+8+9+10")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/1hrc.png, width=900, height=900,ray=1, dpi=500



delete all

delete all
fetch 1kdc, async = 0

# Blue -- Predus (6+7+8+10+11+12+13+14+15+16+17+18+19+20+21+22+23)
# Red -- Annotated (105+106+120+121+124+127+135+57+60+61+64+68+70+95+96+97+98)

color white; color blue, resi 6+7+8+10+11+12+13+14+15+16+17+18+19+20+21+22+23; color red, resi 105+106+120+121+124+127+135+57+60+61+64+68+70+95+96+97+98 
color green, resi 9

select color blue; show spheres, SEL
select color red; show spheres, SEL
; select color green; show spheres, SEL
; label resi 9, ID; set label_position,(3,2,1)
remove resn hoh
zoom complete=1

# blue
orient resi 6+7+8+10+11+12+13+14+15+16+17+18+19+20+21+22+23 
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center 1kdc


python

import pymolpredus

rotator = pymolpredus.Rotate("1kdc", "9", "6+7+8+10+11+12+13+14+15+16+17+18+19+20+21+22+23")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/1kdc.png, width=900, height=900,ray=1, dpi=500



delete all

delete all
fetch 1poh, async = 0

# Blue -- Predus (5+6+7+8+9+10+11+12+13)
# Red -- Annotated (34+66+67+68+70+71+72+75+76)

color white; color blue, resi 5+6+7+8+9+10+11+12+13; color red, resi 34+66+67+68+70+71+72+75+76 
color green, resi 1+2+3+4

select color blue; show spheres, SEL
select color red; show spheres, SEL
; select color green; show spheres, SEL
; label resi 1+2+3+4, ID; set label_position,(3,2,1)
remove resn hoh
zoom complete=1

# blue
orient resi 5+6+7+8+9+10+11+12+13 
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center 1poh


python

import pymolpredus

rotator = pymolpredus.Rotate("1poh", "1+2+3+4", "5+6+7+8+9+10+11+12+13")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/1poh.png, width=900, height=900,ray=1, dpi=500



delete all

delete all
fetch 2hmg.A, async = 0

# Blue -- Predus ()
# Red -- Annotated ()

color white; color blue, resi ; color red, resi  
color green, resi 

select color blue; show spheres, SEL
select color red; show spheres, SEL


remove resn hoh
zoom complete=1

# blue
orient resi  
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center 2hmg.A


python

import pymolpredus

rotator = pymolpredus.Rotate("2hmg.A", "", "")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/2hmg.A.png, width=900, height=900,ray=1, dpi=500



delete all

delete all
fetch 2viu, async = 0

# Blue -- Predus (9+10+11+12+13+14+15+16+17+18+19+20+21+22+23+24+25)
# Red -- Annotated (129+130+131+132+133+134+135+136+137+155+156+157+158+159+190+193+194)

color white; color blue, resi 9+10+11+12+13+14+15+16+17+18+19+20+21+22+23+24+25; color red, resi 129+130+131+132+133+134+135+136+137+155+156+157+158+159+190+193+194 
color green, resi 

select color blue; show spheres, SEL
select color red; show spheres, SEL


remove resn hoh
zoom complete=1

# blue
orient resi 9+10+11+12+13+14+15+16+17+18+19+20+21+22+23+24+25 
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center 2viu


python

import pymolpredus

rotator = pymolpredus.Rotate("2viu", "", "9+10+11+12+13+14+15+16+17+18+19+20+21+22+23+24+25")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/2viu.png, width=900, height=900,ray=1, dpi=500



delete all

delete all
fetch 2vpf, async = 0

# Blue -- Predus (13+14)
# Red -- Annotated (17+21)

color white; color blue, resi 13+14; color red, resi 17+21 
color green, resi 

select color blue; show spheres, SEL
select color red; show spheres, SEL


remove resn hoh
zoom complete=1

# blue
orient resi 13+14 
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center 2vpf


python

import pymolpredus

rotator = pymolpredus.Rotate("2vpf", "", "13+14")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/2vpf.png, width=900, height=900,ray=1, dpi=500



delete all

delete all
fetch 3lzt, async = 0

# Blue -- Predus (1+2+3+4+5+6+7+8+9+10+11+12+13+14)
# Red -- Annotated (41+43+45+46+47+48+49+50+51+53+67+68+81+84)

color white; color blue, resi 1+2+3+4+5+6+7+8+9+10+11+12+13+14; color red, resi 41+43+45+46+47+48+49+50+51+53+67+68+81+84 
color green, resi 

select color blue; show spheres, SEL
select color red; show spheres, SEL


remove resn hoh
zoom complete=1

# blue
orient resi 1+2+3+4+5+6+7+8+9+10+11+12+13+14 
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center 3lzt


python

import pymolpredus

rotator = pymolpredus.Rotate("3lzt", "", "1+2+3+4+5+6+7+8+9+10+11+12+13+14")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/3lzt.png, width=900, height=900,ray=1, dpi=500



delete all

delete all
fetch 7nn9, async = 0

# Blue -- Predus (82+83+84+85+86+87+88+89+90+91+92+93+94+95+96+97+98+99+100+101+102)
# Red -- Annotated (326+327+328+329+343+344+345+347+367+368+369+370+372+399+400+401+402+403+431+432+463)

color white; color blue, resi 82+83+84+85+86+87+88+89+90+91+92+93+94+95+96+97+98+99+100+101+102; color red, resi 326+327+328+329+343+344+345+347+367+368+369+370+372+399+400+401+402+403+431+432+463 
color green, resi 

select color blue; show spheres, SEL
select color red; show spheres, SEL


remove resn hoh
zoom complete=1

# blue
orient resi 82+83+84+85+86+87+88+89+90+91+92+93+94+95+96+97+98+99+100+101+102 
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center 7nn9


python

import pymolpredus

rotator = pymolpredus.Rotate("7nn9", "", "82+83+84+85+86+87+88+89+90+91+92+93+94+95+96+97+98+99+100+101+102")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/7nn9.png, width=900, height=900,ray=1, dpi=500



delete all

delete all
fetch 8lyz, async = 0

# Blue -- Predus (1+2+3+4+5+6+7+8+9+10+11+12+13+14+15)
# Red -- Annotated (102+116+117+118+119+120+121+125+129+18+19+22+23+24+27)

color white; color blue, resi 1+2+3+4+5+6+7+8+9+10+11+12+13+14+15; color red, resi 102+116+117+118+119+120+121+125+129+18+19+22+23+24+27 
color green, resi 

select color blue; show spheres, SEL
select color red; show spheres, SEL


remove resn hoh
zoom complete=1

# blue
orient resi 1+2+3+4+5+6+7+8+9+10+11+12+13+14+15 
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center 8lyz


python

import pymolpredus

rotator = pymolpredus.Rotate("8lyz", "", "1+2+3+4+5+6+7+8+9+10+11+12+13+14+15")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/8lyz.png, width=900, height=900,ray=1, dpi=500



delete all

delete all
fetch 1a43, async = 0

# Blue -- Predus (148+149+150+151+152+153+154+155+156+157+158)
# Red -- Annotated (187+204+205+206+207+208+209+210+212+213+217)

color white; color blue, resi 148+149+150+151+152+153+154+155+156+157+158; color red, resi 187+204+205+206+207+208+209+210+212+213+217 
color green, resi 

select color blue; show spheres, SEL
select color red; show spheres, SEL


remove resn hoh
zoom complete=1

# blue
orient resi 148+149+150+151+152+153+154+155+156+157+158 
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center 1a43


python

import pymolpredus

rotator = pymolpredus.Rotate("1a43", "", "148+149+150+151+152+153+154+155+156+157+158")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/1a43.png, width=900, height=900,ray=1, dpi=500



delete all

delete all
fetch 1bv1, async = 0

# Blue -- Predus (1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+16+17)
# Red -- Annotated (42+43+44+45+46+47+48+49+50+51+52+53+70+72+76+87+97)

color white; color blue, resi 1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+16+17; color red, resi 42+43+44+45+46+47+48+49+50+51+52+53+70+72+76+87+97 
color green, resi 

select color blue; show spheres, SEL
select color red; show spheres, SEL


remove resn hoh
zoom complete=1

# blue
orient resi 1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+16+17 
#unset opaque_background

# removes the shadows that give the appearannce of depth
set depth_cue, 0  

center 1bv1


python

import pymolpredus

rotator = pymolpredus.Rotate("1bv1", "", "1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+16+17")
rotator.take_pictures()


python end

# the directory to which the png files are outputted
# png ../../Antogen/pymolimages/1bv1.png, width=900, height=900,ray=1, dpi=500



delete all
