import tkinter as tk
from tkinter import messagebox
import random

# Clase principal para la interfaz gráfica del juego
class DetectivePastGUI:

    # Constructor de la clase
    # Inicializa la ventana principal y configura el estilo
    def __init__(self, master):
        self.master = master
        master.title("Detective Past")
        
        # Configuración de la ventana principal
        master.geometry("600x600")
        master.configure(bg="#f0f0f0")
        master.resizable(False, False)

        # Fuentes y colores
        self.title_font = ("Arial", 18, "bold")
        self.text_font = ("Arial", 12)
        self.button_font = ("Arial", 10)
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.accent_color = "#e74c3c"

        # Lista de historias
        # Cada historia contiene un título, preguntas con verbos y un misterio
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
    

    #Método para mostrar las historias disponibles
    def mostrar_seleccion_historia(self):
        self.limpiar_pantalla()
        
        # Marco principal con estilo similar al boceto
        main_frame = tk.Frame(self.master, bg="#f0f0f0")
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Título
        titulo_label = tk.Label(main_frame, text="¡Bienvenido a Detective Past!", 
                              font=self.title_font, bg="#f0f0f0", fg=self.primary_color)
        titulo_label.pack(pady=(0, 20))
        
        # Subtítulo
        subtitulo_label = tk.Label(main_frame, text="Elige una historia para resolver:", 
                                 font=self.text_font, bg="#f0f0f0")
        subtitulo_label.pack(pady=(0, 20))
        
        # Marco para los botones de historias
        historias_frame = tk.Frame(main_frame, bg="#f0f0f0")
        historias_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botones de historias
        for i, historia in enumerate(self.historias):
            boton_historia = tk.Button(historias_frame, text=historia["titulo"], 
                                      font=self.button_font, bg=self.secondary_color, fg="white",
                                      command=lambda i=i: self.cargar_historia(i),
                                      padx=20, pady=10, relief=tk.FLAT)
            boton_historia.pack(pady=5, fill=tk.X)

    # Método para cargar la historia seleccionada
    # Inicializa las preguntas, el misterio y la respuesta correcta
    # Reinicia las vidas y aciertos
    # Limpia la pantalla y muestra la primera pregunta
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


    # Método para limpiar la pantalla
    # Elimina todos los widgets de la ventana principal
    # Reinicia la lista de botones de opciones
    def limpiar_pantalla(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.opcion_botones = []


    # Método para mostrar la pregunta actual
    # Muestra el nivel, la historia con un hueco, las opciones de respuesta y la barra inferior
    # Si se han respondido todas las preguntas o se han perdido todas las vidas, muestra el resultado final
    # Si la pregunta actual es válida, muestra el marco principal y los elementos de la interfaz
    # Si no, muestra el resultado final
    def mostrar_pregunta(self):
        if self.indice_pregunta < len(self.preguntas) and self.vidas > 0:
            # Configuración del contenedor principal
            main_frame = tk.Frame(self.master, bg="#f0f0f0")
            main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
            
            # Encabezado con el nivel actual
            nivel_label = tk.Label(main_frame, text=f"Level {self.indice_pregunta + 1}", 
                                 font=self.title_font, bg="#f0f0f0", fg=self.primary_color)
            nivel_label.pack(anchor=tk.W, pady=(0, 20))
            
            self.pregunta_actual = self.preguntas[self.indice_pregunta]
            historia_con_hueco = self.pregunta_actual["historia"].replace("__________", "_____")
            
            # Etiqueta para la historia con hueco
            # Se crea una etiqueta con el texto de la historia y un hueco para el verbo
            historia_label = tk.Label(main_frame, text=historia_con_hueco, 
                                    wraplength=500, justify="left",
                                    font=self.text_font, bg="#f0f0f0")
            historia_label.pack(pady=10, fill=tk.X)
            
            # Marco para las opciones de respuesta
            # Se crea un marco para contener las opciones de respuesta
            opciones_frame = tk.Frame(main_frame, bg="#f0f0f0")
            opciones_frame.pack(pady=20)
            
            opciones = self.pregunta_actual["verbo"]["opciones"]
            random.shuffle(opciones)
            
            # Crear botones de opciones
            # Se crean 3 botones de opción, cada uno con un texto diferente
            for i in range(3):
                opcion_frame = tk.Frame(opciones_frame, bg="#f0f0f0")
                opcion_frame.pack(fill=tk.X, pady=5)
                
                # Botón de opción
                # Se crea un botón para cada opción de respuesta   
                boton_opcion = tk.Button(opcion_frame, text=opciones[i], 
                                       font=self.button_font, bg="white", fg="black",
                                       relief=tk.FLAT, bd=1,
                                       command=lambda opcion=opciones[i]: self.verificar_respuesta(opcion))
                boton_opcion.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.opcion_botones.append(boton_opcion)
            

            # Barra inferior
            # Se crea un marco para contener los botones de la barra inferior
            bottom_frame = tk.Frame(main_frame, bg="#f0f0f0")
            bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
            
            # Botón de reiniciar
            tk.Button(bottom_frame, text="Reiniciar", font=self.button_font, 
                     command=self.reiniciar_juego, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
            
            # Botón de salir
            tk.Button(bottom_frame, text="Exit", font=self.button_font, 
                     command=self.master.quit, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
            

            # Mostrar vidas restantes
            # Se crea un marco para mostrar las vidas restantes
            # Se muestra el número de vidas restantes con un icono de corazón
            vidas_frame = tk.Frame(bottom_frame, bg="#f0f0f0")
            vidas_frame.pack(side=tk.RIGHT)
            tk.Label(vidas_frame, text=f"Vidas: {'♥ ' * self.vidas}", 
                    font=self.button_font, fg=self.accent_color, bg="#f0f0f0").pack()
        
            
        else:
            # Si se han respondido todas las preguntas o se han perdido todas las vidas
            # Se muestra el resultado final
            self.mostrar_resultado_final()

    # Método para verificar la respuesta del usuario
    # Compara la respuesta del usuario con la respuesta correcta
    # Si la respuesta es correcta, aumenta el número de aciertos
    # Si la respuesta es incorrecta, disminuye el número de vidas
    def verificar_respuesta(self, respuesta_usuario):
        if self.pregunta_actual:
            # Verifica si la respuesta del usuario es correcta
            # Si la respuesta es correcta, muestra un mensaje de éxito
            if respuesta_usuario == self.pregunta_actual["verbo"]["pasado"]:
                messagebox.showinfo("Correcto", "¡Respuesta correcta!")
                self.aciertos += 1
            else:
                # Si la respuesta es incorrecta, muestra un mensaje de error
                # Disminuye el número de vidas
                self.vidas -= 1
                messagebox.showerror("Incorrecto", f"¡Respuesta incorrecta! La correcta era: {self.pregunta_actual['verbo']['pasado']}.")

            
            self.indice_pregunta += 1
            self.limpiar_pantalla()
            self.mostrar_pregunta()

    # Método para mostrar el resultado final
    # Muestra el resultado final del juego
    # Muestra el progreso del jugador y la historia completa
    # Si el jugador ha completado todas las preguntas, muestra la recompensa
    # Si no, muestra un mensaje de error
    def mostrar_resultado_final(self):
        self.limpiar_pantalla()
        
        # Contenedor principal
        # Se crea un marco principal para contener todos los elementos de la interfaz
        main_container = tk.Frame(self.master, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        

        # Encabezado
        # Se crea un marco para el encabezado
        header_frame = tk.Frame(main_container, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Icono de resultado
        # Se muestra un icono de éxito o error dependiendo del resultado
        result_icon = "✓" if self.aciertos == len(self.preguntas) else "✗"
        icon_color = "#2ecc71" if self.aciertos == len(self.preguntas) else "#e74c3c"
        
        tk.Label(header_frame, text=result_icon, font=("Arial", 24), 
                fg=icon_color, bg="#f0f0f0").pack(side=tk.LEFT, padx=(0, 15))
        

        # Título y subtítulo
        # Se muestra un título y un subtítulo dependiendo del resultado
        if self.aciertos == len(self.preguntas):
            title_text = "¡Misión Cumplida!"
            subtitle_text = "Has resuelto el misterio"
        else:
            title_text = "¡Casi lo logras!"
            subtitle_text = "El misterio sigue sin resolver"
        
        title_frame = tk.Frame(header_frame, bg="#f0f0f0")
        title_frame.pack(side=tk.LEFT)
        
        tk.Label(title_frame, text=title_text, font=("Arial", 18, "bold"), 
                fg="#2c3e50", bg="#f0f0f0").pack(anchor=tk.W)
        tk.Label(title_frame, text=subtitle_text, font=("Arial", 12), 
                fg="#7f8c8d", bg="#f0f0f0").pack(anchor=tk.W)
        
        
        # Progreso
        # Se crea un marco para mostrar el progreso del jugador
        # Se muestra el número de aciertos y el total de preguntas
        progress_frame = tk.Frame(main_container, bg="#f0f0f0")
        progress_frame.pack(fill=tk.X, pady=(0, 25))
        
        total_preguntas = len(self.preguntas)
        progress_percent = self.aciertos / total_preguntas
        

        # Texto de progreso
        # Se muestra el progreso del jugador en porcentaje
        # Se muestra el número de aciertos y el total de preguntas
        tk.Label(progress_frame, 
                text=f"Progreso: {self.aciertos}/{total_preguntas} ({int(progress_percent*100)}%)",
                font=("Arial", 11), bg="#f0f0f0", fg="#34495e").pack(anchor=tk.W)
        

        # Barra de progreso
        # Se crea un marco para mostrar la barra de progreso
        # Se muestra el progreso del jugador en forma de barra
        progress_bg = tk.Frame(progress_frame, height=20, bg="#ecf0f1")
        progress_bg.pack(fill=tk.X, pady=5)
        
        progress_fg = tk.Frame(progress_bg, height=20, 
                            bg=icon_color, width=progress_bg.winfo_reqwidth()*progress_percent)
        progress_fg.pack(side=tk.LEFT)
        

        # Sección de recompensa (solo si completó todo)
        if self.aciertos == total_preguntas:
            reward_frame = tk.Frame(main_container, bg="#e8f4f8", bd=1, relief=tk.SOLID)
            reward_frame.pack(fill=tk.X, pady=(0, 20))
            
            tk.Label(reward_frame, text="🔍 Recompensa", font=("Arial", 12, "bold"), 
                    bg="#e8f4f8", fg="#16a085").pack(anchor=tk.W, padx=10, pady=5)
            
            tk.Label(reward_frame, text=self.misterio, font=("Arial", 11, "italic"), 
                    bg="#e8f4f8", fg="#34495e").pack(anchor=tk.W, padx=10)
            
            tk.Label(reward_frame, text=f"Respuesta: {self.respuesta_correcta_misterio}", 
                    font=("Arial", 11), bg="#e8f4f8", fg="#34495e").pack(anchor=tk.W, padx=10, pady=(0, 10))
        

        # Sección de historia completa
        # Se crea un marco para mostrar la historia completa
        # Se muestra la historia completa con los verbos en pasado
        story_frame = tk.LabelFrame(main_container, text=" Historia Completa ", 
                                font=("Arial", 12, "bold"), bg="white", fg="#2c3e50",
                                padx=10, pady=10)
        story_frame.pack(fill=tk.BOTH, expand=True)
        

        # Texto de la historia completa
        # Se crea un widget de texto para mostrar la historia completa
        story_text = tk.Text(story_frame, wrap=tk.WORD, font=("Arial", 11), 
                            bg="white", fg="#333333", padx=5, pady=5,
                            height=8, width=60, relief=tk.FLAT)
        
        historia_completa_texto = ""
        for pregunta in self.historia_actual["preguntas"]:
            verbo_correcto = pregunta["verbo"]["pasado"]
            historia_completa_texto += pregunta["historia"].replace("__________", verbo_correcto) + " "
        
        story_text.insert(tk.END, historia_completa_texto)
        story_text.config(state=tk.DISABLED)
        
        scrollbar = tk.Scrollbar(story_frame, orient=tk.VERTICAL, command=story_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        story_text.config(yscrollcommand=scrollbar.set)
        story_text.pack(fill=tk.BOTH, expand=True)
        

        # Botón de reiniciar
        # Se crea un marco para contener los botones de reinicio y salir
        button_frame = tk.Frame(main_container, bg="#f0f0f0", pady=15)
        button_frame.pack(fill=tk.X)
        
        btn_style = {"font": ("Arial", 12), "padx": 25, "pady": 8, "bd": 0}
        
        tk.Button(button_frame, text="Jugar Otra Historia", 
                bg="#3498db", fg="white", **btn_style,
                command=self.reiniciar_juego).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Repetir Esta Historia", 
                bg="#f39c12", fg="white", **btn_style,
                command=lambda: self.cargar_historia(self.historias.index(self.historia_actual))).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Salir", 
                bg="#e74c3c", fg="white", **btn_style,
                command=self.master.quit).pack(side=tk.RIGHT, padx=10)
        

        # Actualizar la ventana
        # Se actualiza la ventana para mostrar todos los elementos
        self.master.update_idletasks()
        

    # Método para reiniciar el juego
    # Limpia la pantalla y muestra la selección de historias
    def reiniciar_juego(self):
        self.mostrar_seleccion_historia()

# Método principal para ejecutar la aplicación
# Crea una instancia de la clase DetectivePastGUI y ejecuta el bucle principal
if __name__ == "__main__":
    root = tk.Tk()
    gui = DetectivePastGUI(root)
    root.mainloop()
