import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
import time
import threading

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)

# Pines GPIO que se utilizarán para PWM
pwm_pins = [21, 20, 16]  # Pines GPIO 21, 20, 16 (pines físicos 40, 38, 36)

# Configurar los pines como salida y PWM
for pin in pwm_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Variables globales para frecuencia y ciclo de trabajo
freq = 1
duty1 = 50
duty3 = 50

# Bandera para controlar el hilo de PWM
running = False

# Función de PWM en un hilo separado
def pwm_thread():
    global running
    period = 1.0 / freq

    while running:
        on_time_21 = (duty1 / 100.0) * period
        off_time_21 = period - on_time_21

        # Pin 21 y Pin 20 alternados sin superposición
        GPIO.output(pwm_pins[0], GPIO.HIGH)
        GPIO.output(pwm_pins[1], GPIO.LOW)  # Asegura que el pin 20 está apagado
        time.sleep(on_time_21)
        GPIO.output(pwm_pins[0], GPIO.LOW)

        GPIO.output(pwm_pins[1], GPIO.HIGH)
        time.sleep(off_time_21)
        GPIO.output(pwm_pins[1], GPIO.LOW)

        # Pin 16
        on_time_16 = (duty3 / 100.0) * period
        off_time_16 = period - on_time_16

        GPIO.output(pwm_pins[2], GPIO.HIGH)
        time.sleep(on_time_16)
        GPIO.output(pwm_pins[2], GPIO.LOW)
        time.sleep(off_time_16)

# Función para actualizar PWM
def update_pwm():
    global freq, duty1, duty3, running

    try:
        freq = float(freq_entry.get())
        duty1 = float(duty_entry1.get())
        duty3 = float(duty_entry3.get())

        # Asegurar que el ciclo de trabajo esté entre 0 y 100%
        if duty1 > 100:
            duty1 = 100
        if duty3 > 100:
            duty3 = 100

        # Detener el hilo anterior si está corriendo
        running = False
        time.sleep(0.1)  # Esperar un momento para asegurar que el hilo se detenga

        # Iniciar un nuevo hilo de PWM
        running = True
        threading.Thread(target=pwm_thread).start()
    except ValueError:
        pass  # Maneja errores en caso de entrada no válida

# Función para apagar PWM y limpiar GPIO
def shutdown():
    global running
    running = False
    time.sleep(0.1)  # Esperar un momento para asegurar que el hilo se detenga
    for pin in pwm_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()
    root.destroy()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Control de PWM")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Variables de Tkinter
freq_entry = tk.StringVar()
duty_entry1 = tk.StringVar()
duty_entry3 = tk.StringVar()

# Elementos de la interfaz
ttk.Label(mainframe, text="Frecuencia (Hz)").grid(column=1, row=1, sticky=tk.W)
ttk.Entry(mainframe, width=7, textvariable=freq_entry).grid(column=2, row=1, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="Ciclo de trabajo pin 21 (%)").grid(column=1, row=2, sticky=tk.W)
ttk.Entry(mainframe, width=7, textvariable=duty_entry1).grid(column=2, row=2, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="Ciclo de trabajo pin 16 (%)").grid(column=1, row=3, sticky=tk.W)
ttk.Entry(mainframe, width=7, textvariable=duty_entry3).grid(column=2, row=3, sticky=(tk.W, tk.E))

ttk.Button(mainframe, text="Actualizar", command=update_pwm).grid(column=2, row=4, sticky=tk.W)
ttk.Button(mainframe, text="Apagar", command=shutdown).grid(column=2, row=5, sticky=tk.W)

# Agregar padding a todos los elementos del frame
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

# Correr la aplicación de Tkinter
root.mainloop()
#aqui le hacemos un cambio
# Limpiar los pines GPIO al cerrar
for pin in pwm_pins:
    GPIO.output(pin, GPIO.LOW)
GPIO.cleanup()

