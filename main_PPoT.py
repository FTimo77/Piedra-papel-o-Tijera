import tkinter as tk
from tkinter import PhotoImage, messagebox
import random

class Logica:
    OPCIONES = {1: "Piedra", 2: "Papel", 3: "Tijera"}

    def __init__(self):
        self.objeto_usuario = None
        self.objeto_maquina = None

    def eleccion_maquina(self):
        self.objeto_maquina = random.choice(list(self.OPCIONES.keys()))

    def elegir_ganador(self):
        if self.objeto_usuario == self.objeto_maquina:
            return 0  # Empate
        elif (self.objeto_usuario == 1 and self.objeto_maquina == 3) or \
             (self.objeto_usuario == 2 and self.objeto_maquina == 1) or \
             (self.objeto_usuario == 3 and self.objeto_maquina == 2):
            return 1  # Usuario gana
        else:
            return -1  # Máquina gana


class Interfaz:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Piedra, Papel o Tijera")
        self.ventana.geometry("800x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f4fc")

        self.logica = Logica()
        self.puntos_usuario = 0
        self.puntos_maquina = 0

        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Título
        titulo = tk.Label(
            self.ventana, text="¡Piedra, Papel o Tijera!",
            font=("Arial", 24, "bold"), bg="#587ef8", fg="white", pady=10
        )
        titulo.pack(fill="x")

        # Puntuación
        puntuacion_frame = tk.LabelFrame(
            self.ventana, text="Puntuación", font=("Arial", 14),
            bg="#dbe7ff", fg="black", padx=20, pady=10
        )
        puntuacion_frame.pack(pady=20, fill="x")

        self.puntuacion_label = tk.Label(
            puntuacion_frame, text="Tú: 0 | Máquina: 0",
            font=("Arial", 18), bg="#dbe7ff"
        )
        self.puntuacion_label.pack()

        # Contenedor de imágenes centrado
        self.frame_juego = tk.Frame(self.ventana, bg="#f0f4fc")
        self.frame_juego.pack(pady=20, expand=True)

        # Imágenes para elecciones
        self.imagenes = {
            1: PhotoImage(file="piedra.png").subsample(4, 4),
            2: PhotoImage(file="papel.png").subsample(4, 4),
            3: PhotoImage(file="tijera.png").subsample(4, 4)
        }

        # Imagen del usuario
        self.usuario_label = tk.Label(self.frame_juego, text="Tu elección", font=("Arial", 16), bg="#f0f4fc")
        self.usuario_label.grid(row=0, column=0, padx=20)

        self.img_usuario = tk.Label(self.frame_juego, bg="#f0f4fc")
        self.img_usuario.grid(row=1, column=0, padx=20)

        # Imagen de la máquina
        self.maquina_label = tk.Label(self.frame_juego, text="Elección de la máquina", font=("Arial", 16), bg="#f0f4fc")
        self.maquina_label.grid(row=0, column=2, padx=20)

        self.img_maquina = tk.Label(self.frame_juego, bg="#f0f4fc")
        self.img_maquina.grid(row=1, column=2, padx=20)

        # Botones de opciones centrados
        boton_frame = tk.Frame(self.ventana, bg="#f0f4fc")
        boton_frame.pack(pady=10)

        for i, (opcion, imagen) in enumerate(self.imagenes.items(), start=1):
            boton = tk.Button(
                boton_frame, image=imagen, command=lambda eleccion=opcion: self.jugada(eleccion),
                borderwidth=0, bg="#e6edff", activebackground="#dbe7ff"
            )
            boton.grid(row=0, column=i, padx=20, pady=20)

    def jugada(self, eleccion_usuario):
        # Mostrar la elección del usuario
        eleccion_imagen = self.imagenes[eleccion_usuario]
        self.img_usuario.config(image=eleccion_imagen)
        self.img_usuario.image = eleccion_imagen

        # Asignar elección del usuario
        self.logica.objeto_usuario = eleccion_usuario

        # Animación y elección de la máquina
        self.animacion_maquina()

    def animacion_maquina(self):
        imagenes = list(self.imagenes.values())

        def actualizar_imagen(i):
            if i < 10:  # Mostrar animación durante 10 ciclos
                eleccion_random = random.choice(imagenes)
                self.img_maquina.config(image=eleccion_random)
                self.img_maquina.image = eleccion_random
                self.ventana.after(100, actualizar_imagen, i + 1)
            else:
                # Selección definitiva de la máquina
                self.logica.eleccion_maquina()
                eleccion_final = self.logica.objeto_maquina
                eleccion_imagen = self.imagenes[eleccion_final]
                self.img_maquina.config(image=eleccion_imagen)
                self.img_maquina.image = eleccion_imagen

                # Determinar resultado
                self.mostrar_resultado()

        actualizar_imagen(0)

    def mostrar_resultado(self):
        resultado = self.logica.elegir_ganador()

        if resultado == 0:
            mensaje = "¡Es un empate!"
        elif resultado == 1:
            mensaje = "¡Ganaste!"
            self.puntos_usuario += 1
        else:
            mensaje = "¡La máquina ganó!"
            self.puntos_maquina += 1

        # Actualizar puntuación
        self.puntuacion_label.config(
            text=f"Tú: {self.puntos_usuario} | Máquina: {self.puntos_maquina}"
        )

        # Mostrar mensaje del resultado
        messagebox.showinfo("Resultado", mensaje)


if __name__ == "__main__":
    app = Interfaz()
    app.ventana.mainloop()
