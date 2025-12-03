# Documentación de `trusted_setup.py`

El módulo `trusted_setup.py` es responsable de gestionar la configuración de confianza necesaria para las operaciones criptográficas con la librería `ckzg`. También proporciona funciones de simulación para KZG cuando la configuración real no está disponible.

## Funcionalidad Principal

- **Carga de la Configuración de Confianza:** Intenta cargar un archivo `trusted_setup.txt` que contiene los parámetros precalculados para `ckzg`.
- **Funciones de Simulación:** Ofrece un conjunto de funciones que simulan la creación y verificación de compromisos y pruebas KZG utilizando `hashlib.sha256`. Esto permite que el sistema funcione incluso si la configuración de `ckzg` falla.
- **Gestión de Estado Global:** Utiliza variables globales para mantener el estado de la configuración de `ckzg` y evitar cargas repetidas.

## Funciones

### `setup_ckzg()`

Esta función inicializa la configuración de `ckzg`.

- **Comportamiento:**
    1. Verifica si la configuración ya ha sido cargada para evitar reinicializaciones.
    2. Comprueba si el archivo `trusted_setup.txt` existe.
    3. Si existe, llama a `ckzg.load_trusted_setup` para cargar los parámetros.
    4. Si tiene éxito, marca la configuración como cargada.
- **Retorno:**
    - `True`: Si la configuración se carga correctamente o ya estaba cargada.
    - `False`: Si ocurre un error (ej. el archivo no se encuentra).

### `get_trusted_setup()`

- **Comportamiento:** Devuelve el objeto de configuración de confianza que fue cargado.
- **Retorno:**
    - El objeto `_trusted_setup` o `None` si no ha sido cargado.

### Funciones de Simulación

Estas funciones proporcionan una alternativa cuando no se puede usar `ckzg`.

- **`blob_to_kzg_commitment_sim(blob)`:**
    - Simula la creación de un compromiso KZG calculando el hash SHA256 del `blob`.
    - **Retorno:** Un hash de 48 bytes.

- **`compute_kzg_proof_sim(blob, z)`:**
    - Simula el cálculo de una prueba KZG calculando el hash SHA256 de la concatenación del `blob` y un valor `z`.
    - **Retorno:** Un hash de 48 bytes.

- **`verify_kzg_proof_sim(commitment, z, y, proof)`:**
    - Simula la verificación de una prueba KZG.
    - **Comportamiento:** Siempre devuelve `True`, lo que significa que la verificación simulada nunca falla.
    - **Retorno:** `True`.
