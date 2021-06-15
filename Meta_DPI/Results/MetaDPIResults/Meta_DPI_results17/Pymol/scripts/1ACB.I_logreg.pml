delete all 
    fetch 1ACB.I
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 41+42+43+44+45+46+47+48+49+55+68
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 47+46+42+44+45+48+49+43+8+41+50+27+55+53+28+33+51+35+68+70
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results17/Pymol/Images/1ACB.I/1ACB.I_logreg.png,width=900, height=900,dpi = 350,ray=1
    quit