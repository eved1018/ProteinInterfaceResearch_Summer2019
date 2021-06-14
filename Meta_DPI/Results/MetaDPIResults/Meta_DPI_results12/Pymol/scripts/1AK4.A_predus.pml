delete all 
    fetch 1AK4.A
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 55+60+63+71+72+73+102+111+121
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 71+121+120+81+122+79+72+74+124+103+80+68+84+37+118+125+70+126+82+123+104+54+105+4+67+102
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results12/Pymol/Images/1AK4.A/1AK4.A_predus.png,width=900, height=900,ray=1
    quit