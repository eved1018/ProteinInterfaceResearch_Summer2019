delete all 
    fetch 1ACB.E
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 39+41+57+58+146+191+192+193+195+214+215+216+218
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 192+191+146+172+99+98+216+218+217+169+190+175+171+189+215+193+174+145+195+40+153+97+41+219+173+143+151+226+150
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results18/Pymol/Images/1ACB.E/1ACB.E_predus.png,width=900, height=900,dpi = 350,ray=1
    quit