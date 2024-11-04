import femm
import os
import imageio

# Parámetros de la animación
num_steps = 36  # Número de fotogramas
rotation_angle = 360 / num_steps  # Ángulo por fotograma
images = []  # Lista para almacenar las rutas de las imágenes

output_folder = "frames"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

femm.openfemm()


femm.opendocument(r'iteracion2.FEM')  

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
