delete all 
    fetch 1BUH.A
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 207+208+209+210+213+235+237+239+240+241+242+243
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 150+272+213+241+232+243+207+209+217+239+206+208+242+229+240+210+182+228+151+237+234+214+153+271+156+51+154+270+47+231+200
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/images_350dpi//Images/1BUH.A/1BUH.A_logreg.png,width=900, height=900,dpi = 350,ray=1
    quit