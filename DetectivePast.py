import tkinter as tk
from tkinter import messagebox
import random

# Clase principal para la interfaz gráfica del juego "Detective Past"
# Esta clase maneja la lógica del juego, la selección de historias y preguntas, y la interacción con el usuario.
# La interfaz gráfica se construye utilizando la biblioteca tkinter de Python.
class DetectivePastGUI:
    # Este método inicializa la clase y configura la ventana principal del juego.
    def __init__(self, master):
        self.master = master
        master.title("Detective Past")
        
        master.geometry("500x500")
        master.configure(bg="lightblue")
        master.resizable(False, False)

        # Definición de las historias y preguntas del juego
        # Cada historia tiene un título, una lista de preguntas con un verbo en pasado y presente, y un misterio a resolver.
        # Las preguntas contienen un texto con un espacio en blanco que el jugador debe completar con la forma correcta del verbo.
        self.historias = [
            {
                "titulo": "The Case of the Missing Painting",
                "preguntas": [
                    {
                        "historia": "Once upon a time, in a small town, a mysterious event __________. A valuable painting disappeared from the local museum and nobody saw nothing. The detective, Sherlock Holmes, was called to solve the case.",
                        "verbo": {"presente": "happen", "pasado": "happened", "opciones": ["happened", "happening", "happens"]}
                    },
                    {
                        "historia": "Sherlock Holmes arrived at the museum and __________ to investigate. He asked the curator about the last time the painting was seen. The curator said that it was last seen on Friday.",
                        "verbo": {"presente": "start", "pasado": "started", "opciones": ["started", "starting", "starts"]}
                    },
                    {
                        "historia": "The detective then interviewed several witnesses. One witness said that he __________ a suspicious person near the museum on Friday. Another witness said that she heard a strange noise coming from the museum that night.",
                        "verbo": {"presente": "see", "pasado": "saw", "opciones": ["saw", "see", "seen"]}
                    },
                    {
                        "historia": "Sherlock Holmes carefully examined the museum and __________ a clue. He discovered a footprint near the window where the painting was stolen. The footprint belonged to a well-known thief.",
                        "verbo": {"presente": "find", "pasado": "found", "opciones": ["found", "finding", "finds"]}
                    },
                    {
                        "historia": "After gathering all the evidence, Sherlock Holmes put the pieces together. He __________ that the thief was someone who worked at the museum. He confronted the thief and recovered the painting.",
                        "verbo": {"presente": "realize", "pasado": "realized", "opciones": ["realized", "realizing", "realizes"]}
                    }
                ],
                "misterio": "¿Quién robó la pintura?",
                "respuesta_correcta_misterio": "Alguien que trabajaba en el museo."
            },
            {
                "titulo": "The Mystery of the Locked Room",
                "preguntas": [
                    {
                        "historia": "A famous writer __________ dead in his locked study. The only window was bolted from the inside, and the door __________ locked with the key in the writer's pocket.",
                        "verbo": {"presente": "be", "pasado": "was", "opciones": ["was", "is", "were"]}
                    },
                    {
                        "historia": "The detective, Inspector Davies, __________ at the seemingly impossible crime scene and __________ to observe every detail.",
                        "verbo": {"presente": "arrive", "pasado": "arrived", "opciones": ["arrived", "arriving", "arrives"]}
                    },
                    {
                        "historia": "He __________ the room carefully, noting the position of the body and the lack of any forced entry.",
                        "verbo": {"presente": "examine", "pasado": "examined", "opciones": ["examined", "examining", "examines"]}
                    },
                    {
                        "historia": "The inspector __________ the servants, each of whom had an alibi for the time of the murder.",
                        "verbo": {"presente": "interview", "pasado": "interviewed", "opciones": ["interviewed", "interviewing", "interviews"]}
                    },
                    {
                        "historia": "Finally, Inspector Davies __________ the solution: the writer had committed suicide using a clever trick.",
                        "verbo": {"presente": "deduce", "pasado": "deduced", "opciones": ["deduced", "deducing", "deduces"]}
                    }
                ],
                "misterio": "¿Cómo murió el escritor en la habitación cerrada?",
                "respuesta_correcta_misterio": "Se suicidó usando un truco."
            }
        ]

        self.historia_actual = None
        self.preguntas = []
        self.pregunta_actual = None
        self.vidas = 3
        self.aciertos = 0
        self.indice_pregunta = 0
        self.opcion_botones = []

    
        self.mostrar_seleccion_historia()
    
    def mostrar_seleccion_historia(self):
        self.limpiar_pantalla()
        titulo_label = tk.Label(self.master, text="¡Bienvenido a Detective Past!", font=("Arial", 16))
        titulo_label.pack(pady=10)
        instrucciones_label = tk.Label(self.master, text="Elige una historia para resolver:", justify="left")
        instrucciones_label.pack(pady=5)

        for i, historia in enumerate(self.historias):
            boton_historia = tk.Button(self.master, text=historia["titulo"], command=lambda i=i: self.cargar_historia(i))
            boton_historia.pack(pady=5)


    # Este método carga la historia seleccionada y prepara las preguntas para el juego.
    # Inicializa las variables necesarias para el juego, como el número de vidas y aciertos.
    # También se encarga de limpiar la pantalla y mostrar la primera pregunta al jugador.
    def cargar_historia(self, indice_historia):
        self.historia_actual = self.historias[indice_historia]
        self.preguntas = list(self.historia_actual["preguntas"])
        self.misterio = self.historia_actual["misterio"]
        self.respuesta_correcta_misterio = self.historia_actual["respuesta_correcta_misterio"]
        self.vidas = 3
        self.aciertos = 0
        self.indice_pregunta = 0
        self.limpiar_pantalla()
        self.mostrar_pregunta()

    # Este método se encarga de limpiar la pantalla de la interfaz gráfica, eliminando todos los widgets existentes.
    # Esto es útil para preparar la pantalla para mostrar una nueva pregunta o resultado final.
    def limpiar_pantalla(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.opcion_botones = []

    # Este método muestra la pregunta actual al jugador, incluyendo la historia con un espacio en blanco y las opciones de respuesta.
    # También muestra el número de vidas restantes.
    # Si el jugador ha respondido todas las preguntas o se ha quedado sin vidas, se muestra el resultado final.
    # Las opciones de respuesta se barajan para que el jugador no pueda predecir la respuesta correcta.
    # La historia se muestra con un espacio en blanco que el jugador debe completar con la forma correcta del verbo.
    def mostrar_pregunta(self):
        if self.indice_pregunta < len(self.preguntas) and self.vidas > 0:
            self.pregunta_actual = self.preguntas[self.indice_pregunta]
            historia_con_hueco = self.pregunta_actual["historia"].replace("__________", "_____")

            historia_label = tk.Label(self.master, text=historia_con_hueco, wraplength=400, justify="left")
            historia_label.pack(pady=10)

            opciones = self.pregunta_actual["verbo"]["opciones"]
            random.shuffle(opciones)
            for i in range(3):
                boton_opcion = tk.Button(self.master, text=opciones[i], command=lambda opcion=opciones[i]: self.verificar_respuesta(opcion))
                self.opcion_botones.append(boton_opcion)
                boton_opcion.pack(pady=5)

            vidas_label = tk.Label(self.master, text=f"Vidas: {self.vidas}")
            vidas_label.pack(pady=10)
        else:
            self.mostrar_resultado_final()


    # Este método verifica la respuesta del jugador comparándola con la respuesta correcta.
    # Si la respuesta es correcta, se incrementa el número de aciertos y se muestra un mensaje de éxito.
    # Si la respuesta es incorrecta, se decrementa el número de vidas y se muestra un mensaje de error.
    # Después de cada respuesta, se avanza a la siguiente pregunta o se muestra el resultado final si no hay más preguntas.
    # Si el jugador se queda sin vidas, se muestra un mensaje de error y se termina el juego.
    # Si el jugador responde correctamente a todas las preguntas, se muestra un mensaje de éxito y se revela el misterio.
    # También se muestra la historia completa con las respuestas correctas.
    def verificar_respuesta(self, respuesta_usuario):
        if self.pregunta_actual:
            if respuesta_usuario == self.pregunta_actual["verbo"]["pasado"]:
                messagebox.showinfo("Correcto", "¡Respuesta correcta!")
                self.aciertos += 1
            else:
                self.vidas -= 1
                messagebox.showerror("Incorrecto", f"¡Respuesta incorrecta! La correcta era: {self.pregunta_actual['verbo']['pasado']}.")

            self.indice_pregunta += 1
            self.limpiar_pantalla()
            self.mostrar_pregunta()


    # Este método muestra el resultado final del juego, incluyendo el número de aciertos y vidas restantes.
    # Si el jugador ha respondido todas las preguntas correctamente, se muestra un mensaje de éxito y se revela el misterio.
    # Si el jugador se ha quedado sin vidas, se muestra un mensaje de error y se ofrece la opción de jugar de nuevo o salir.
    # También se muestra la historia completa con las respuestas correctas.
    def mostrar_resultado_final(self):
        self.limpiar_pantalla()
        titulo_label = tk.Label(self.master, text="--- Resultado Final ---", font=("Arial", 16))
        titulo_label.pack(pady=10)
        total_preguntas = len(self.preguntas)
        resultado_texto = f"Aciertos: {self.aciertos} de {total_preguntas}\n"

        if self.aciertos == total_preguntas:
            resultado_texto += "¡Impecable trabajo de detective! Has resuelto el misterio.\n"
            respuesta_misterio_label = tk.Label(self.master, text=f"\nMisterio: {self.misterio}\nRespuesta: {self.respuesta_correcta_misterio}", justify="left")
            respuesta_misterio_label.pack(pady=5)
            historia_completa_texto = "\n--- Historia Completa ---\n"
            for pregunta in self.historia_actual["preguntas"]:
                verbo_correcto = pregunta["verbo"]["pasado"]
                historia_completa_texto += pregunta["historia"].replace("__________", verbo_correcto) + " "
            historia_completa_label = tk.Label(self.master, text=historia_completa_texto, justify="left", wraplength=400)
            historia_completa_label.pack(pady=5)
        else:
            resultado_texto += f"Te quedaste sin vidas. El misterio sigue sin resolverse.\n"
            resultado_texto += "¿Quieres intentarlo de nuevo?"
            respuesta_misterio_label = tk.Label(self.master, text=resultado_texto, justify="left")
            respuesta_misterio_label.pack(pady=5)

        reiniciar_button = tk.Button(self.master, text="Jugar de Nuevo", command=self.reiniciar_juego)
        reiniciar_button.pack(pady=10)
        salir_button = tk.Button(self.master, text="Salir", command=self.master.quit)
        salir_button.pack(pady=5)


    # Este método reinicia el juego, volviendo a la pantalla de selección de historias.
    # Se limpia la pantalla y se muestra la lista de historias disponibles para que el jugador elija una nueva historia.
    # También se restablecen todas las variables del juego a su estado inicial.
    # Esto permite al jugador comenzar una nueva partida sin necesidad de cerrar la aplicación.
    def reiniciar_juego(self):
        self.mostrar_seleccion_historia()

if __name__ == "__main__":
    root = tk.Tk()
    gui = DetectivePastGUI(root)
    root.mainloop()