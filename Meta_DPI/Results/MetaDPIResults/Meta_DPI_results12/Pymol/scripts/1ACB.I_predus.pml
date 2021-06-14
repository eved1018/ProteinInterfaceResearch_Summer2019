delete all 
    fetch 1ACB.I
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 41+42+43+44+45+46+47+48+49+55+68
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 48+47+49+51+50+45+70+46+43+53+44+68+33+42+31+32+26+69+35+23
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results12/Pymol/Images/1ACB.I/1ACB.I_predus.png,width=900, height=900,ray=1
    quit