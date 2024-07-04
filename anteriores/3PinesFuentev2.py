import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
import time

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)

# Pines GPIO que se utilizarán para PWM
pwm_pins = [18, 23, 24]  # Cambia estos pines según tu configuración

# Configurar los pines como salida y PWM
pwms = []
for pin in pwm_pins:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 1000)  # Frecuencia inicial de 1 kHz
    pwm.start(0)  # Duty cycle inicial del 0%
    pwms.append(pwm)

# Función para actualizar PWM con dead time
def update_pwm():
    try:
        freq = float(freq_entry.get())
        duty1 = float(duty_entry1.get())
        duty2 = float(duty_entry2.get())
        duty3 = float(duty_entry3.get())

        for pwm in pwms:
            pwm.ChangeFrequency(freq)
        
        # Asegurar que los pines 18 y 23 nunca están activos al mismo tiempo
        if duty1 > 0:
            pwms[0].ChangeDutyCycle(duty1)
            pwms[1].ChangeDutyCycle(0)
            time.sleep(0.001)  # Tiempo muerto de 1 ms
            pwms[1].ChangeDutyCycle(duty2)
        else:
            pwms[1].ChangeDutyCycle(duty2)
            pwms[0].ChangeDutyCycle(0)
            time.sleep(0.001)  # Tiempo muerto de 1 ms
            pwms[0].ChangeDutyCycle(duty1)

        pwms[2].ChangeDutyCycle(duty3)
    except ValueError:
        pass  # Maneja errores en caso de entrada no válida

# Función para apagar PWM y limpiar GPIO
def shutdown():
    for pwm in pwms:
        pwm.stop()
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
duty_entry2 = tk.StringVar()
duty_entry3 = tk.StringVar()

# Elementos de la interfaz
ttk.Label(mainframe, text="Frecuencia (Hz)").grid(column=1, row=1, sticky=tk.W)
ttk.Entry(mainframe, width=7, textvariable=freq_entry).grid(column=2, row=1, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="Ciclo de trabajo pin 18 (%)").grid(column=1, row=2, sticky=tk.W)
ttk.Entry(mainframe, width=7, textvariable=duty_entry1).grid(column=2, row=2, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="Ciclo de trabajo pin 23 (%)").grid(column=1, row=3, sticky=tk.W)
ttk.Entry(mainframe, width=7, textvariable=duty_entry2).grid(column=2, row=3, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="Ciclo de trabajo pin 24 (%)").grid(column=1, row=4, sticky=tk.W)
ttk.Entry(mainframe, width=7, textvariable=duty_entry3).grid(column=2, row=4, sticky=(tk.W, tk.E))

ttk.Button(mainframe, text="Actualizar", command=update_pwm).grid(column=2, row=5, sticky=tk.W)
ttk.Button(mainframe, text="Apagar", command=shutdown).grid(column=2, row=6, sticky=tk.W)

# Agregar padding a todos los elementos del frame
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

# Correr la aplicación de Tkinter
root.mainloop()

# Limpiar los pines GPIO al cerrar
for pwm in pwms:
    pwm.stop()
GPIO.cleanup()
