delete all 
    fetch 1FC2.D
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 251+252+253+254+309+311+432+433+434+435
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 395+397+398+297+407+296+264+394+405+393+399+298+392+366+400+239+351+349+396+267+370+241+294+347+300+301+265+334+314
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/images_350dpi//Images/1FC2.D/1FC2.D_rfscore.png,width=900, height=900,dpi = 350,ray=1
    quit