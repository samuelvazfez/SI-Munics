# Documentación de `demo.py`

El script `demo.py` sirve como un ejecutable de demostración que ilustra el flujo completo del esquema de **Verifiable Secret Sharing (VSS)**, desde la distribución del secreto por parte del `dealer` hasta su reconstrucción por parte del `client`.

## Funcionalidad Principal

El objetivo de este script es simular un escenario completo y mostrar los resultados de manera clara y educativa. Orquesta las dos fases principales del protocolo:

1.  **Fase de Distribución:** Un `VSSDealer` crea los shares a partir de un secreto.
2.  **Fase de Reconstrucción:** Un `VSSClient` verifica los shares y reconstruye el secreto.

## Función `demo_completa()`

Esta es la única función del script y contiene toda la lógica de la demostración.

### Comportamiento

1.  **Configuración Inicial:**
    -   Define los parámetros del esquema: un `SECRETO`, el número de participantes `N` y el umbral `T`.
    -   Imprime esta configuración para que el usuario entienda las condiciones del escenario.

2.  **Fase 1: Distribución (Dealer):**
    -   Crea una instancia de `VSSDealer` con los parámetros definidos.
    -   Llama a `dealer.distribute_secret()`, lo que genera el polinomio, el `commitment`, los `shares`, las pruebas (`witnesses`) y guarda todo en `dealer_output.json`.

3.  **Fase 2: Reconstrucción (Client):**
    -   Crea una instancia de `VSSClient`.
    -   Llama a `client.load_dealer_output()` para cargar los datos generados por el dealer.

4.  **Pruebas de Reconstrucción:**
    -   El script simula varios intentos de reconstrucción para demostrar cómo funciona el umbral y la verificación:
        -   **Combinación 1 y 2:** Utiliza dos conjuntos diferentes de `T+1` shares. En ambos casos, el cliente verifica los shares, confirma que son suficientes y reconstruye el secreto con éxito.
        -   **Combinación 3:** Intenta reconstruir el secreto con solo `T` shares. El script muestra que la reconstrucción falla porque no se alcanza el umbral necesario de `T+1`.
        -   **Combinación 4 (Completa):** Llama al método `run_reconstruction()` del cliente sin especificar shares, lo que hace que el cliente intente usar todos los shares disponibles y válidos para la reconstrucción.

5.  **Resumen Final:**
    -   Imprime un resumen de los resultados, indicando el secreto original, el modo KZG utilizado ("REAL" o "SIMULADO") y si las combinaciones de reconstrucción tuvieron éxito.

## Cómo Ejecutar la Demo

Para ejecutar la demostración, simplemente corra el script desde la línea de comandos:

```bash
python demo.py
```

La salida mostrará paso a paso el proceso de distribución, verificación y los resultados de cada intento de reconstrucción, permitiendo una fácil comprensión del funcionamiento del sistema VSS implementado.
