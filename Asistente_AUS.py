import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

#id de las voces de los asistentes virtuales en mi maquina
id1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"
id2 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

# escuchar microfono y devolver audio como texto
def transforma_audio_texto():
    #almacenara el reconocedor en una variable
    r = sr.Recognizer()
    #confirar microfono
    with sr.Microphone() as origen:
        #timepo de espera
        r.pause_threshold = 1.00
        #informar que comenzo la grabacion
        print("ya puedesd hablar :)")
        #guardar el audio que se escuche
        audio = r.listen(origen)

        try:
            #buscar en google lo que se escuche
            pedido = r.recognize_google(audio,language = "es-mx")
            # prueba de que puede transformar mi voz;
            print(f"has dicho: ^^^^{pedido}")

            #devolver a pedido
            return pedido
        #en caso de no comprender el audio:
        except sr.UnknownValueError:
            #prueba de que no comprendio
            print("no se entendio el audio")
            #devolver error
            return "habla de nuevo"
        #en caso de no resolver el pedido
        except sr.RequestError:
            print("el prgrama fallo")
            # devolver error
            return "habla de nuevo"
        #error inesperado
        except :
            print("algo salio mal")
            # devolver error
            return "habla de nuevo"

#funcion para que el asistende voz pueda ser escuchado
def hablar(mensaje):
    #encender erl motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice',id1)
    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

#dar dia de la semana
def pedir_dia():
    #crear la variable con datos de hoy
    dia = datetime.date.today()
    print(dia)
    #crear una variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)
    #diccionario con nombres de los dias
    calendario = {0:"Lunes",1:"Martes",2:"Mièrcoles",3:"Juebebes",4:"Viernes",5:"Sèbado",6:"Domingo"}
    #decir el dia de la semana
    hablar(f" Hoy es {calendario[dia_semana]} Makina")

#informar Hora
def pedir_hora():
    #crear unma variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f"en este momento son: las {hora.hour} con {hora.minute} minutos y con {hora.second} segundos"
    print(hora)

    #decir hora
    hablar(hora)
#funcion del saludo inicial
def saludo_inicial():
    #variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buenos dias'
    else:
        momento = 'Buenas tardes'
    #decir el saludo
    hablar(f"{momento} soy Sabina, tu asistente de paithon, ¿que puedo hacer por ti?")

#funcion main del asistente
def pedir_cosas():
    saludo_inicial()
    #variable de corte
    comenzar = True
    while comenzar:
        #activa el miocrofono y guarda la orden en un texto
        pedido = transforma_audio_texto().lower()
        if 'abrir youtube' in pedido:
            hablar(" abrire youtube")
            webbrowser.open("https://www.youtube.com/watch?v=qF9ndkfdyNw")
            continue
        elif 'abrir el navegador' in pedido:
            hablar("vamos a abrir el navegador")
            webbrowser.open("https://www.google.com/")
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar("vamos a buscarlo en wikipedia")
            pedido = pedido.replace('busca en wikipedia','')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido,sentences = 1)
            hablar('Wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('vamos a buscar')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('encontre esto, gracias:')
            continue
        elif 'reproducir' in pedido:
            hablar('buen tema. lo pongo ahora')
            pedido = pedido.replace('reproducir', '')
            pywhatkit.playonyt(pedido)
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de ')[-1].strip()
            print(accion)
            cartera = {'apple':'APPL','amazon':'AMZN',
                       'google':'GOOGL'}
            try:
                accion_buscada = cartera(accion)
                print(accion_buscada)
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketplace']
                hablar(f" la encontre el precio de: {accion} es {precio_actual}")
                continue
            except:
                hablar("Perdon no encontre tus acciones")
                continue
        elif 'adiós' in pedido:
            hablar("Ten un buen día si me necesitas enciendeme")
            break







pedir_cosas()