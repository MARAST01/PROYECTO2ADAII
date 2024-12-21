# Proyecto ADA II
#  Desarrolladores: 
# Juan Jose Hernandez 2259500
# Juan Jose Gallego 2259433
# Marlon Astudillo 2259462
# Tina Torres 2259729
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def seleccionar_archivo():
    """Permite al usuario seleccionar un archivo de entrada."""
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de entrada", filetypes=[("Archivos MiniZinc", "*.dzn"), ("Todos los archivos", "*.*")])
    if archivo:
        archivo_entrada.set(archivo)

def ejecutar_modelo():
    """Ejecuta el modelo de MiniZinc usando el archivo seleccionado."""
    archivo = archivo_entrada.get()
    if not archivo:
        messagebox.showerror("Error", "Debe seleccionar un archivo de entrada.")
        return

    solver = solver_seleccionado.get()
    if not solver:
        messagebox.showerror("Error", "Debe seleccionar un solver.")
        return

    try:
        # Comando para ejecutar MiniZinc con el solver seleccionado
        resultado = subprocess.run([
            "minizinc", "--solver", solver, "modelo.mzn", archivo
        ], capture_output=True, text=True, check=True)

        # Mostrar resultado
        text_salida.delete(1.0, tk.END)
        text_salida.insert(tk.END, resultado.stdout)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al ejecutar el modelo:\n{e.stderr}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz MiniZinc")
ventana.geometry("600x500")

# Variable para almacenar la ruta del archivo de entrada
archivo_entrada = tk.StringVar()
solver_seleccionado = tk.StringVar()

# Etiqueta y botón para seleccionar archivo
frame_entrada = tk.Frame(ventana)
frame_entrada.pack(pady=10)

etiqueta_entrada = tk.Label(frame_entrada, text="Archivo de entrada:")
etiqueta_entrada.pack(side=tk.LEFT, padx=5)

entrada_texto = tk.Entry(frame_entrada, textvariable=archivo_entrada, width=50, state="readonly")
entrada_texto.pack(side=tk.LEFT, padx=5)

boton_entrada = tk.Button(frame_entrada, text="Seleccionar", command=seleccionar_archivo)
boton_entrada.pack(side=tk.LEFT, padx=5)

# Opciones de solver
frame_solver = tk.Frame(ventana)
frame_solver.pack(pady=10)

etiqueta_solver = tk.Label(frame_solver, text="Seleccione un solver:")
etiqueta_solver.pack(side=tk.LEFT, padx=5)

opciones_solver = ["gecode", "chuffed", "cbc"]
menu_solver = tk.OptionMenu(frame_solver, solver_seleccionado, *opciones_solver)
menu_solver.pack(side=tk.LEFT, padx=5)

# Botón para ejecutar el modelo
boton_ejecutar = tk.Button(ventana, text="Ejecutar Modelo", command=ejecutar_modelo)
boton_ejecutar.pack(pady=10)

# Área de texto para mostrar la salida
text_salida = tk.Text(ventana, wrap=tk.WORD, height=20, width=70)
text_salida.pack(padx=10, pady=10)

# Iniciar el bucle principal
ventana.mainloop()
