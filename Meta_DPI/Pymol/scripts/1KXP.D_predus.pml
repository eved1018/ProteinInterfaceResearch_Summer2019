delete all 
        load /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Code/PDB_Files/Predus_241_for_real/predus_1KXP_D.pdb
        color blue 
        set cartoon_transparency,0.75
        select ann, resi 134+136+137+138+139+140+141+143+167+196+203+205+207+210+211+214+218+311+314+413+414+415+416+450+451+456
        indicate bycalpha ann
        create annotated, indicate
        select pred, resi 21+19+18+20+17+414+23+22+417+412+127+126+420+416+413+24+25+26+415+28+27+30+29+133+132+135+134+411+131+128+410+419+51+136+409+31
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
        png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/Images_sphere/1KXP.D/1KXP.D_predus.png,width=900, height=900,ray=1
        quit