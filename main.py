import femm
import numpy as np
import time

def rot_mat(angle):
    matrix = np.array(((np.cos(angle), -np.sin(angle)),
                       (np.sin(angle),  np.cos(angle))))
    return matrix

def rot_vec(vec, angle):
    R = rot_mat(angle)
    new_vec = R.dot(vec)
    return new_vec

out_path = "Maquina.FEM"

## machine variables
ancho_cruzeta = 1
largo_cruzeta = 2
largo_iman = 0.5
radio_interno_estator = 5
radio_externo_estator = 6
air_gap_externo = 1
min_air_gap = 0.1
ancho_bobinas = 0.5
N_bobinas = 100
bobinado_libre = 1
largo_bobinas = radio_interno_estator - largo_cruzeta - largo_iman - bobinado_libre
rr = np.sqrt((ancho_cruzeta/2)**2 + (largo_cruzeta + largo_iman)**2)

## materials
mat0 = "Air"         ## air
mat1 = "Pure Iron"   ## core
mat2 = "N35"         ## magnet
mat3 = "22 AWG"      ## wire

## Create femm model
femm.openfemm()
femm.newdocument(0) # 0 = magnetic problem

femm.mi_getmaterial(mat0)
femm.mi_getmaterial(mat1)
femm.mi_getmaterial(mat2)
femm.mi_getmaterial(mat3)

femm.mi_addblocklabel(ancho_cruzeta/2+0.1, ancho_cruzeta/2+0.1) # Add a new block label at (x,y)
femm.mi_selectlabel(ancho_cruzeta/2+0.1, ancho_cruzeta/2+0.1)
femm.mi_setblockprop(mat0, 1, 1, "0", 0, 0, 0) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns 
femm.mi_clearselected()

femm.mi_addblocklabel(0,0) # Add a new block label at (x,y)
femm.mi_selectlabel(0,0)
femm.mi_setblockprop(mat1, 1, 1, "0", 0, 0, 0) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns 
femm.mi_clearselected()

femm.mi_drawrectangle(ancho_cruzeta/2, -ancho_cruzeta/2, largo_cruzeta, ancho_cruzeta/2) #x1,y1,x2,y2           #cruzeta
femm.mi_drawrectangle(largo_cruzeta, -ancho_cruzeta/2, largo_cruzeta + largo_iman, ancho_cruzeta/2) #x1,y1,x2,y2  #iman

femm.mi_addblocklabel(largo_cruzeta/2,0) # Add a new block label at (x,y)
femm.mi_selectlabel(largo_cruzeta/2,0)
femm.mi_setblockprop(mat1, 1, 1, "0", 0, 0, 0) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns
femm.mi_clearselected()

femm.mi_addblocklabel(largo_cruzeta + largo_iman/2,0) # Add a new block label at (x,y)
femm.mi_selectlabel(largo_cruzeta + largo_iman/2,0)
femm.mi_setblockprop(mat2, 1, 1, "0", 180, 0, 0) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns 
femm.mi_clearselected()

femm.mi_selectrectangle(ancho_cruzeta/2, -ancho_cruzeta/2, largo_cruzeta+largo_iman, ancho_cruzeta/2,4)
femm.mi_copyrotate2(0,0,90,3,4) #bx, by, angle, copies, type

femm.mi_selectlabel(largo_cruzeta + largo_iman/2,0)
femm.mi_setblockprop(mat2, 1, 1, "0", 0, 0, 0) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns 
femm.mi_clearselected()

femm.mi_selectlabel(-largo_cruzeta - largo_iman/2,0)
femm.mi_setblockprop(mat2, 1, 1, "0", 180, 0, 0) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns 
femm.mi_clearselected()

femm.mi_drawarc(radio_interno_estator, 0, -radio_interno_estator, 0, 180, 1) #x1,y1,x2,y2,angle,maxseg
femm.mi_drawarc(-radio_interno_estator, 0, radio_interno_estator, 0, 180, 1) #x1,y1,x2,y2,angle,maxseg
femm.mi_drawarc(radio_externo_estator, 0, -radio_externo_estator, 0, 180, 1) #x1,y1,x2,y2,angle,maxseg
femm.mi_drawarc(-radio_externo_estator, 0, radio_externo_estator, 0, 180, 1) #x1,y1,x2,y2,angle,maxseg
femm.mi_drawarc(radio_externo_estator + air_gap_externo, 0, -radio_externo_estator - air_gap_externo, 0, 180, 1) #x1,y1,x2,y2,angle,maxseg
femm.mi_drawarc(-radio_externo_estator - air_gap_externo, 0, radio_externo_estator + air_gap_externo, 0, 180, 1) #x1,y1,x2,y2,angle,maxseg

