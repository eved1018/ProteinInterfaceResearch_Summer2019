delete all 
    fetch 1AK4.A
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 55+60+63+71+72+73+102+111+121
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 121+125+116+148+79+60+144+59+55+122+72+16+17+81+51+27+41+71+68+1+76+102+145+93+28+45
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results18/Pymol/Images/1AK4.A/1AK4.A_rfscore.png,width=900, height=900,dpi = 350,ray=1
    quit