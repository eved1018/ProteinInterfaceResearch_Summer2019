delete all 
    fetch 1BUH.A
    color blue 
    set cartoon_transparency,0.75
    select ann, resi 207+208+209+210+213+235+237+239+240+241+242+243
    indicate bycalpha ann
    create annotated, indicate
    select pred, resi 38+39+70+72+71+2+161+157+158+122+159+77+179+178+14+160+37+4+27+23+1+3+152+163+162+73+26+74+24+177+34
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
    png /Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Meta_DPI/Pymol/images_350dpi//Images/1BUH.A/1BUH.A_predus.png,width=900, height=900,dpi = 350,ray=1
    quit