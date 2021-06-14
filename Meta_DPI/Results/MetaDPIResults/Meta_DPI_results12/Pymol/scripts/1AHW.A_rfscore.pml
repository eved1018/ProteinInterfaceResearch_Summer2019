delete all 
    fetch 1AHW.A
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 30+32+50+91+92+93+94+96+530+531+532+533+552+554+555+557+559+600+601+602
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 50+533+602+32+53+601+49+606+600+557+532+531+603+54+554+56+552+605+558+559+92+31+556+45+502+550+30+41+675+91+96+598+599+60+93
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results12/Pymol/Images/1AHW.A/1AHW.A_rfscore.png,width=900, height=900,ray=1
    quit