import femm
import os
import imageio
import numpy as np
import time 

# Funciones auxiliares
def rot_mat(angle):
    matrix = np.array(((np.cos(angle), -np.sin(angle)),
                       (np.sin(angle),  np.cos(angle))))
    return matrix

def rot_vec(vec, angle):
    R = rot_mat(angle)
    new_vec = R.dot(vec)
    return new_vec

# Parámetros de la animación
num_steps = 360  # Número de fotogramas
rotation_angle = 360 / num_steps  # Ángulo por fotograma
images = []  # Lista para almacenar las rutas de las imágenes

output_folder = "frames"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Parámetros de calculo de flujo
puntos = [[54, -6.3], [54, 6.3]]
slots = []
for i in range(12):
    punto_1 = rot_vec(puntos[0], i*np.pi/6)
    punto_2 = rot_vec(puntos[1], i*np.pi/6)
    slots.append([punto_1, punto_2])

output_file = "Flujos.txt"

femm.openfemm()

femm.opendocument(r'MaquinaTrabajoABC_SA.FEM')  

# Bucle para cada paso de rotación
for i in range(num_steps):
    angle = i * rotation_angle
    print(f"Generando fotograma {i+1}/{num_steps} con ángulo {angle}°")
    
    # Rotar el rotor (Grupo 1)
    femm.mi_selectgroup(1)  
    femm.mi_moverotate(0, 0, rotation_angle)  
    femm.mi_clearselected()
    
    # Resolver el problema
    try:
        femm.mi_analyze()
    except Exception as e:
        print(f"Error en mi_analyze en el fotograma {i}: {e}")
        femm.closefemm()
        exit(1)
    
    # Cargar la solución
    try:
        femm.mi_loadsolution()
    except Exception as e:
        print(f"Error en mi_loadsolution en el fotograma {i}: {e}")
        femm.closefemm()
        exit(1)

    try:
        femm.mo_showdensityplot(1, 0, 0, 1, 'bmag') 
    except Exception as e:
        print(f"Error en mo_showdensityplot en el fotograma {i}: {e}")
        femm.closefemm()
        exit(1)

    image_path = os.path.join(output_folder, f'frame_{i:03d}.png')
    try:
        femm.mo_savebitmap(image_path)
    except Exception as e:
        print(f"Error al guardar la imagen en el fotograma {i}: {e}")
        femm.closefemm()
        exit(1)
    
    images.append(image_path)
    
    try:
        flujos = []
        for slot in slots:
            femm.mo_seteditmode("contour")
            femm.mo_addcontour(slot[0][0], slot[0][1])
            femm.mo_addcontour(slot[1][0], slot[1][1]) 
            flux_density = femm.mo_lineintegral(0)
            flujos.append(str(flux_density[0]))
            femm.mo_clearcontour()
        f = open(output_file, "a")
        f.write(str(flujos))
        f.write("\n")
        f.close()
    except Exception as e:
        print(f"Error el calculo del flujo {i}: {e}")
        femm.closefemm()
        exit(1)

    femm.mo_close()

femm.closefemm()

# Crear el GIF animado
gif_path = "animacion.gif"
try:
    with imageio.get_writer(gif_path, mode='I', duration=0.1) as writer:
        for image_file in images:
            image = imageio.imread(image_file)
            writer.append_data(image)
    print(f"GIF creado exitosamente en {gif_path}")
except Exception as e:
    print(f"Error al crear el GIF: {e}")

# Limpiar imágenes 
for image in images:
    try:
        os.remove(image)
    except Exception as e:
        print(f"Error al eliminar la imagen {image}: {e}")
