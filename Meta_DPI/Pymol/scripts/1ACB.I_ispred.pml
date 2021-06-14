delete all 
    load /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Code/PDB_Files/Predus_241_for_real/predus_1ACB_I.pdb
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 41+42+43+44+45+46+47+48+49+55+68
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 46+47+42+44+45+41+27+8+55+43+49+28+48+50+53+14+9+33+56+40
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/Images/1ACB.I/1ACB.I_ispred.png,width=900, height=900,ray=1
    quit