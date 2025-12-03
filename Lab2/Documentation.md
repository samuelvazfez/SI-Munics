# Documentación del Proyecto VSS con KZG

Este proyecto es una implementación del esquema de **Verifiable Secret Sharing (VSS)** basado en el protocolo de Shamir, con la adición de compromisos criptográficos **KZG (Kate-Zaverucha-Goldberg)** para la verificabilidad de los *shares*.

El sistema permite a un *dealer* distribuir un secreto entre *n* participantes de tal manera que solo un subconjunto de ellos (un umbral *t+1*) pueda reconstruirlo. Gracias a KZG, cada participante puede verificar que su *share* es correcto y pertenece al polinomio original sin necesidad de confiar en otros.

## Arquitectura del Proyecto

El proyecto está estructurado en varios módulos de Python, cada uno con una responsabilidad clara:

-   **`vss_common.py`**: Contiene la lógica matemática fundamental para el esquema de Shamir.
-   **`trusted_setup.py`**: Gestiona la configuración de confianza para los compromisos KZG.
-   **`dealer.py`**: Implementa la entidad que distribuye el secreto.
-   **`client.py`**: Implementa la entidad que recibe un *share* y participa en la reconstrucción del secreto.
-   **`demo.py`**: Un script de demostración que ejecuta el flujo completo del protocolo.

## Documentación Detallada por Módulo

A continuación se encuentran los enlaces a la documentación detallada para cada componente del sistema:

-   [**`TrustedSetup.md`**](./TrustedSetup.md): Explicación sobre cómo se carga y gestiona la configuración de confianza para KZG y las funciones de simulación.
-   [**`VSSCommon.md`**](./VSSCommon.md): Descripción de las operaciones matemáticas básicas como la generación de polinomios y la interpolación de Lagrange.
-   [**`Dealer.md`**](./Dealer.md): Detalla el proceso de distribución del secreto, incluyendo la generación de *shares* y pruebas KZG.
-   [**`Client.md`**](./Client.md): Explica cómo un cliente verifica su *share* y participa en la reconstrucción del secreto.
-   [**`Demo.md`**](./Demo.md): Describe el flujo de la demostración completa y cómo interpretar sus resultados.

## Flujo General del Protocolo

1.  **Inicialización**: El `dealer` define un secreto, el número de participantes (`n`) y el umbral (`t`).
2.  **Distribución**:
    -   El `dealer` genera un polinomio aleatorio de grado `t` donde el término independiente es el secreto.
    -   Calcula un compromiso KZG del polinomio y lo hace público.
    -   Para cada participante, calcula un *share* (un punto en el polinomio) y una prueba KZG (*witness*).
    -   Toda esta información se publica (en este caso, en el archivo `dealer_output.json`).
3.  **Verificación y Reconstrucción**:
    -   Un `cliente` (o un grupo de ellos) carga la información pública del `dealer`.
    -   Cada cliente puede verificar de forma independiente la validez de su *share* utilizando la prueba KZG y el compromiso público.
    -   Un grupo de al menos `t+1` clientes puede juntar sus *shares* válidos para reconstruir el secreto mediante interpolación de Lagrange.
