import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO

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

# Función para actualizar PWM
def update_pwm():
    try:
        freq = float(freq_entry.get())
        duty = float(duty_entry.get())
        for pwm in pwms:
            pwm.ChangeFrequency(freq)
            pwm.ChangeDutyCycle(duty)
    except ValueError:
        pass  # Maneja errores en caso de entrada no válida

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Control de PWM")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Variables de Tkinter
freq_entry = tk.StringVar()
duty_entry = tk.StringVar()

# Elementos de la interfaz
ttk.Label(mainframe, text="Frecuencia (Hz)").grid(column=1, row=1, sticky=tk.W)
ttk.Entry(mainframe, width=7, textvariable=freq_entry).grid(column=2, row=1, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="Ciclo de trabajo (%)").grid(column=1, row=2, sticky=tk.W)
ttk.Entry(mainframe, width=7, textvariable=duty_entry).grid(column=2, row=2, sticky=(tk.W, tk.E))

ttk.Button(mainframe, text="Actualizar", command=update_pwm).grid(column=2, row=3, sticky=tk.W)

# Agregar padding a todos los elementos del frame
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

# Correr la aplicación de Tkinter
root.mainloop()

# Limpiar los pines GPIO al cerrar
for pwm in pwms:
    pwm.stop()
GPIO.cleanup()
