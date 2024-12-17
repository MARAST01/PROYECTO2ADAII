import tkinter as tk
from tkinter import filedialog, messagebox
from minizinc import Instance, Model, Solver
import os

# Función para cargar archivo de entrada
def cargar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de entrada",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        entrada_label.config(text=f"Archivo seleccionado: {os.path.basename(archivo)}")
        global archivo_entrada
        archivo_entrada = archivo

# Modelo en MiniZinc embebido como cadena
modelo_mzn = """
include "globals.mzn";

int: n;  % Tamaño de la matriz
int: num_ubicaciones_existentes;  % Número de ubicaciones existentes
set of int: R = 1..n;  % Rango de las filas y columnas
set of int: E = 1..num_ubicaciones_existentes;  % Rango de ubicaciones existentes

array[E, 2] of int: ubicaciones_existentes;  % Coordenadas de las ubicaciones existentes
array[R, R] of int: matriz_poblacion;  % Matriz del segmento de población
array[R, R] of int: matriz_entorno;  % Matriz del entorno empresarial
int: nuevas_ubicaciones;  % Número de ubicaciones a agregar

array[1..nuevas_ubicaciones, 2] of var R: ubicaciones_nuevas;  % Coordenadas nuevas

% Restricciones
constraint forall(i in 1..nuevas_ubicaciones)(
    forall(j in E)(
        abs(ubicaciones_nuevas[i, 1] - ubicaciones_existentes[j, 1]) > 1 \/
        abs(ubicaciones_nuevas[i, 2] - ubicaciones_existentes[j, 2]) > 1
    )
);

constraint forall(i in 1..nuevas_ubicaciones)(
    sum([matriz_poblacion[x, y] | x in ubicaciones_nuevas[i, 1]-1..ubicaciones_nuevas[i, 1]+1, 
                                      y in ubicaciones_nuevas[i, 2]-1..ubicaciones_nuevas[i, 2]+1 where x in R /\ y in R]) >= 25 /\
    sum([matriz_entorno[x, y] | x in ubicaciones_nuevas[i, 1]-1..ubicaciones_nuevas[i, 1]+1, 
                                   y in ubicaciones_nuevas[i, 2]-1..ubicaciones_nuevas[i, 2]+1 where x in R /\ y in R]) >= 20
);

% Función objetivo: Maximizar la suma de los valores de población y entorno
var int: ganancia_total = 
    sum(i in 1..nuevas_ubicaciones)(
        sum([matriz_poblacion[x, y] | x in ubicaciones_nuevas[i, 1]-1..ubicaciones_nuevas[i, 1]+1, 
                                          y in ubicaciones_nuevas[i, 2]-1..ubicaciones_nuevas[i, 2]+1 where x in R /\ y in R]) +
        sum([matriz_entorno[x, y] | x in ubicaciones_nuevas[i, 1]-1..ubicaciones_nuevas[i, 1]+1, 
                                     y in ubicaciones_nuevas[i, 2]-1..ubicaciones_nuevas[i, 2]+1 where x in R /\ y in R])
    );

solve maximize ganancia_total;
"""

# Función para resolver el modelo
def resolver_modelo():
    try:
        if not archivo_entrada:
            messagebox.showerror("Error", "Debe seleccionar un archivo de entrada")
            return

        # Cargar modelo desde cadena
        model = Model()
        model.add_string(modelo_mzn)
        solver = Solver.lookup("gecode")
        instance = Instance(solver, model)

        # Leer datos del archivo de entrada
        with open(archivo_entrada, "r") as file:
            lines = [line.strip() for line in file if line.strip()]

        # Procesar datos de entrada
        num_ubicaciones = int(lines[0])  # Número de ubicaciones existentes
        ubicaciones_existentes = [
            tuple(map(int, lines[i + 1].split())) for i in range(num_ubicaciones)
        ]
        
        matriz_tamano = int(lines[num_ubicaciones + 1])  # Tamaño de las matrices
        matriz_poblacion = [
            list(map(int, lines[num_ubicaciones + 2 + i].split()))
            for i in range(matriz_tamano)
        ]
        matriz_entorno = [
            list(map(int, lines[num_ubicaciones + 2 + matriz_tamano + i].split()))
            for i in range(matriz_tamano)
        ]
        nuevas_ubicaciones = int(lines[-1])  # Número de nuevas ubicaciones

        # Asignar datos a la instancia
        instance["n"] = matriz_tamano
        instance["num_ubicaciones_existentes"] = num_ubicaciones
        instance["ubicaciones_existentes"] = ubicaciones_existentes
        instance["matriz_poblacion"] = matriz_poblacion
        instance["matriz_entorno"] = matriz_entorno
        instance["nuevas_ubicaciones"] = nuevas_ubicaciones

        # Resolver el modelo
        result = instance.solve()

        # Mostrar resultados
        resultados_texto = (
            f"Ganancia total: {result['ganancia_total']}\n"
            f"Nuevas ubicaciones: {result['ubicaciones_nuevas']}"
        )
        resultados_label.config(text=resultados_texto)

    except Exception as e:
        messagebox.showerror("Error", f"Error al resolver el modelo: {e}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Optimizador de Programas de Ingeniería")

archivo_entrada = None

# Elementos de la interfaz
titulo = tk.Label(root, text="Optimizador de Localización de Programas", font=("Arial", 16))
titulo.pack(pady=10)

entrada_button = tk.Button(root, text="Cargar archivo de entrada", command=cargar_archivo)
entrada_button.pack(pady=5)

entrada_label = tk.Label(root, text="No se ha seleccionado un archivo")
entrada_label.pack(pady=5)

resolver_button = tk.Button(root, text="Resolver", command=resolver_modelo)
resolver_button.pack(pady=5)

resultados_label = tk.Label(root, text="Resultados aparecerán aquí", justify="left")
resultados_label.pack(pady=10)

# Iniciar el bucle principal
root.mainloop()
