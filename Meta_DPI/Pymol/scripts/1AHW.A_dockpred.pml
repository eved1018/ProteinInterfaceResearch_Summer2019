delete all 
    load /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Code/PDB_Files/Predus_241_for_real/predus_1AHW_A.pdb
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 30+32+50+91+92+93+94+96+530+531+532+533+552+554+555+557+559+600+601+602
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 602+50+32+601+49+600+533+53+30+532+531+603+31+92+54+554+552+52+56+96+91+55+605+555+599+93+598+557+606+501+530+94+57+559+502
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/Images/1AHW.A/1AHW.A_dockpred.png,width=900, height=900,ray=1
    quit