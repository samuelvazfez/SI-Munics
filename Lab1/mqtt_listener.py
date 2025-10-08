import paho.mqtt.client as mqtt
import tor
import mqtt_sender as mqtt_client
import logging
import time
from collections import defaultdict, deque
from datetime import datetime
from config import BROKER_HOST, BROKER_USER, BROKER_PWD, BROKER_PORT, KEEPALIVE, MY_ID

# Estadísticas globales
stats = {
    'messages_received': 0,
    'messages_forwarded': 0,
    'final_messages': 0,
    'errors': 0,
    'senders': defaultdict(int),
    'last_messages': deque(maxlen=10)
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def get_next_hop(payload: bytes) -> str:
    # Devolvemos el next-hop decodificado (5 bytes, padded con \\x00 a la derecha)
    if len(payload) < 5:
        return ""
    hop_bytes = payload[:5]
    return hop_bytes.rstrip(b'\x00').decode('ascii', errors='ignore')
def on_message(client, userdata, msg):
    logging.debug("Mensaje recibido en topic %s (len=%d)", msg.topic, len(msg.payload))
    try:
        decrypted = tor.decrypt_hybrid(msg.payload)
    except Exception as e:
        logging.exception("Fallo al descifrar la capa; descartando mensaje")

    if len(decrypted) < 5:
        logging.error("Payload descifrado demasiado corto: %d bytes", len(decrypted))
        return
    
    next_hop = get_next_hop(decrypted)   # string, p.ej. 'svf' o 'end'
    inner = decrypted[5:]

    if next_hop.lower() == "end":
        # destinatario final: inner = sender(5 bytes) || message bytes
        if len(inner) < 5:
            logging.error("Inner demasiado corto para contener sender + message")
            return
        sender = inner[:5].rstrip(b'\x00').decode('ascii', errors='ignore')
        message_bytes = inner[5:]
        # decode seguro en utf-8 
        message_text = message_bytes.decode('utf-8', errors='replace')

        # Estadísticas simples 
        stats['senders'][sender] += 1
        stats['last_messages'].append({
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'from': sender,
            'message': message_text,
            'size': len(msg.payload)
        })

        logging.info("Mensaje final recibido. De: %s — Contenido: %s", sender, message_text)
    else:
        # reenvío al siguiente hop: publicamos EXACTAMENTE los bytes 'inner'
        try:
            client.publish(next_hop, payload=inner, qos=1)
            logging.info("🔄 Reenviado %d bytes a %s", len(inner), next_hop)
        except Exception:
            logging.exception("Error al reenviar a %s", next_hop)

def show_stats():
    """Mostrar estadísticas en formato legible"""
    print("\n" + "="*50)
    print("📊 ESTADÍSTICAS DEL NODO TOR")
    print("="*50)
    print(f"🔸 ID del nodo: {MY_ID}")
    print(f"🔸 Mensajes recibidos: {stats['messages_received']}")
    print(f"🔸 Mensajes reenviados: {stats['messages_forwarded']}")
    print(f"🔸 Mensajes finales: {stats['final_messages']}")
    print(f"🔸 Errores: {stats['errors']}")

    if stats['senders']:
        print("\n👤 Top remitentes:")
        for sender, count in sorted(stats['senders'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {sender}: {count} mensajes")
    
    if stats['last_messages']:
        print(f"\nÚltimos {len(stats['last_messages'])} mensajes:")
        for msg in list(stats['last_messages'])[-5:]:
            print(f"   [{msg['timestamp']}] {msg['from']}: {msg['message'][:50]}...")

def show_help():
    """Mostrar ayuda del menú"""
    print("\n" + "="*50)
    print("🎮 COMANDOS DISPONIBLES")
    print("="*50)
    print("stats  - Mostrar estadísticas")
    print("clear  - Limpiar estadísticas")
    print("log    - Cambiar nivel de log (DEBUG/INFO/WARNING/ERROR)")
    print("help   - Mostrar esta ayuda")
    print("exit   - Salir del programa")
    print("="*50)

def clear_stats():
    """Limpiar todas las estadísticas"""
    global stats
    stats = {
        'messages_received': 0,
        'messages_forwarded': 0,
        'final_messages': 0,
        'errors': 0,
        'senders': defaultdict(int),
        'last_messages': deque(maxlen=10)
    }
    print("✅ Estadísticas limpiadas")

def change_log_level():
    """Cambiar nivel de logging"""
    levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR'}
    print("\nNiveles disponibles: DEBUG, INFO, WARNING, ERROR")
    level = input("Nuevo nivel: ").upper()
    if level in levels:
        logging.getLogger().setLevel(getattr(logging, level))
        print(f"✅ Nivel de log cambiado a {level}")
    else:
        print("❌ Nivel no válido")

def menu_loop(client):
    """Bucle principal del menú interactivo"""
    show_help()
    
    while True:
        try:
            cmd = input("\n▶️  Comando: ").strip().lower()
            
            if cmd == 'stats':
                show_stats()
            elif cmd == 'clear':
                clear_stats()
            elif cmd == 'log':
                change_log_level()
            elif cmd == 'help':
                show_help()
            elif cmd in ['exit', 'quit', 'q']:
                print("👋 Saliendo...")
                break
            elif cmd == '':
                continue
            else:
                print("❌ Comando no reconocido. Escribe 'help' para ver opciones.")
                
        except KeyboardInterrupt:
            print("\n👋 Saliendo...")
            break
        except Exception as e:
            print(f"❌ Error en el menú: {e}")


# Configuration del cliente
def mqtt_client(server, port, topic, user, password, keepalive):
    client = mqtt.Client()
    client.on_message = on_message
    client.username_pw_set(user, password)
    client.connect(server, port, keepalive)
    client.subscribe(topic)
    return client

if __name__ == "__main__":
    print("🚀 Iniciando Nodo TOR MQTT...")
    print(f"📡 Conectando a {BROKER_HOST} como '{MY_ID}'")
    
    client = mqtt_client(BROKER_HOST, BROKER_PORT, MY_ID, BROKER_USER, BROKER_PWD, KEEPALIVE)
    
    # Iniciar loop MQTT en un hilo separado
    client.loop_start()
    
    # Banner de inicio
    print("✅ Conectado al broker MQTT")
    print("🎧 Escuchando mensajes...")
    print("💡 Escribe 'help' para ver comandos disponibles")
    
    try:
        menu_loop(client)
    finally:
        print("🔌 Desconectando del broker...")
        client.loop_stop()
        client.disconnect()

