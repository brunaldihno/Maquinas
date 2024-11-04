import matplotlib.pyplot as plt
import numpy as np

file = "Flujos.txt"
angulos = 360
frec_mec = 10
dt = 1/(frec_mec*angulos)
N = 200

with open(file, "r") as f:
    data = f.readlines()

data_2 = []

for angle in data:
    angle = angle[1:-1]
    angle = angle.split(",")
    lista = []
    x = True
    for elem in angle:
        elem = elem.strip("]")
        if x:
            elem = elem[1:-1]
        else:
            elem = elem[2:-1]
        x = False
        lista.append(float(elem))
    data_2.append(lista)

data_2 = np.transpose(data_2)

data_3 = []

for i in range(len(data_2)):
    lista = []
    for j in range(len(data_2[0])):
        lista.append(-N*(data_2[i][j]- data_2[i][j-1])/dt)
    data_3.append(lista)

num_plots = len(data_3)

# Create a 3x4 grid of subplots (adjust as necessary)
fig, axes = plt.subplots(3, 4, figsize=(15, 10))

axes = axes.flatten()

# Plot each data row in data_3 on its corresponding subplot
for i in range(num_plots):
    axes[i].plot(data_2[i])
    axes[i].set_title(f'Bobinado {i+1}')
    axes[i].set_xlabel("Ángulo")
    axes[i].set_ylabel("Flujo [Wb]")

plt.tight_layout()
plt.show()

fig, axes = plt.subplots(3, 4, figsize=(15, 10))

axes = axes.flatten()

# Plot each data row in data_3 on its corresponding subplot
for i in range(num_plots):
    axes[i].plot(data_3[i])
    axes[i].set_title(f'Bobinado {i+1}')
    axes[i].set_xlabel("Ángulo")
    axes[i].set_ylabel("Voltaje [V]")

plt.tight_layout()
plt.show()

Fase_A = [0, -1, -6, 7] 
Fase_B = [-2, 3, 8, -9]
Fase_C = [4, -5, -10, 11]

def add_rows(data, indices):
    d = np.zeros_like(data_3[0])
    for indice in indices:
        if indice >= 0:
            d += data[indice]  # Add row if index is positive
        else:
            d -= data[abs(indice)]  # Subtract row if index is negative
    return d

Data_A = add_rows(data_3, Fase_A)
Data_B = add_rows(data_3, Fase_B)
Data_C = add_rows(data_3, Fase_C)

fig, axes = plt.subplots(1, 3, figsize=(15, 10))
axes = axes.flatten()

# Plot each data row in data_3 on its corresponding subplot
fases = (Data_A, Data_B, Data_C)
titulos = ["A", "B", "C"]
for i in range(3):
    axes[i].plot(fases[i])
    axes[i].set_title(f'Fase {titulos[i]}')
    axes[i].set_xlabel("Ángulo")
    axes[i].set_ylabel("Voltaje [V]")

plt.tight_layout()
plt.show()

fft_A = np.fft.fft(Data_A)
fft_B = np.fft.fft(Data_B)
fft_C = np.fft.fft(Data_C)

fig, axes = plt.subplots(1, 3, figsize=(15, 10))
axes = axes.flatten()

ffts = (fft_A, fft_B, fft_C)
for i in range(3):
    axes[i].plot(np.abs(ffts[i][:angulos//2]))
    axes[i].set_title(f'Fase {titulos[i]}')
    axes[i].set_xlabel("Frecuencia [Hz]")
    axes[i].set_ylabel("Magnitud")

plt.tight_layout()
plt.show()

frecuancias = np.fft.fftfreq(angulos, d=dt)
main_frequency_idx = np.argmax(np.abs(fft_A[:angulos//2]))
main_frequency = frecuancias[main_frequency_idx]
print(f"Main frequency: {main_frequency} Hz")

# Calculate harmonics (integer multiples of the main frequency)
harmonics = [(i+1) * main_frequency for i in range(1, 5)]  # First 4 harmonics
print("Harmonics:", harmonics)