delete all 
        load /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Code/PDB_Files/Predus_241_for_real/predus_4XXH_A.pdb
        color blue 
        set cartoon_transparency,0.75
        select ann, resi 62+64+73+78+82+85+94+96+97+98+99+110+116+117+118+218+249+272+273
        indicate bycalpha ann
        create annotated, indicate
        select pred, resi 272+89+117+97+273+98+275+269+85+99+116+268+276+96+271+72+250+86+94+82+64+118+256+71+249+101+258+83+252
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
        png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/Images_sphere/4XXH.A/4XXH.A_logreg.png,width=900, height=900,ray=1
        quit