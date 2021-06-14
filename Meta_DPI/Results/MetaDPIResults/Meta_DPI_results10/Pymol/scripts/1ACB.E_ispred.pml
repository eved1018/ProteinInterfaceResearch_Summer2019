delete all 
    fetch 1ACB.E
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 39+41+57+58+146+191+192+193+195+214+215+216+218
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 41+39+146+57+98+97+175+239+149+240+216+75+177+96+37+244+59+93+74+245+242+94+89+90+36+215+218+193+237
    indicate bycalpha pred
    create pred_res, indicate
    show sphere, annotated
    color pink, annotated
    set sphere_transparency, 0.5,annotated
    show sphere, pred_res
    set sphere_scale,0.5,pred_res
    color green, pred_res
    set sphere_transparency,0,pred_res
    set cartoon_transparency,1,pred_res
    remove resn hoh
    zoom complete=1
    bg_color white 
    set ray_opaque_background, 1
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results10/Pymol/Images/1ACB.E/1ACB.E_ispred.png,width=900, height=900,ray=1
    quit