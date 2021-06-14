delete all 
    fetch 1AK4.A
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 55+60+63+71+72+73+102+111+121
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 121+71+103+72+125+74+126+104+73+165+148+55+68+69+102+60+76+46+45+149+44+120+54+124+107+105
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results12/Pymol/Images/1AK4.A/1AK4.A_logreg.png,width=900, height=900,ray=1
    quit