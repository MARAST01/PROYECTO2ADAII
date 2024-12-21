
                % ------------------------------------------
        % PARAMETRIZACI�N
        % ------------------------------------------

        % Cantidad de posiciones definidas de antemano
        int: total_posiciones_fijas;

        % Coordenadas de las posiciones definidas previamente (matriz de tama�o [total_posiciones_fijas, 2])
        array[1..total_posiciones_fijas, 1..2] of int: posiciones_fijas;

        % Dimensiones de la cuadr�cula
        int: tam_cuadricula;

        % Matriz que representa la distribuci�n poblacional
        array[1..tam_cuadricula, 1..tam_cuadricula] of int: matriz_poblacional;

        % Matriz que representa el entorno econ�mico
        array[1..tam_cuadricula, 1..tam_cuadricula] of int: matriz_economica;

        % Cantidad de ubicaciones por asignar
        int: cantidad_ubicaciones;


        % ------------------------------------------
        % VARIABLES
        % ------------------------------------------

        % Matriz que indica la presencia de una ubicaci�n (1) o su ausencia (0) en la cuadr�cula
        array[1..tam_cuadricula, 1..tam_cuadricula] of var 0..1: mapa_ubicaciones;

        % Inicializaci�n de las posiciones fijas
        array[1..tam_cuadricula, 1..tam_cuadricula] of int: ubicaciones_fijas = 
          array2d(1..tam_cuadricula, 1..tam_cuadricula, 
            [if exists(p in 1..total_posiciones_fijas) 
                (i = posiciones_fijas[p, 2] /\ j = posiciones_fijas[p, 1]) 
             then 1 else 0 endif | i, j in 1..tam_cuadricula]);


        % ------------------------------------------
        % RESTRICCIONES
        % ------------------------------------------

        % Las posiciones fijas deben permanecer activadas
        constraint forall(i, j in 1..tam_cuadricula)(
          ubicaciones_fijas[i, j] = 1 -> mapa_ubicaciones[i, j] = 1
        );

        % La cantidad total de ubicaciones debe ser la suma de las fijas y las nuevas asignadas
        constraint sum(i in 1..tam_cuadricula, j in 1..tam_cuadricula)(mapa_ubicaciones[i, j]) = cantidad_ubicaciones + total_posiciones_fijas;

        % Evitar que haya ubicaciones en celdas adyacentes
        constraint forall(i, j in 1..tam_cuadricula)(
          mapa_ubicaciones[i, j] = 1 ->
          forall(k in max(1, i-1)..min(tam_cuadricula, i+1), 
                 l in max(1, j-1)..min(tam_cuadricula, j+1))(
            (k != i \/ l != j) -> mapa_ubicaciones[k, l] = 0
          )
        );

        % Definir una funci�n que calcula la suma de los valores vecinos en una matriz dada
        function int: suma_vecindad(array[1..tam_cuadricula, 1..tam_cuadricula] of int: matriz, int: i, int: j) =
          sum(k in max(1, i-1)..min(tam_cuadricula, i+1), 
              l in max(1, j-1)..min(tam_cuadricula, j+1))(
                matriz[k, l]
          );

        % Restricciones para garantizar un m�nimo de poblaci�n y entorno econ�mico
        constraint forall(i, j in 1..tam_cuadricula)(
          mapa_ubicaciones[i, j] = 1 ->
          (
                suma_vecindad(matriz_poblacional, i, j) >= 25 /\
                suma_vecindad(matriz_economica, i, j) >= 20
                )
              );


        % ------------------------------------------
        % FUNCI�N OBJETIVO
        % ------------------------------------------

        % Calcular la ganancia obtenida por todas las ubicaciones
        var int: beneficio_total = sum(i, j in 1..tam_cuadricula where mapa_ubicaciones[i, j] = 1)(
          suma_vecindad(matriz_poblacional, i, j) +
          suma_vecindad(matriz_economica, i, j)
        );

        % Beneficio exclusivo para las posiciones predefinidas
        var int: beneficio_posiciones_fijas = sum(p in 1..total_posiciones_fijas)(
          suma_vecindad(matriz_poblacional, posiciones_fijas[p, 2], posiciones_fijas[p, 1]) +
          suma_vecindad(matriz_economica, posiciones_fijas[p, 2], posiciones_fijas[p, 1])
        );

        % Maximizar el beneficio total
        solve maximize beneficio_total;


        % ------------------------------------------
        % SALIDA
        % ------------------------------------------

        % Mostrar la matriz de ubicaciones y el beneficio calculado
        output [
          "Mapa de ubicaciones:", show([mapa_ubicaciones[i, j] | i in 1..tam_cuadricula, j in 1..tam_cuadricula]), "Beneficio total: ", show(beneficio_total),                "  Beneficio de las posiciones fijas: ", show(beneficio_posiciones_fijas), "   "
        ];
        