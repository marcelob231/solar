import numpy as np

def calcula_delta_media(_irr_glo, latitude, albedo):
    maior_min = 0
    resultado = []
    for i in range(51):
        irradiacoes_angulares = calculo(_irr_glo, i, latitude, albedo)
        menor = min(irradiacoes_angulares)
        angulo_min = i
        if menor > maior_min:
            maior_min = menor
            resultado = [angulo_min, irradiacoes_angulares]
    return resultado


def calculo(irr_glo, angle_module, latitude, albedo):
    sol_const = 1367

    if latitude < 0:
        angle_module = -1 * angle_module

    dia_media = [17, 47, 75, 105, 135, 162, 198, 228, 258, 288, 318, 344]

    def get_declinacao_rad(dia):
        return 23.45 * np.sin(2*np.pi*(284+dia)/365)

    def get_sunset(lat, declinacao):
        return np.arccos(-1*np.tan(np.deg2rad(lat))*np.tan(np.deg2rad(declinacao)))*180/np.pi

    def get_sunset_incli(lat, angulo, declinacao, sunsetflat):
        temp_sunset = np.arccos(-1*np.tan(np.deg2rad(lat-angulo))*np.tan(np.deg2rad(declinacao)))*180/np.pi
        if (temp_sunset <= sunsetflat):
            return temp_sunset
        else:
            return sunsetflat

    def get_h_zero(declinacao, sun_set, dia, lat, solconst):

        return 24/np.pi * solconst*(1+0.033*np.cos(2*np.pi*dia/365))*(np.cos(np.deg2rad(lat))*np.cos(np.deg2rad(declinacao))\
                *np.sin(np.deg2rad(sun_set))+sun_set*2*np.pi/360*np.sin(np.deg2rad(lat))*np.sin(np.deg2rad(declinacao)))

    def get_kt(h, h0):
        return h/h0

    def get_hd_h(kt):
        return 1.390-4.027*kt+5.531*kt**2-3.108*kt**3

    def get_rb(lat, angulo_mod, declinacao, sun_set, sun_set_incl):
        return (np.cos(np.deg2rad(lat-angulo_mod))*np.cos(np.deg2rad(declinacao))*np.sin(np.deg2rad(sun_set_incl))+np.deg2rad(sun_set_incl)*np.sin(np.deg2rad(lat-angulo_mod))*np.sin(np.deg2rad(declinacao)))/ \
                (np.cos(np.deg2rad(lat))*np.cos(np.deg2rad(declinacao))*np.sin(np.deg2rad(sun_set))+np.deg2rad(sun_set)*np.sin(np.deg2rad(lat))*np.sin(np.deg2rad(declinacao)))

    def get_hbt2(irra_gb, irra_df, rb, angu, alb):
        return irra_gb*(1-irra_df)*rb+irra_df*irra_gb*((1+np.cos(np.deg2rad(angu)))/2)+irra_gb*alb*((1-np.cos(np.deg2rad(angu)))/2)

    declinacao_meses = []
    sunset = []
    sunset_incl = []
    h_zero = []
    kt = []
    irra_dif = []
    rb = []
    hbt2 = []
    
    for i in range(12):
        declinacao_meses.append(get_declinacao_rad(dia_media[i]))
        sunset.append(get_sunset(latitude, declinacao_meses[i]))
        sunset_incl.append(get_sunset_incli(latitude, angle_module, declinacao_meses[i], sunset[i]))
        h_zero.append(get_h_zero(declinacao_meses[i], sunset[i], dia_media[i], latitude, sol_const))
        kt.append(get_kt(irr_glo[i], h_zero[i]))
        irra_dif.append(get_hd_h(kt[i]))
        rb.append(get_rb(latitude, angle_module, declinacao_meses[i], sunset[i], sunset_incl[i]))
        hbt2.append(get_hbt2(irr_glo[i], irra_dif[i], rb[i], angle_module, albedo))
	 
    hbt_kw = []
    for i in hbt2:
        hbt_kw.append(i / 1000)
    
    return hbt_kw




