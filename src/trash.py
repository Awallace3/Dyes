def lumo(cam,pbe):
    lumo_lsf = [0.76, 0.67]
    lumo = lumo_lsf[0] * cam + lumo_lsf[1] * pbe



    return lumo

print(lumo(-2.1698,-2.981))