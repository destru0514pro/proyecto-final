# -*- coding: utf-8 -*-
"""Proyectofin.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gaPqP2gzS66lHataQVdBpe-QBs_cf1s6
"""

import tensorflow as tf
from tensorflow.keras.datasets import fashion_mnist
import numpy as np
from tensorflow.keras.utils import to_categorical
import tensorflow_datasets as tfds

#Descargar set de datos de Fashion MNIST de Zalando
datos, metadatos = tfds.load('fashion_mnist', as_supervised=True, with_info=True)

#Obtenemos en variables separadas los datos de entrenamiento (60k) y pruebas (10k)
datos_entrenamiento, datos_pruebas = datos['train'], datos['test']

#Cargar los datos de fashion_mnist
(X_entrenamiento, Y_entrenamiento), (X_pruebas, Y_pruebas) = fashion_mnist.load_data()

#Colocar los datos en la forma correcta que ya hemos visto (1, 28, 28, 1)
X_entrenamiento = X_entrenamiento.reshape(X_entrenamiento.shape[0], 28, 28, 1)
X_pruebas = X_pruebas.reshape(X_pruebas.shape[0], 28, 28, 1)

#Hacer 'one-hot encoding' de los resultados (e.g. en lugar de tener como resultado una sola neurona, tendre 10 donde solo el resultado correcto sera 1 y el resto 0)
Y_entrenamiento = to_categorical(Y_entrenamiento)
Y_pruebas = to_categorical(Y_pruebas)

#Convertir a flotante y normalizar para que aprenda mejor la red
X_entrenamiento = X_entrenamiento.astype('float32') / 255
X_pruebas = X_pruebas.astype('float32') / 255

#Etiquetas de las 10 categorias posibles
nombres_clases = metadatos.features['label'].names

nombres_clases

#Aumento de datos
#Variables para controlar las transformaciones que se haran en el aumento de datos
#utilizando ImageDataGenerator de keras

from tensorflow.keras.preprocessing.image import ImageDataGenerator

rango_rotacion = 30
mov_ancho = 0.25
mov_alto = 0.25
#rango_inclinacion=15 #No uso este de momento pero si quieres puedes probar usandolo!
rango_acercamiento=[0.5,1.5]

datagen = ImageDataGenerator(
    rotation_range = rango_rotacion,
    width_shift_range = mov_ancho,
    height_shift_range = mov_alto,
    zoom_range=rango_acercamiento,
    #shear_range=rango_inclinacion #No uso este de momento pero si quieres puedes probar usandolo!
)

datagen.fit(X_entrenamiento)

#Modelo
modelo = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(100, activation='relu'),
    tf.keras.layers.Dense(10, activation="softmax")
])

#Compilación
modelo.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
#Los datos para entrenar saldran del datagen, de manera que sean generados con las transformaciones que indicamos
data_gen_entrenamiento = datagen.flow(X_entrenamiento, Y_entrenamiento, batch_size=32)

# Commented out IPython magic to ensure Python compatibility.
from tensorflow.keras.callbacks import TensorBoard
#Cargar la extension de tensorboard de colab
# %load_ext tensorboard

#Ejecutar tensorboard e indicarle que lea la carpeta "logs"
# %tensorboard --logdir logs

TAMANO_LOTE = 32

#Entrenar la red. Toma un buen rato! Ve por un café ;)
#Oye suscribete al canal!
print("Entrenando modelo...");
tensorboard = TensorBoard(log_dir='logs/')
history = modelo.fit(
    data_gen_entrenamiento,
    epochs=70,
    batch_size=TAMANO_LOTE,
    validation_data=(X_pruebas, Y_pruebas),
    steps_per_epoch=int(np.ceil(60000 / float(TAMANO_LOTE))),
    validation_steps=int(np.ceil(10000 / float(TAMANO_LOTE))),
    callbacks=[tensorboard]
)

print("Modelo entrenado!");

#Exportar el modelo al explorador
modelo.save('ropa_conv.h5')

#Convertirlo a tensorflow.js
!pip install tensorflowjs

!mkdir carpeta_salida

!tensorflowjs_converter --input_format keras ropa_conv.h5 carpeta_salida

import random

valores_prendas = {} # Agrega más clases según sea necesario


for i in nombres_clases:
  valores_prendas[i]=random.randint(100,3000)
print(valores_prendas)

# Función para predecir el valor de una prenda
import numpy as np
def predecir_valor(imagen):
    imagen = np.array([imagen])
    prediccion = modelo.predict(imagen)
    return prediccion[0]

# Calcular la suma total del valor de las prendas en una lista de imágenes
def calcular_suma_total(imagenes):
    suma_total = 0
    for imagen in imagenes:
        valor_predicho = predecir_valor(imagen)
        clase_predicha = np.argmax(valor_predicho)
        suma_total += valores_prendas[nombres_clases[clase_predicha]]
    return suma_total

# Verificar que las clases en nombres_clases estén en valores_prendas
for clase in nombres_clases:
    if clase not in valores_prendas:
        # Asignar un valor por defecto o manejar la situación según tus necesidades
        valores_prendas[clase] = 0  # Puedes cambiar 0 por el valor que desees asignar

