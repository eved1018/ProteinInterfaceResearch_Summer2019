delete all 
    fetch 1BUH.A
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 207+208+209+210+213+235+237+239+240+241+242+243
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 178+150+208+207+152+180+181+209+179+151+156+154+153+182+124+206+166+176+51+167+213+155+2+37+241+1+123+6+204+122+50
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/images_350dpi//Images/1BUH.A/1BUH.A_ispred.png,width=900, height=900,dpi = 350,ray=1
    quit