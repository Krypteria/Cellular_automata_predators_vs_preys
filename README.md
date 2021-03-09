# Cellular_automata_predators_vs_preys

![gif](https://user-images.githubusercontent.com/55555187/110488475-caec7d00-80ee-11eb-9d94-7bd2e7fc2e14.gif)

## Como descargarlo y ejecutarlo
### Opción 1 (recomendada)
1. Descargar el ejecutable <b>*Prey_vs_predator.exe*</b> de la última release.
2. Lanzar el ejecutable.
(Debido al caracter de Python es probable que windows defender lo bloquee, dar a ejecutar de todas formas)
### Opción 2
1. Descargar el código fuente en zip de la última release.
2. Descomprimir el zip 
3. Ir a la carpeta donde esté el código fuente
4. Ejecutar desde CMD o terminal <b>*./main.py*</b>

--- 

## ¿Que es un autómata celular?

<img align="left" width="300" height="300" src="https://user-images.githubusercontent.com/55555187/110489933-181d1e80-80f0-11eb-88ef-ee578cf45288.png">

Si nos remitimos a la definición formal, un autómata celular es un modelo matemático para un sistema dinámico compuesto por un conjunto de celdas o células que adquieren distintos estados o valores. Estos estados son alterados de un instante a otro en unidades de tiempo discreto, es decir, que se puede cuantificar con valores enteros a intervalos regulares. 

De esta manera este conjunto de células logra una evolución según una determinada expresión matemática o conjunto de reglas que son sensibles a los estados de las células vecinas.

El nombre de autómata celular se debe a su gran parecido con el crecimiento celular.  

<br>
  
---  

## Tipos de autómatas 

<img align="left" width="403" height="196" src="https://user-images.githubusercontent.com/55555187/110493884-5405b300-80f3-11eb-97a2-742477eb24f2.png">
La simulación cuenta con 6 autómatas diferentes, estos se agrupan en 2 grandes tipos (depredadores o presas) y dentro de cada tipo en 3 etapas diferentes (joven, adulto o viejo). 

<br><br><br><br>

--- 

## Reglas
El comportamiento de cada autómata vienen definido por una serie de reglas que toman en consideración el tipo del autómata, la etapa en la que está y el estado de los autómatas vecinos.

### Depredadores

<details>
  <summary><b>Crecimiento</b></summary>
  
- Si el tiempo de vida de un depredador jóven es igual a un cierto límite *"YOUNG_PREDATOR_LIMIT"*, entonces, el depredador pasa a ser adulto.
- Si el tiempo de vida de un depredador adulto es igual a un cierto límite *"ADULT_PREDATOR_LIMIT"*, entonces, el depredador pasa a ser viejo.
- Si el tiempo de vida de un depredador viejo es igual a un cierto límite *"OLD_PREDATOR_LIMIT"*, entonces, el depredador muere.

</details>

<details>
  <summary><b>Reproducción</b></summary>

- Los depredadores jóvenes y viejos no tienen la capacidad de reproducirse.
- Los depredadores adultos se reproducen si su tiempo de reproducción *"timeToReproduction"* es igual a 0, pueden reproducirse de dos formas diferentes siguiendo las siguiente condiciones:

  - Si el número de presas adyacentes es igual o mayor que un cierto parámetro *"PREDATOR_REPRODUCTION_CONDITION"* entonces el depredador ingerirá *"PREDATOR_REPRODUCTION_RATIO"* presas generando el mismo número de depredadores jovenes en dichas posiciones (*"PREDATOR_REPRODUCTION_CONDITION"* >= *"PREDATOR_REPRODUCTION_RATIO"*).
 
  - Si *"PREDATOR_REPRODUCTION_CONDITION"* > número presas adyacentes >= 1, entonces, el depredador ingerirá a una de las presas generando un depredador joven en dicha celda.

</details>

<details>
  <summary><b>Alimentación</b></summary>

- Los depredadores jóvenes y los viejos pueden comer siempre que tengan al menos una presa en una celda adyacente, al ingerir la presa se mueven a dicha celda.
- Los depredadores adultos al ingerir una presa se reproducen generando nuevos depredadores.

</details>

<details>
  <summary><b>Movimiento</b></summary>

- Los depredadores jóvenes se mueven si no han comido y tienen al menos una celda adyacente libre.
- Los depredadores adultos se mueven si no se han reproducido y tienen al menos una celda adyacente libre.
- Los depredadores viejos se mueven con una probabilidad del 50% si no han comido y tienen al menos una celda adyacente libre.

</details>

### Presas


<details>
  <summary><b>Crecimiento</b></summary>

- Si el tiempo de vida de una presa joven es igual a un cierto límite *"YOUNG_PREY_LIMIT"*, entonces, la presa pasa a ser adulta.
- Si el tiempo de vida de una presa adulta es igual a un cierto límite *"ADULT_PREY_LIMIT"*, entonces, la presa pasa a ser vieja.
- Si el tiempo de vida de una presa vieja es igual a un cierto límite *"OLD_PREY_LIMIT"*, entonces, la presa muere.

</details>

<details>
  <summary><b>Reproducción</b></summary>
  
- Las presas jovenes y viejas no tienen la capacidad de reproducirse.
- Las presas adultas se reproducen si su tiempo de reproducción *"timeToReproduction"* es igual a 0 y tienen al menos una celda adyacente libre.

</details>
  
<details>
  <summary><b>Movimiento</b></summary>

- Las presas jóvenes se mueven si tienen al menos una celda adyacente libre.
- Las presas viejas se mueven con una probabilidad del 50% si tienen al menos una celda adyacente libre. 
- Las presas adultas se mueven si no se han reproducido tienen al menos una celda adyacente libre.

</details>

## Funcionalidades extra
La aplicación cuenta con una funcionalidad para pausar y despausar la simulación pulsando cualquier tecla del teclado.

## GIFS 

![Gif2](https://user-images.githubusercontent.com/55555187/110504831-d6937000-80fd-11eb-87d6-0c5affd8e1c1.gif)
![gif3](https://user-images.githubusercontent.com/55555187/110504833-d72c0680-80fd-11eb-8e09-6d3e2662f863.gif)
