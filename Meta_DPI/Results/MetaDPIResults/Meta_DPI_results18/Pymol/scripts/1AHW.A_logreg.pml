delete all 
    fetch 1AHW.A
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 30+32+50+91+92+93+94+96+530+531+532+533+552+554+555+557+559+600+601+602
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 602+50+32+601+49+600+53+531+532+30+54+554+533+552+31+92+557+56+555+559+52+558+93+606+576+530+60+57+96+577+91+599+556+28+161
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results18/Pymol/Images/1AHW.A/1AHW.A_logreg.png,width=900, height=900,dpi = 350,ray=1
    quit