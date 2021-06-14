delete all 
    fetch 1AK4.A
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 55+60+63+71+72+73+102+111+121
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 121+148+60+59+120+46+125+45+118+57+55+44+149+58+76+117+67+49+70+68+47+69+80+144+105+50
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results12/Pymol/Images/1AK4.A/1AK4.A_dockpred.png,width=900, height=900,ray=1
    quit