delete all 
    load /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Code/PDB_Files/Predus_241_for_real/predus_1ACB_I.pdb
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 41+42+43+44+45+46+47+48+49+55+68
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 49+35+8+22+47+36+41+42+32+43+33+37+56+68+31+53+38+48+45+44
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/Images/1ACB.I/1ACB.I_dockpred.png,width=900, height=900,ray=1
    quit