femm.mi_addblocklabel(radio_interno_estator/2+radio_externo_estator/2,0) # Add a new block label at (x,y) ### cilindro estator
femm.mi_selectlabel(radio_interno_estator/2+radio_externo_estator/2,0)
femm.mi_setblockprop(mat1, 1, 1, "0", 0, 0, 0) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns 
femm.mi_clearselected()

femm.mi_addblocklabel(radio_externo_estator + air_gap_externo/2,0) # Add a new block label at (x,y)   ### air gap externo estator
femm.mi_selectlabel(radio_externo_estator + air_gap_externo/2,0)
femm.mi_setblockprop(mat0, 1, 1, "0", 0, 0, 0) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns 
femm.mi_clearselected()

femm.mi_drawline(radio_interno_estator, ancho_cruzeta/2, rr + min_air_gap, ancho_cruzeta/2)
femm.mi_drawline(rr + min_air_gap, ancho_cruzeta/2, rr + min_air_gap, -ancho_cruzeta/2)
femm.mi_drawline(rr + min_air_gap, -ancho_cruzeta/2, radio_interno_estator, -ancho_cruzeta/2)

femm.mi_addblocklabel(rr + min_air_gap + 0.1, 0) # Add a new block label at (x,y)                       ### barras estator
femm.mi_selectlabel(rr + min_air_gap + 0.1, 0)
femm.mi_setblockprop(mat1, 1, 1, "0", 0, 0, 0) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns 
femm.mi_clearselected()

femm.mi_drawrectangle(radio_interno_estator - largo_bobinas - bobinado_libre/2, ancho_cruzeta/2 + 0.1, radio_interno_estator - bobinado_libre/2, ancho_cruzeta/2 + 0.1 + ancho_bobinas) #x1,y1,x2,y2 bobina superior
femm.mi_drawrectangle(radio_interno_estator - largo_bobinas - bobinado_libre/2, -ancho_cruzeta/2 -0.1 - ancho_bobinas, radio_interno_estator - bobinado_libre/2, - ancho_cruzeta/2 - 0.1) #x1,y1,x2,y2 bobina inferior

centro_bobina_superior =  [radio_interno_estator - bobinado_libre/2 - largo_bobinas/2, ancho_cruzeta/2 + 0.1 + ancho_bobinas/2]
centro_bobina_inferior =  [radio_interno_estator - bobinado_libre/2 - largo_bobinas/2, -ancho_cruzeta/2 - 0.1 - ancho_bobinas/2]
bobinas_superiores =  [rot_vec(centro_bobina_superior, 60*i*np.pi/180) for i in range(6)]
bobinas_inferiores =  [rot_vec(centro_bobina_inferior, 60*i*np.pi/180) for i in range(6)]

femm.mi_addcircprop("A", 0, 1)   #circuitname’, i, circuittype
femm.mi_addcircprop("B", 0, 1)   #circuitname’, i, circuittype
femm.mi_addcircprop("C", 0, 1)   #circuitname’, i, circuittype

femm.mi_addblocklabel(centro_bobina_superior[0], centro_bobina_superior[1]) # Add a new block label at (x,y)
femm.mi_selectlabel(centro_bobina_superior[0], centro_bobina_superior[1])
femm.mi_setblockprop(mat3, 1, 1, "A", 0, 0, N_bobinas) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns 
femm.mi_clearselected()

femm.mi_addblocklabel(centro_bobina_inferior[0], centro_bobina_inferior[1]) # Add a new block label at (x,y)
femm.mi_selectlabel(centro_bobina_inferior[0], centro_bobina_inferior[1])
femm.mi_setblockprop(mat3, 1, 1, "A", 0, 0, -N_bobinas) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns 
femm.mi_clearselected()

femm.mi_selectrectangle(rr + min_air_gap, -ancho_cruzeta/2-0.1 - ancho_bobinas, radio_interno_estator, ancho_cruzeta/2 + 0.1 + ancho_bobinas, 4)
femm.mi_copyrotate2(0, 0, 60, 5, 4)

for bobina in enumerate(bobinas_superiores):
    if bobina[0]%3 == 0:
        cir = "A"
    elif bobina[0]%3 == 1:
        cir = "B"
    else:
        cir = "C"
    femm.mi_selectlabel(bobina[1][0], bobina[1][1])
    femm.mi_setblockprop(mat3, 1, 1, cir, 0, 0, N_bobinas) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns 
    femm.mi_clearselected()

for bobina in enumerate(bobinas_inferiores):
    if bobina[0]%3 == 0:
        cir = "A"
    elif bobina[0]%3 == 1:
        cir = "B"
    else:
        cir = "C"
    femm.mi_selectlabel(bobina[1][0], bobina[1][1])
    femm.mi_setblockprop(mat3, 1, 1, cir, 0, 0, -N_bobinas) #’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns 
    femm.mi_clearselected()
    


femm.mi_saveas(out_path)


time.sleep(5)