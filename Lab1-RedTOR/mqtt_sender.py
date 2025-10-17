import paho.mqtt.client as mqtt
import tor
import time
from config import BROKER_HOST, BROKER_USER, BROKER_PWD, BROKER_PORT, KEEPALIVE, MY_ID

# Configuracion del cliente 
def mqtt_client (server, port, topic, user, password, keepalive):
    client = mqtt.Client()
    client.username_pw_set(user, password)
    client.connect(server, port, keepalive)
    client.subscribe(topic)
    return client

# Creamos el ciente MQTT
if __name__ == "__main__":
    client = mqtt_client(BROKER_HOST, BROKER_PORT, MY_ID, BROKER_USER, BROKER_PWD, KEEPALIVE)

    # Ejemplo de mensaje y ruta (ajusta según necesites)
    cipher_message = b"Prueba para el trabajo siendo anonimo"
    path = ["svf", "acu"]  

    encrypted_to_send = tor.encrypt_nested_hybrid(path, cipher_message)

    # Iniciar loop para que el hilo de red de paho procese la publicación
    client.loop_start()
    
    print("SENDER: len:", len(encrypted_to_send))
    print("SENDER: prefix hex:", encrypted_to_send[:64].hex())

    publish_result = client.publish(path[0], payload=encrypted_to_send, qos=1)
    
    publish_result.wait_for_publish()
    time.sleep(0.1)  
    client.loop_stop()
    client.disconnect()

    print(f"Mensaje cifrado publicado en el topic '{path[0]}'")