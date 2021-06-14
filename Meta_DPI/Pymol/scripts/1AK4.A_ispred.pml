delete all 
    load /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Code/PDB_Files/Predus_241_for_real/predus_1AK4_A.pdb
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 55+60+63+71+72+73+102+111+121
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 121+74+72+165+103+73+126+104+71+102+69+125+54+55+68+107+1+76+149+44+82+88+43+124+105+164
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/Images/1AK4.A/1AK4.A_ispred.png,width=900, height=900,ray=1
    quit