# Calcular la suma total del valor de las prendas


# Imprimir el resultado
print("Suma total del valor de las prendas:", )

# Supongamos que 'imagenes_a_evaluar' es un conjunto de imágenes que tienes
# Puedes reemplazar esta parte con el conjunto real de imágenes que estás utilizando

# Por ejemplo, si las imágenes provienen de tu conjunto de datos de prueba:
imagenes_a_evaluar, etiquetas_a_evaluar = next(iter(datos_pruebas))
imagenes_a_evaluar = imagenes_a_evaluar.numpy()



# Imprimir el resultado
print("Suma total del valor de las prendas:", )

import cv2
from PIL import Image
def capturar_imagen_camara():
    cap = cv2.VideoCapture(0)  # El argumento 0 indica la cámara predeterminada

    while True:
        ret, frame = cap.read()
        cv2.imshow("Camara", frame)

        # Esperar hasta que se presione la tecla 's' para capturar la imagen
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return frame

def preprocesar_imagen_camara(imagen):
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    imagen = cv2.resize(imagen, (28, 28))
    imagen = imagen / 255.0  # Normalización
    imagen = np.expand_dims(imagen, axis=-1)  # Agregar una dimensión para que coincida con el formato de entrada del modelo
    return imagen

from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode
import numpy as np
import cv2
from PIL import Image
import io

# Función para capturar imágenes de la cámara en Google Colab
def capturar_imagen_colab():
    js = Javascript('''
        async function capturar_imagen_colab() {
            const div = document.createElement('div');
            const video = document.createElement('video');
            video.style.display = 'block';
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            document.body.appendChild(div);
            div.appendChild(video);
            video.srcObject = stream;
            await video.play();

            // Esperar hasta que se haga clic en la imagen
            return new Promise((resolve) => {
                video.onclick = () => {
                    const canvas = document.createElement('canvas');
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    canvas.getContext('2d').drawImage(video, 0, 0);
                    stream.getVideoTracks()[0].stop();
                    div.remove();
                    resolve(canvas.toDataURL('image/jpeg'));
                };
            });
        }
    ''')
    display(js)
    data_url = eval_js('capturar_imagen_colab()')
    binary = b64decode(data_url.split(',')[1])
    image = Image.open(io.BytesIO(binary))
    return np.array(image)

# Definir la función para preprocesar la imagen de la cámara
def preprocesar_imagen_camara(imagen):
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    imagen = cv2.resize(imagen, (28, 28))
    imagen = imagen / 255.0  # Normalización
    imagen = np.expand_dims(imagen, axis=-1)  # Agregar una dimensión para coincidir con el formato de entrada del modelo
    return imagen

# Capturar imagen de la cámara en Colab y realizar predicciones
imagen_camara = capturar_imagen_colab()
imagen_preprocesada = preprocesar_imagen_camara(imagen_camara)

# Utilizar el modelo para predecir la clase
valor_predicho = predecir_valor(imagen_preprocesada)
clase_predicha = np.argmax(valor_predicho)

# Obtener el valor asignado a la clase predicha
valor_asignado = valores_prendas.get(nombres_clases[clase_predicha], 0)

# Mostrar la predicción y el valor asignado
print("Predicción de la prenda:", nombres_clases[clase_predicha])
print("Valor asignado a la prenda:", valor_asignado)

historial_escaneo = []

# Capturar imagen de la cámara en Colab y realizar predicciones
imagen_camara = capturar_imagen_colab()

# Imprimir la forma de la imagen capturada
print("Forma de la imagen capturada:", imagen_camara.shape)

imagen_preprocesada = preprocesar_imagen_camara(imagen_camara)

# Imprimir la forma de la imagen preprocesada
print("Forma de la imagen preprocesada:", imagen_preprocesada.shape)

# Utilizar el modelo para predecir la clase
valor_predicho = predecir_valor(imagen_preprocesada)
clase_predicha = np.argmax(valor_predicho)

# Obtener el valor asignado a la clase predicha
valor_asignado = valores_prendas.get(nombres_clases[clase_predicha], 0)

# Mostrar la predicción y el valor asignado
print("Predicción de la prenda:", nombres_clases[clase_predicha])
print("Valor asignado a la prenda:", valor_asignado)

# Agregar a historial de escaneo
historial_escaneo.append({
    "imagen_camara": imagen_camara,
    "prediccion": nombres_clases[clase_predicha],
    "valor_asignado": valor_asignado
})

# Mostrar la imagen capturada junto con la predicción y el valor asignado
import matplotlib.pyplot as plt

plt.imshow(imagen_camara)
plt.title(f"Predicción: {nombres_clases[clase_predicha]}\nValor asignado: {valor_asignado}")
plt.axis('off')
plt.show()

# Mostrar el historial de escaneo
print("\nHistorial de Escaneo:")
for escaneo in historial_escaneo:
    print("Predicción:", escaneo["prediccion"])
    print("Valor asignado:", valores_prendas[escaneo["prediccion"]],'$')
    print("-" * 20)