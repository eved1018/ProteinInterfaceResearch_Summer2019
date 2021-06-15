delete all 
    fetch 1ACB.E
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 39+41+57+58+146+191+192+193+195+214+215+216+218
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 96+192+39+141+57+146+90+218+149+193+59+37+94+145+216+151+219+174+175+97+215+41+89+36+189+35+99+217+190
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results27/Pymol/Images/1ACB.E/1ACB.E_rfscore.png,width=900, height=900,dpi = 350,ray=1
    quit