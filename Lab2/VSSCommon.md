# Documentación de `vss_common.py`

El módulo `vss_common.py` define una clase `VSSCommon` que encapsula la lógica matemática fundamental para el esquema de **Verifiable Secret Sharing (VSS)** de Shamir. Proporciona las herramientas necesarias para la generación de polinomios, su evaluación y la reconstrucción del secreto mediante interpolación de Lagrange.

## Clase `VSSCommon`

Esta clase contiene las operaciones matemáticas que se realizan sobre un cuerpo finito, definido por el primo `field_prime`.

### Atributos

- **`field_prime`**: Un número primo grande que define el cuerpo finito sobre el cual se realizan todas las operaciones aritméticas. El valor es `0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001`.

### Métodos

#### `generate_polynomial(secret: int, degree: int) -> List[int]`

- **Propósito:** Generar un polinomio aleatorio de un grado específico, donde el término independiente es el secreto.
- **Parámetros:**
    - `secret`: El valor del secreto a compartir.
    - `degree`: El grado del polinomio (que corresponde a `t` en el esquema de Shamir).
- **Comportamiento:**
    1. El coeficiente de grado 0 (término independiente) se establece como `secret`.
    2. Los coeficientes restantes (hasta el grado `degree`) se generan de forma aleatoria y se reducen módulo `field_prime`.
- **Retorno:** Una lista de los coeficientes del polinomio.

#### `evaluate_polynomial(coefficients: List[int], x: int) -> int`

- **Propósito:** Evaluar el polinomio en un punto `x` específico.
- **Parámetros:**
    - `coefficients`: La lista de coeficientes del polinomio.
    - `x`: El punto en el que se evaluará el polinomio.
- **Comportamiento:** Utiliza el método de Horner para evaluar eficientemente el polinomio. Todas las operaciones se realizan módulo `field_prime`.
- **Retorno:** El resultado de la evaluación, `P(x)`.

#### `lagrange_interpolation(points: List[Tuple[int, int]], x: int = 0) -> int`

- **Propósito:** Reconstruir el valor del polinomio en un punto `x` (por defecto, `x=0` para obtener el secreto) a partir de un conjunto de puntos.
- **Parámetros:**
    - `points`: Una lista de tuplas `(xi, yi)`, donde cada tupla es un punto del polinomio.
    - `x`: El punto en el que se desea reconstruir el valor del polinomio. El valor por defecto es `0`, que corresponde al término independiente (el secreto).
- **Comportamiento:** Implementa el algoritmo de interpolación de Lagrange.
- **Retorno:** El valor reconstruido del polinomio en `x`.

#### `polynomial_to_blob(coefficients: List[int]) -> bytes`

- **Propósito:** Convertir los coeficientes de un polinomio en un formato de `blob` (objeto binario grande) compatible con `ckzg`.
- **Parámetros:**
    - `coefficients`: La lista de coeficientes del polinomio.
- **Comportamiento:**
    1. Crea una lista de 4096 elementos inicializada en cero.
    2. Rellena esta lista con los coeficientes del polinomio.
    3. Convierte cada elemento a una representación de 32 bytes en formato `little-endian` y los concatena.
- **Retorno:** Un `blob` de bytes que representa el polinomio.
