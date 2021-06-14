delete all 
        load /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Code/PDB_Files/Predus_241_for_real/predus_1KXP_D.pdb
        color blue 
        set cartoon_transparency,0.75
        select ann, resi 134+136+137+138+139+140+141+143+167+196+203+205+207+210+211+214+218+311+314+413+414+415+416+450+451+456
        indicate bycalpha ann
        create annotated, indicate
        select pred, resi 26+22+85+23+21+27+25+19+88+20+18+84+29+30+17+24+82+81+28+31+92+52+96+105+83+48+95+126+106+33+98+431+89+53+99+104
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
        png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/Images_sphere/1KXP.D/1KXP.D_meta-ppisp.png,width=900, height=900,ray=1
        quit