delete all 
    fetch 1FC2.D
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 251+252+253+254+309+311+432+433+434+435
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 241+243+395+301+296+398+397+396+264+244+334+404+239+297+262+394+375+392+242+393+246+405+294+399+407+400+336+339+260
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/images_350dpi//Images/1FC2.D/1FC2.D_dockpred.png,width=900, height=900,dpi = 350,ray=1
    quit