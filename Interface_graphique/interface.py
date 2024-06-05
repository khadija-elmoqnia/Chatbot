from tkinter import *
from chatbot.reponse import getResponse
from PIL import Image, ImageTk
from tkinter.scrolledtext import ScrolledText

message_list = []
bot_label_writing = None

def send():
    global message_list
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    if msg != '':
        message_list.append("You: " + msg)
        show_user_message("You: " + msg)
        base.after(500, lambda: delayed_bot_response(msg))
        remove_initial_message()

def delayed_bot_response(msg):
    ChatLog.config(state=NORMAL)
    ChatLog.insert(END, "\n\n")
    ChatLog.config(state=DISABLED)
    show_writing_message()
    base.after(100, lambda: bot_response(msg))


def show_user_message(message):
    global ChatLog

    ChatLog.config(state=NORMAL)
    ChatLog.tag_configure("right", justify="right", font=("Arial", 21))

    # Enregistrement de la position avant d'ajouter le message
    position = ChatLog.index(END)

    # Ajout d'un saut de ligne avant d'ajouter le message de l'utilisateur
    ChatLog.insert(END, "\n")

    # Ajout du message de l'utilisateur aligné à droite avec un fond blanc
    user_label = Label(ChatLog, text=message, bg="white", fg="black", font=("Arial", 21), justify="right", wraplength=600)
    ChatLog.window_create(position, window=user_label)

    # Configuration du tag pour le texte de l'utilisateur
    ChatLog.tag_add("user", position, position + "+1c")
    ChatLog.tag_config("user", justify="right")

    ChatLog.config(state=DISABLED)
    ChatLog.yview(END)
    ChatLog.see(END)




def show_writing_message():
    global bot_label_writing
    if bot_label_writing:
        base.after_cancel(bot_label_writing.destruction_job)
    bot_label_writing = Label(ChatLog, text="Doctor Bot: Writing...", bg="#EBF7FD", fg="black", font=("Arial", 21),
                              justify="right", wraplength=900)
    ChatLog.window_create("end", window=bot_label_writing)
    ChatLog.see("end")
    bot_label_writing.destruction_job = base.after(3000, bot_label_writing.destroy)


def bot_response(msg):
    global message_list
    res = getResponse(msg)
    lines = res.split('\n')

    ChatLog.config(state=NORMAL)

    for line in lines:
        message_list.append("Doctor Bot: " + line)
        bot_label = Label(ChatLog, text="Doctor Bot: " + line, bg="#EBF7FD", fg="black", font=("Arial", 21),
                          justify="left", wraplength=900)
        ChatLog.window_create("end", window=bot_label)
        ChatLog.insert(END, "\n")

    ChatLog.insert(END, "\n\n")  # Add a newline after displaying the bot's response
    ChatLog.yview(END)
    base.update_idletasks()
    ChatLog.config(state=DISABLED)

# Fonction pour afficher le message initial
def show_initial_message():
    global bot_label_initial
    initial_message = "Comment puis-je vous aider aujourd'hui ?"
    bot_label_initial = Label(base, text=initial_message, bg="#F6F6F6", fg="black", font=("Arial", 30), justify="left")
    bot_label_initial.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

# Fonction pour supprimer le message initial
def remove_initial_message():
    global bot_label_initial
    if bot_label_initial:
        bot_label_initial.grid_forget()


def interface(get_response_function):
    global EntryBox, ChatLog, base, bot_label_writing

    base = Tk()
    base.title("ChatBot Cardio")
    base.attributes('-fullscreen', True)
    base.config(background='white')

    img = Image.open("interface_graphique/imagebot.png")
    img = img.resize((100, 100), Image.BILINEAR)
    img = ImageTk.PhotoImage(img)

    label_img = Label(base, image=img, bg='white')
    label_img.grid(row=0, column=0, padx=5, pady=5)

    EntryBox = ScrolledText(base, bd=0, bg="#F6F6F6", width="40", height="2", font=("Arial", 14))
    EntryBox.grid(row=2, column=0, padx=5, pady=20, sticky="ew")

    ChatLog = ScrolledText(base, bd=0, bg="#F6F6F6", height=15, width="60", wrap=WORD, font=("Arial", 16))
    ChatLog.config(state=DISABLED)
    ChatLog.grid(row=1, column=0, columnspan=4, padx=5, pady=(5, 20), sticky="nsew")

    label_title = Label(base, text="Doctor Bot", image=img, compound='left', font=("Courier", 30, 'bold'), bg='white', fg='black')
    label_title.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

    SendButton = Button(base, text='Envoyer', font=("Arial", 21), bg='#84bac4', fg='black', command=send)
    SendButton.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

    QuitButton = Button(base, text='Quiter', font=("Arial", 22), bg='#BF382A', fg='black', command=base.destroy)
    QuitButton.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

    base.columnconfigure(0, weight=1)
    base.rowconfigure(1, weight=1)

    show_initial_message() 

    base.mainloop()










