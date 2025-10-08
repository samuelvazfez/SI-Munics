# 🕸️ Red TOR sobre MQTT
Sistema de comunicación anónima y segura implementando una red TOR sobre protocolo MQTT con cifrado híbrido (RSA + AES-GCM).

## 📋 Requisitos
Python 3.7+

Librerías: paho-mqtt, cryptography

## ⚙️ Configuración Inicial
### 1. Instalar dependencias
```bash
pip install paho-mqtt cryptography
```
### 2. Copiar plantilla de configuración y editar con tus datos
```bash
cp config_template.py config.py
```
### 4. Configurar claves RSA
Asegúrate de tener en el directorio:
La clave privada y la pública

## 🚀 Uso del Sistema
### 1. Iniciar Listener (Receptor)
```bash
python mqtt_listener.py
```
#### Comandos disponibles en el listener:

##### stats - Ver estadísticas de mensajes

##### clear - Limpiar estadísticas

##### log - Cambiar nivel de logging (DEBUG/INFO/WARNING/ERROR)

##### help - Mostrar ayuda

##### exit - Salir

### 2. Enviar Mensajes (Sender)
```bash
python mqtt_sender.py
```

## 🔒 Esquema de Cifrado
El sistema utiliza cifrado híbrido:

RSA-OAEP (2048 bits) para el intercambio de claves

AES-GCM (128 bits) para el cifrado de datos

Nonce de 12 bytes derivado de la clave AES


## 🎯 Nodos Disponibles
Los nodos están definidos en tor.py en el diccionario pubkey_dictionary. Algunos ejemplos:

svf, ancr, svr, etc.

## 📊 Monitoreo y Debugging
### Niveles de Logging:
#### DEBUG: Todo el flujo de cifrado/descifrado

#### INFO: Mensajes entrantes/salientes (recomendado)

#### WARNING: Solo advertencias y errores

#### ERROR: Solo errores críticos

### Estadísticas del Listener:
#### Mensajes recibidos/reenviados

#### Top remitentes

#### Últimos mensajes recibidos

#### Tasa de errores



## 📁 Estructura de Archivos
```
tor_network/
├── tor.py                 # Librería criptográfica
├── mqtt_listener.py       # Receptor de mensajes
├── mqtt_sender.py         # Enviador de mensajes
├── config_template.py     # Plantilla de configuración
├── config.py             # Configuración real (.gitignore)
├── id_rsaSIsamu          # Clave privada (.gitignore)
├── id_rsaSIsamu.pub      # Clave pública
└── README.md             # Este archivo
```

## 🔄 Flujo de Mensajes
Cifrado anidado a través de la ruta especificada

Cada nodo descifra su capa y reenvía al siguiente hop

Destino final muestra el mensaje y remitente

Anonimato preservado mediante múltiples capas de cifrado
