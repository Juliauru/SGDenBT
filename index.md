# Trabajo de Fin de Grado: Análisis de flujo de cargas en redes de distribución urbanas con integración de sistemas fotovoltaicos
En esta página se recogen los resultados obtenidos en el TFG "Análisis de flujo de cargas en redes de distribución urbanas con integración de sistemas fotovoltaicos" realizado por Julia Uruel Sanz, alumna del Doble grado de Ingeniería Eléctrica e Ingeniería Electrónica Industrial y Automática en la UPM. Este proyecto se ha realizado en colaboración con el Instituto de Energía Solar (IES) y ha sido tutorizado por Óscar Perpiñan Lamigueiro.

## Resumen
En los últimos años las energías renovables están cobrando importancia social y económicamente y, entre ellas, destaca la energía fotovoltaica. El autoconsumo eléctrico residencial es uno de los campos con mayor potencial y la implantación de sistemas fotovoltaicos conectados a red está en auge. 
La instalación en entornos residenciales de sistemas de generación distribuida puede variar el comportamiento de las redes de distribución de baja tensión,  ya que estas redes están diseñadas para llevar un flujo unidireccional, y la inclusión de estos generadores supone fluctuaciones en los flujos de carga. 
Por ello, se ha realizado el estudio de las magnitudes fundamentales en tres redes de baja tensión situadas en Madrid para diferentes grados de penetración fotovoltaica. Se han realizado las simulaciones necesarias mediante el software OpenDSS y se ha llevado a cabo el análisis de los resultados. Tanto el código implementado como los resultados obtenidos se han recogido en este sitio web de libre acceso. 
La investigación concluye que, entre otros aspectos, los sistemas fotovoltaicos conectados a red producen variaciones de tensión en un punto de la red, las cuales dependen de la penetración fotovoltaica, de la distancia entre el punto de estudio y el centro de transformación y de la relación entre consumo y generación en la red. Además, existen grandes fluctuaciones estacionales pues dependen de parámetros como la irradiancia o el consumo que a su vez varían estacionalmente. Otros factores que influyen en la evolución general del sistema son la tipología de edificio y la topología de red.

## Código
El código se puede consultar en el repositorio [SGDenBT](https://github.com/Juliauru/SGDenBT). Se puede consultar tanto el código en MATLAB utilizado para crear el código en OpenDSS desde planos en formato '.dxf' y la realización de simulaciones, como el código en Python para realizar gráficas dinámicas con la librería Plotly. 

## Resultados
En este apartado se recogen todas las gráficas dinámicas generadas para la realización del estudio. Para interactuar con ellas pulse sobre las leyenda para mostrar/ocultar un conjunto de datos.

* ### [Calle Bélgica-Calle Sofía](https://juliauru.github.io/D.Belgica)

* ### [Calle Benimamet](https://juliauru.github.io/D.Benimamet)

* ### [Calle Godella](https://juliauru.github.io/D.Godella)


