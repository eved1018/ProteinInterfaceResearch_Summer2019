delete all 
    fetch 1FC2.D
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 251+252+253+254+309+311+432+433+434+435
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 253+314+311+434+436+310+252+435+315+309+350+256+254+433+312+402+432+307+255+302+431+316+344+345+343+303+317+291+425
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/images_350dpi//Images/1FC2.D/1FC2.D_logreg.png,width=900, height=900,dpi = 350,ray=1
    quit