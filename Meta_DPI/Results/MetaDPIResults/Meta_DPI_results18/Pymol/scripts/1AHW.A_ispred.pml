delete all 
    fetch 1AHW.A
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 30+32+50+91+92+93+94+96+530+531+532+533+552+554+555+557+559+600+601+602
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 53+54+50+531+557+558+554+606+600+576+601+92+552+602+32+533+56+577+532+559+60+49+45+556+127+165+93+161+530+573+572+555+30+574+57
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Results/MetaDPIResults/Meta_DPI_results18/Pymol/Images/1AHW.A/1AHW.A_ispred.png,width=900, height=900,dpi = 350,ray=1
    quit