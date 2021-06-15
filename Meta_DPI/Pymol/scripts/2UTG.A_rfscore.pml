delete all 
        load /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Code/PDB_Files/Predus_241_for_real/predus_2UTG_A.pdb
        color blue 
        set cartoon_transparency,0.75
        select ann, resi 3+5+6+28+29+34+37+45+55+59+62+63+66+69
        indicate bycalpha ann
        create annotated, indicate
        select pred, resi 40+6+34+59+66+28+2+62+63+3+69+1+56+29+41+30+5+67+37+60+4
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
        png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/Images_sphere/2UTG.A/2UTG.A_rfscore.png,width=900, height=900,ray=1
        quit