delete all 
        load /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Code/PDB_Files/Predus_241_for_real/predus_4XXH_A.pdb
        color blue 
        set cartoon_transparency,0.75
        select ann, resi 62+64+73+78+82+85+94+96+97+98+99+110+116+117+118+218+249+272+273
        indicate bycalpha ann
        create annotated, indicate
        select pred, resi 97+96+272+117+72+113+82+98+94+89+78+110+273+269+116+86+99+85+73+268+62+75+271+118+218+231+90+257+61
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
        png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/Images_sphere/4XXH.A/4XXH.A_vorffip.png,width=900, height=900,ray=1
        quit