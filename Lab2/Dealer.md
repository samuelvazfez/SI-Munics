# Documentación de `dealer.py`

El módulo `dealer.py` define la clase `VSSDealer`, que actúa como la entidad central en el esquema de Verifiable Secret Sharing (VSS). El "dealer" es responsable de tomar un secreto, generar un polinomio y distribuir "shares" (participaciones) a varios participantes de una manera que sea verificable.

## Clase `VSSDealer`

Esta clase orquesta el proceso de distribución del secreto, interactuando con `vss_common.py` para las operaciones matemáticas y `trusted_setup.py` para la funcionalidad criptográfica de KZG.

### Atributos

- **`n`**: El número total de participantes.
- **`t`**: El grado del polinomio, que define el umbral (`t+1`) de participantes necesarios para reconstruir el secreto.
- **`secret`**: El valor que se va a compartir.
- **`common`**: Una instancia de `VSSCommon` para acceder a las funciones matemáticas.
- **`ckzg_ready`**: Un booleano que indica si la librería `ckzg` fue configurada correctamente.
- **`trusted_setup`**: El objeto de configuración de confianza cargado desde `trusted_setup.py`.
- **`polynomial_coeffs`**: Los coeficientes del polinomio generado.
- **`commitment`**: El compromiso criptográfico del polinomio.

### `__init__(self, n: int, t: int, secret: int)`

- **Propósito:** Inicializar el dealer.
- **Parámetros:**
    - `n`: Número total de participantes.
    - `t`: Grado del polinomio (umbral). Se restringe a un máximo de 4.
    - `secret`: El secreto a compartir.
- **Comportamiento:**
    - Configura los parámetros `n`, `t` y `secret`.
    - Llama a `setup_ckzg()` para intentar inicializar la configuración de confianza de KZG.

### `distribute_secret(self)`

- **Propósito:** Orquestar todo el proceso de distribución del secreto.
- **Comportamiento:**
    1. **Generación del Polinomio:** Llama a `self.common.generate_polynomial()` para crear un polinomio de grado `t` con el secreto como término independiente.
    2. **Creación del Compromiso (Commitment):**
        - Intenta usar `ckzg.blob_to_kzg_commitment()` para generar un compromiso real a partir de un `blob` (en este caso, un blob de ceros).
        - Si la librería `ckzg` no está disponible o falla, recurre a `blob_to_kzg_commitment_sim()` para generar un compromiso simulado.
    3. **Generación de Shares y Pruebas (Witnesses):**
        - Itera desde `i = 1` hasta `n` para cada participante.
        - Calcula el "share" evaluando el polinomio en el punto `i`.
        - Genera una prueba criptográfica (witness) para cada share. Intenta usar `ckzg.compute_kzg_proof()` si está en modo "REAL"; de lo contrario, usa la simulación `compute_kzg_proof_sim()`.
    4. **Almacenamiento del Resultado:**
        - Guarda toda la información relevante (parámetros, compromiso, polinomio y los shares con sus pruebas) en un archivo `dealer_output.json`.
        - Este archivo es la salida pública del dealer, que será consumida por los clientes.
- **Retorno:** Un diccionario con toda la información generada.

## Flujo de Ejecución

1. El dealer se inicializa con el secreto y los parámetros `n` y `t`.
2. Se genera un polinomio aleatorio que "oculta" el secreto.
3. Se crea un compromiso con este polinomio, que actúa como una "promesa" inmutable sobre el polinomio sin revelarlo.
4. Para cada participante, se calcula un punto del polinomio (el "share") y una prueba que demuestra que ese share pertenece al polinomio comprometido.
5. Toda esta información se empaqueta y se guarda en `dealer_output.json` para que los clientes puedan acceder a ella.
