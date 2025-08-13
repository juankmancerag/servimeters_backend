# main.py

#Calcula el total de órdenes, por servicio y por ciudad

from src.agents.agents import agente_orquestador

def main():
    print("🧠 Bienvenido al Agente Programador Servimeters. Escribe 'salir' para terminar.\n")
    agente = agente_orquestador.agente_orquestador()

    while True:
        mensaje = input("Tú: ")
        if mensaje.lower() in ["salir", "exit", "quit"]:
            print("👋 ¡Gracias por usar el Agente Servimeters!")
            break

        respuesta = agente.responder(mensaje)
        print("🤖 Agente:\n", respuesta)
        print("-" * 60)

if __name__ == "__main__":
    main()
