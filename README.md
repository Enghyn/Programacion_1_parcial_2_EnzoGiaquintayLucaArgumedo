# Sistema de Gestión de Supermercado

Este proyecto implementa un sistema de gestión de productos para supermercado, permitiendo administrar diferentes categorías de productos a través de una estructura jerárquica de archivos CSV.

## Autores
- Enzo Giaquinta
- Luca Argumedo

## Información Académica
- **Universidad:** Universidad Tecnológica Nacional (UTN)
- **Carrera:** Tecnicatura Universitaria en Programación
- **Comisión:** 4 - 1 prog 4
- **Profesor:** Ramiro Hualpa

## Estructura del Proyecto

El proyecto está organizado en una estructura jerárquica de carpetas que representa las diferentes categorías y subcategorías de productos:

```
Supermercado/
├── Alimentos/
│   ├── Lácteos/
│   │   ├── Descremados/
│   │   │   └── Productos.csv
│   │   └── Enteros/
│   │       └── Productos.csv
│   └── Cereales/
│       ├── Avena/
│       │   └── Productos.csv
│       └── Maiz/
│           └── Productos.csv
└── Bebidas/
    ├── Gaseosas/
    │   ├── Regular/
    │   │   └── Productos.csv
    │   └── Zero/
    │       └── Productos.csv
    └── Jugos/
        ├── Artificiales/
        │   └── Productos.csv
        └── Naturales/
            └── Productos.csv
```

## Funcionalidades

El sistema ofrece las siguientes funcionalidades principales:

1. **Alta de Item:** Permite agregar nuevos productos en cualquier categoría.
2. **Mostrar Items:** 
   - Visualiza todos los productos de una categoría seleccionada
   - Permite filtrar productos por nombre
3. **Modificar Item:** Permite editar la información de productos existentes.
4. **Eliminar Item:** Permite eliminar productos del sistema.
5. **Ordenar Productos:** Ordena los productos por:
   - Precio (ascendente/descendente)
   - Stock (ascendente/descendente)
6. **Promedio de Productos:** Calcula promedios de:
   - Precio y stock por categoría
   - Precio y stock global de todos los productos

## Estructura de Datos

Cada producto se almacena en archivos CSV con los siguientes campos:
- **ID:** Identificador único del producto
- **Nombre:** Nombre del producto
- **Precio:** Precio del producto
- **Stock:** Cantidad disponible del producto

## Cómo Usar el Sistema

1. Ejecute el archivo `main.py`
2. Se mostrará un menú con las siguientes opciones:
   ```
   === SISTEMA DE GESTIÓN DE SUPERMERCADO ===
   1. Alta de item
   2. Mostrar todos los items
   3. Mostrar items (filtrado)
   4. Modificar item
   5. Eliminar item
   6. Ordenar productos
   7. Promedio de productos
   8. Salir
   ```
3. Seleccione la opción deseada ingresando el número correspondiente
4. Siga las instrucciones en pantalla para navegar por las categorías y realizar operaciones

## Características Técnicas

- **Validación de Datos:** El sistema incluye validación robusta para todos los inputs del usuario
- **Manejo de Errores:** Gestión de errores para operaciones de archivo y entrada de datos
- **Estructura Jerárquica:** Sistema de navegación intuitivo por categorías y subcategorías
- **Persistencia de Datos:** Almacenamiento en archivos CSV para mantener la información entre sesiones

## Requisitos

- Python 3.x
- No se requieren bibliotecas externas adicionales

## Enlaces

- https://youtu.be/iwx1cqUalLM

## Notas Adicionales

- El sistema verifica y crea automáticamente la estructura de carpetas si no existe
- Los archivos CSV son validados al inicio para asegurar la integridad de los datos
- Se mantiene una numeración consecutiva de IDs al eliminar productos
