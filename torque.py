import femm
import numpy as np
import matplotlib.pyplot as plt
import resave

angulo_total = 72
cambio_angulo = 6
cambios = angulo_total//cambio_angulo

delta = 10
delta_rad = delta*np.pi/180

femm.openfemm()
femm.opendocument(r'MaquinaTrabajoABC.FEM')  

output_file = f"torques_{delta}.txt"

Imax = 1
Fase_A = np.linspace(0,2*np.pi,cambios+1)[:-1]
Fase_B = np.linspace(0,2*np.pi,cambios+1)[:-1]
Fase_C = np.linspace(0,2*np.pi,cambios+1)[:-1]

for i in range(cambios):
    Fase_A[i] = Imax*np.cos(Fase_A[i] + delta_rad)
    Fase_B[i] = Imax*np.cos(Fase_B[i] + delta_rad + (2*np.pi/3))
    Fase_C[i] = Imax*np.cos(Fase_C[i] + delta_rad + (4*np.pi/3))

rotation_angle = cambio_angulo
for i in range(cambios):
    print(f"Generando torque {i+1}/{cambios} con ángulo {i}°")

    femm.mi_setcurrent("A", Fase_A[i])
    femm.mi_setcurrent("B", Fase_B[i])
    femm.mi_setcurrent("C", Fase_C[i])

    try:
        femm.mi_analyze()
    except Exception as e:
        print(f"Error en mi_analyze en el fotograma {i}: {e}")
        femm.closefemm()
        exit(1)
    
    try:
        femm.mi_loadsolution()
    except Exception as e:
        print(f"Error en mi_loadsolution en el fotograma {i}: {e}")
        femm.closefemm()
        exit(1)
    
    femm.mo_groupselectblock(1)
    try:
        torque = femm.mo_blockintegral(22)
    except Exception as e:
        print(f"Error calculating torque at frame {i}: {e}")
        femm.closefemm()
        exit(1)
    femm.mo_clearblock()

    # Write torque to file
    with open(output_file, "a") as f:
        f.write(f"{torque}\n")

    femm.mo_close()

    femm.mi_selectgroup(1)  
    femm.mi_moverotate(0, 0, rotation_angle)  
    femm.mi_clearselected()
    
