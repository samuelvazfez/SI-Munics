# Documentación de `client.py`

El módulo `client.py` define la clase `VSSClient`, que representa a un participante en el esquema de Verifiable Secret Sharing (VSS). El cliente es responsable de cargar la información generada por el `VSSDealer`, verificar la validez de los "shares" (participaciones) que recibe y, finalmente, reconstruir el secreto si tiene suficientes shares válidos.

## Clase `VSSClient`

Esta clase implementa el lado del receptor en el esquema VSS, asegurando que solo los shares válidos se utilicen para la reconstrucción del secreto.

### Atributos

- **`common`**: Una instancia de `VSSCommon` para acceder a las funciones matemáticas, como la interpolación de Lagrange.
- **`received_shares`**: Un diccionario para almacenar los shares que ha recibido (aunque no se utiliza activamente en la implementación actual, está preparado para un escenario más complejo).
- **`ckzg_ready`**: Un booleano que indica si la librería `ckzg` fue configurada correctamente para la verificación.
- **`trusted_setup`**: El objeto de configuración de confianza cargado.
- **`data`**: El contenido deserializado del archivo `dealer_output.json`.
- **`n`, `t`, `original_secret`**: Parámetros del esquema VSS leídos desde `dealer_output.json`.
- **`commitment`**: El compromiso criptográfico del polinomio, leído desde el `dealer_output.json`.
- **`kzg_mode`**: El modo en que se generaron los shares ("REAL" o "SIMULADO").

### Métodos

#### `load_dealer_output(self, filename="dealer_output.json")`

- **Propósito:** Cargar y procesar la información pública generada por el `VSSDealer`.
- **Parámetros:**
    - `filename`: El nombre del archivo JSON a cargar.
- **Comportamiento:**
    - Abre y lee el archivo `dealer_output.json`.
    - Extrae y almacena los parámetros (`n`, `t`), el secreto original (para comparación), el `commitment` y el modo KZG.

#### `verify_share(self, share_data)`

- **Propósito:** Verificar si un "share" es válido utilizando su prueba (witness) y el compromiso público.
- **Parámetros:**
    - `share_data`: Un diccionario que contiene el share, el witness y el commitment asociado.
- **Comportamiento:**
    1. Extrae el `commitment`, `x`, `share` (y) y la `proof` (witness) del `share_data`.
    2. Si el modo es "REAL" y `ckzg` está listo, intenta verificar la prueba usando `ckzg.verify_kzg_proof()`.
    3. Si el modo es "SIMULADO" o la verificación real falla, utiliza `verify_kzg_proof_sim()`, que siempre devuelve `True`.
- **Retorno:** `True` si el share es válido, `False` en caso contrario.

#### `collect_shares(self, share_indices=None)`

- **Propósito:** Recolectar y verificar un conjunto de shares.
- **Parámetros:**
    - `share_indices`: Una lista de los índices de los shares que se intentarán recolectar y verificar.
- **Comportamiento:**
    - Itera sobre los índices de los shares especificados.
    - Para cada share, llama a `verify_share()`.
    - Si el share es válido, lo añade a una lista de `valid_shares`.
- **Retorno:** Una lista de tuplas `(x, share)` que representan los shares válidos.

#### `reconstruct_secret(self, shares)`

- **Propósito:** Reconstruir el secreto a partir de un conjunto de shares válidos.
- **Parámetros:**
    - `shares`: Una lista de shares válidos (tuplas `(x, share)`).
- **Comportamiento:**
    1. Comprueba si el número de shares es suficiente (al menos `t+1`).
    2. Si es así, llama a `self.common.lagrange_interpolation()` para reconstruir el secreto (evaluando el polinomio en `x=0`).
- **Retorno:** El secreto reconstruido o `None` si no hay suficientes shares.

#### `run_reconstruction(self, share_indices=None)`

- **Propósito:** Orquestar el proceso completo de recolección, verificación y reconstrucción.
- **Comportamiento:**
    1. Llama a `collect_shares()` para obtener los shares válidos.
    2. Imprime un resumen de cuántos shares válidos se encontraron y cuántos son necesarios.
    3. Si hay suficientes shares, llama a `reconstruct_secret()` y compara el resultado con el secreto original.
- **Retorno:** El secreto reconstruido o `None`.
