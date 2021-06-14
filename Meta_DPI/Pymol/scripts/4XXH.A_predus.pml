delete all 
        load /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Code/PDB_Files/Predus_241_for_real/predus_4XXH_A.pdb
        color blue 
        set cartoon_transparency,0.75
        select ann, resi 62+64+73+78+82+85+94+96+97+98+99+110+116+117+118+218+249+272+273
        indicate bycalpha ann
        create annotated, indicate
        select pred, resi 250+256+254+252+253+89+249+85+255+64+222+248+87+93+62+218+117+99+274+72+91+92+98+245+96+86+101+119+71
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
        png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/Images_sphere/4XXH.A/4XXH.A_predus.png,width=900, height=900,ray=1
        quit