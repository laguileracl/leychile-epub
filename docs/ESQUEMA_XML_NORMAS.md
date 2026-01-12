# 📋 Esquema Estándar XML para Normas Legales Chilenas

Este documento define el esquema estándar que deben seguir los archivos XML de normas legales chilenas (leyes, decretos, códigos, DFL, DL, etc.) para permitir:

1. **Parseo automático** de texto plano a XML estructurado
2. **Validación** de documentos XML
3. **Interoperabilidad** entre sistemas
4. **Generación de ePub** y otros formatos

---

## 📑 Índice

1. [Estructura General](#estructura-general)
2. [Elemento Raíz: `<ley>`](#elemento-raíz-ley)
3. [Metadatos: `<metadatos>`](#metadatos-metadatos)
4. [Encabezado: `<encabezado>`](#encabezado-encabezado)
5. [Contenido: `<contenido>`](#contenido-contenido)
6. [Jerarquía de Divisiones](#jerarquía-de-divisiones)
7. [Artículos y Sub-elementos](#artículos-y-sub-elementos)
8. [Patrones de Reconocimiento de Texto](#patrones-de-reconocimiento-de-texto)
9. [Ejemplos Completos](#ejemplos-completos)
10. [Algoritmo de Conversión](#algoritmo-de-conversión)

---

## Estructura General

```xml
<?xml version="1.0" encoding="utf-8"?>
<ley xmlns="https://leychile.cl/schema/ley/v1"
     version="1.0"
     idioma="es-CL"
     id_norma="[ID]"
     tipo="[TIPO_NORMA]"
     numero="[NUMERO]"
     estado="vigente|derogada|parcial"
     fecha_version="YYYY-MM-DD"
     fecha_promulgacion="YYYY-MM-DD"
     fecha_publicacion="YYYY-MM-DD"
     generado="[TIMESTAMP_ISO]"
     fuente="[FUENTE]"
     url_original="[URL]">
  
  <metadatos>...</metadatos>
  <encabezado>...</encabezado>
  <contenido>...</contenido>
  
</ley>
```

---

## Elemento Raíz: `<ley>`

### Atributos Obligatorios

| Atributo | Tipo | Descripción | Ejemplo |
|----------|------|-------------|---------|
| `xmlns` | URI | Namespace del esquema | `https://leychile.cl/schema/ley/v1` |
| `version` | String | Versión del esquema XML | `1.0` |
| `idioma` | Locale | Código de idioma | `es-CL` |
| `id_norma` | Integer | ID único BCN | `242302` |
| `tipo` | Enum | Tipo de norma | Ver tabla de tipos |
| `numero` | String | Número de la norma | `100`, `19496`, `PENAL` |
| `estado` | Enum | Estado de vigencia | `vigente`, `derogada`, `parcial` |

### Atributos Opcionales

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `fecha_version` | Date | Fecha de la versión del texto |
| `fecha_promulgacion` | Date | Fecha de promulgación |
| `fecha_publicacion` | Date | Fecha de publicación |
| `generado` | DateTime | Timestamp de generación |
| `fuente` | String | Fuente del documento |
| `url_original` | URL | URL original de BCN |

### Tipos de Norma Válidos

| Valor | Descripción |
|-------|-------------|
| `Ley` | Ley ordinaria |
| `Decreto` | Decreto supremo |
| `Decreto Ley` | Decreto ley (DL) |
| `Decreto con Fuerza de Ley` | DFL |
| `Código` | Código (Civil, Penal, etc.) |
| `Reglamento` | Reglamento |
| `Resolución` | Resolución administrativa |
| `Auto Acordado` | Auto acordado judicial |
| `Tratado Internacional` | Tratado o convención |

---

## Metadatos: `<metadatos>`

```xml
<metadatos>
  <titulo>[TÍTULO OFICIAL COMPLETO]</titulo>
  
  <identificacion>
    <tipo>[TIPO_NORMA]</tipo>
    <numero>[NUMERO]</numero>
  </identificacion>
  
  <organismos>
    <organismo>[MINISTERIO/ORGANISMO]</organismo>
    <!-- Puede haber múltiples organismos -->
  </organismos>
  
  <materias>
    <materia>[TEMA 1]</materia>
    <materia>[TEMA 2]</materia>
    <!-- Materias/temas de la norma -->
  </materias>
  
  <nombres_comunes>
    <nombre>[NOMBRE COMÚN 1]</nombre>
    <!-- Ej: "LEY DICOM", "CÓDIGO CIVIL" -->
  </nombres_comunes>
  
  <fechas>
    <promulgacion>YYYY-MM-DD</promulgacion>
    <publicacion>YYYY-MM-DD</publicacion>
    <version>YYYY-MM-DD</version>
  </fechas>
  
  <fuente>[Diario Oficial | Boletín de Leyes...]</fuente>
</metadatos>
```

---

## Encabezado: `<encabezado>`

Contiene el texto preambular de la norma antes del articulado:

```xml
<encabezado>ESTABLECE NORMAS SOBRE PROTECCION DE LOS DERECHOS DE LOS
CONSUMIDORES

 Teniendo presente que el H. Congreso Nacional ha dado
su aprobación al siguiente

P r o y e c t o d e l e y:</encabezado>
```

### Contenido Típico del Encabezado
- Título de la norma
- Fórmula promulgatoria ("Teniendo presente que el H. Congreso Nacional...")
- Vistos y considerandos
- Decreto inicial

---

## Contenido: `<contenido>`

### Atributos Informativos

```xml
<contenido total_articulos="148" 
           total_libros="0" 
           total_titulos="7" 
           total_capitulos="0">
  <!-- Estructura jerárquica -->
</contenido>
```

---

## Jerarquía de Divisiones

Las normas chilenas siguen una **jerarquía de divisiones** de mayor a menor:

```
LIBRO → TÍTULO → CAPÍTULO → PÁRRAFO → SECCIÓN → ARTÍCULO
```

### Orden de Anidamiento

1. **Libro** (opcional) - Para códigos extensos
2. **Título** (común) - División principal
3. **Capítulo** (común) - Subdivisión de títulos
4. **Párrafo** (frecuente) - Subdivisión de capítulos
5. **Sección/Enumeración** (variable) - Subdivisiones menores (§)
6. **Artículo** (fundamental) - Unidad básica

### Elemento: `<libro>`

```xml
<libro id="[ID_UNICO]" tipo_original="Libro" fecha_modificacion="YYYY-MM-DD">
  <titulo_seccion>LIBRO PRIMERO DE LOS COMERCIANTES...</titulo_seccion>
  <texto>Libro I DE LOS COMERCIANTES Y DE LOS AGENTES DEL COMERCIO</texto>
  
  <!-- Contiene títulos, capítulos, artículos -->
</libro>
```

### Elemento: `<titulo>`

```xml
<titulo id="[ID_UNICO]" tipo_original="Título" fecha_modificacion="YYYY-MM-DD">
  <titulo_seccion>TITULO I NORMAS GENERALES</titulo_seccion>
  <contexto>Libro I DE LOS COMERCIANTES...</contexto>
  <texto>TITULO I NORMAS GENERALES</texto>
  
  <!-- Contiene párrafos, capítulos, artículos -->
</titulo>
```

### Elemento: `<capitulo>`

```xml
<capitulo id="[ID_UNICO]" tipo_original="Capítulo" fecha_modificacion="YYYY-MM-DD">
  <titulo_seccion>Capítulo I BASES DE LA INSTITUCIONALIDAD</titulo_seccion>
  <contexto><!-- Jerarquía padre --></contexto>
  <texto>Capítulo I BASES DE LA INSTITUCIONALIDAD</texto>
  
  <!-- Contiene párrafos, secciones, artículos -->
</capitulo>
```

### Elemento: `<parrafo>`

```xml
<parrafo id="[ID_UNICO]" tipo_original="Párrafo" fecha_modificacion="YYYY-MM-DD">
  <titulo_seccion>Párrafo 1º Los derechos y deberes del consumidor</titulo_seccion>
  <contexto>T I T U L O II Disposiciones generales</contexto>
  <texto>Párrafo 1º Los derechos y deberes del consumidor</texto>
  
  <!-- Contiene artículos -->
</parrafo>
```

### Elemento: `<seccion>` (Enumeración §)

```xml
<seccion id="[ID_UNICO]" tipo_original="Enumeración" fecha_modificacion="YYYY-MM-DD">
  <titulo_seccion>§ 1. De la ley</titulo_seccion>
  <contexto>TITULO PRELIMINAR</contexto>
  <texto>§ 1. De la ley</texto>
  
  <!-- Contiene artículos -->
</seccion>
```

---

## Artículos y Sub-elementos

### Elemento: `<articulo>`

```xml
<articulo id="[ID_UNICO]" 
          tipo_original="Artículo" 
          numero="[NUMERO]" 
          fecha_modificacion="YYYY-MM-DD">
  
  <contexto>[JERARQUÍA COMPLETA DE PADRES]</contexto>
  
  <!-- OPCIÓN 1: Texto simple -->
  <texto>Artículo 1º.- La presente ley tiene por objeto...</texto>
  
  <!-- OPCIÓN 2: Contenido estructurado -->
  <contenido>
    <parrafo>Artículo 3º.- Son derechos y deberes básicos del consumidor:</parrafo>
    <parrafo>a) La libre elección del bien o servicio...</parrafo>
    <parrafo>b) El derecho a una información veraz...</parrafo>
    <inciso numero="1">Texto del inciso 1...</inciso>
    <inciso numero="2">Texto del inciso 2...</inciso>
  </contenido>
  
  <referencias>
    <ref articulo="[NUM_REFERENCIADO]"/>
  </referencias>
</articulo>
```

### Numeración de Artículos

| Formato Original | Valor `numero` |
|------------------|----------------|
| `Artículo 1º` | `1` |
| `Artículo 2°` | `2` |
| `Art. 10` | `10` |
| `ARTÍCULO 100` | `100` |
| `Artículo 3 bis` | `3 BIS` |
| `Artículo 3 ter` | `3 TER` |
| `Artículo 1 (DEL ART. 2)` | `1 (DEL ART. 2)` |

### Sub-elementos del Contenido

#### `<parrafo>` - Párrafo interno

```xml
<parrafo>Texto del párrafo sin numeración especial.</parrafo>
```

#### `<inciso>` - Inciso numerado

```xml
<inciso numero="1">Texto del primer inciso...</inciso>
<inciso numero="2">Texto del segundo inciso...</inciso>
```

#### Letras (dentro del texto o párrafos)

Las letras (a, b, c...) generalmente se incluyen como parte del texto del párrafo:

```xml
<parrafo>a) La libre elección del bien o servicio.</parrafo>
<parrafo>b) El derecho a una información veraz...</parrafo>
```

#### Numerales (1°, 2°, etc.)

Los numerales también van como parte del texto:

```xml
<parrafo>1°) Por "venta", toda convención independiente...</parrafo>
<parrafo>2°) Por "servicio", la acción o prestación...</parrafo>
```

---

## Patrones de Reconocimiento de Texto

### Divisiones Mayores

| Patrón Regex | Tipo | Ejemplo |
|--------------|------|---------|
| `^LIBRO\s+(PRIMERO\|SEGUNDO\|[IVXLC]+\|[0-9]+)` | Libro | `LIBRO PRIMERO`, `LIBRO I` |
| `^T[ÍI]TULO\s+(PRELIMINAR\|[IVXLC]+\|[0-9]+)` | Título | `TÍTULO I`, `TITULO PRELIMINAR` |
| `^CAP[ÍI]TULO\s+([IVXLC]+\|[0-9]+)` | Capítulo | `CAPÍTULO I`, `Capítulo 1` |
| `^P[ÁA]RRAFO\s+([0-9]+[º°]?\|[IVXLC]+)` | Párrafo | `PÁRRAFO 1º`, `Párrafo 2°` |
| `^§\s*[0-9]+\.?` | Sección | `§ 1. De la ley` |

### Artículos

```regex
^(ART[ÍI]CULO|Art\.?)\s*([0-9]+)\s*(BIS|TER|QUATER|QUINQUIES|SEXIES|SEPTIES|OCTIES|NOVIES|DECIES)?[º°]?\.?\s*[-–—]?
```

**Ejemplos reconocidos:**
- `Artículo 1º.-`
- `Art. 2°.-`
- `ARTÍCULO 100.-`
- `Artículo 3 bis.-`
- `Art. 4 ter.`

### Incisos

```regex
^([0-9]+)[°º]?\)?\.?\s+
```

**Ejemplos:**
- `1) Texto...`
- `2°) Texto...`
- `1. Texto...`
- `1° Texto...`

### Letras

```regex
^([a-z])\)\s+
```

**Ejemplos:**
- `a) Texto...`
- `b) Texto...`
- `ñ) Texto...`

### Numerales Romanos

```regex
^([IVXLC]+)[.)\s]
```

**Ejemplos:**
- `I. Texto...`
- `II) Texto...`

---

## Ejemplos Completos

### Ejemplo 1: Ley Simple

```xml
<?xml version="1.0" encoding="utf-8"?>
<ley xmlns="https://leychile.cl/schema/ley/v1" version="1.0" idioma="es-CL" 
     id_norma="19628" tipo="Ley" numero="19628" estado="vigente"
     fecha_promulgacion="1999-08-18" fecha_publicacion="1999-08-28">
  
  <metadatos>
    <titulo>SOBRE PROTECCION DE LA VIDA PRIVADA</titulo>
    <identificacion>
      <tipo>Ley</tipo>
      <numero>19628</numero>
    </identificacion>
    <organismos>
      <organismo>MINISTERIO SECRETARÍA GENERAL DE LA PRESIDENCIA</organismo>
    </organismos>
    <materias>
      <materia>Derecho a la Privacidad</materia>
    </materias>
    <nombres_comunes>
      <nombre>LEY DICOM</nombre>
    </nombres_comunes>
    <fechas>
      <promulgacion>1999-08-18</promulgacion>
      <publicacion>1999-08-28</publicacion>
    </fechas>
    <fuente>Diario Oficial</fuente>
  </metadatos>
  
  <encabezado>SOBRE PROTECCION DE LA VIDA PRIVADA

 Teniendo presente que el H. Congreso Nacional ha dado
su aprobación al siguiente

 P r o y e c t o d e l e y:</encabezado>
  
  <contenido total_articulos="27" total_titulos="7">
    <titulo id="t1" tipo_original="Título" fecha_modificacion="1999-08-28">
      <titulo_seccion>Título Preliminar Disposiciones generales</titulo_seccion>
      <texto>Título Preliminar Disposiciones generales</texto>
      
      <articulo id="a1" tipo_original="Artículo" numero="1" fecha_modificacion="1999-08-28">
        <contexto>Título Preliminar Disposiciones generales</contexto>
        <texto>Artículo 1º.- El tratamiento de los datos de
carácter personal en registros o bancos de datos por
organismos públicos o por particulares se sujetará a las
disposiciones de esta ley...</texto>
        <referencias>
          <ref articulo="1"/>
        </referencias>
      </articulo>
      
      <articulo id="a2" tipo_original="Artículo" numero="2" fecha_modificacion="1999-08-28">
        <contexto>Título Preliminar Disposiciones generales</contexto>
        <texto>Artículo 2°.- Para los efectos de esta ley se
entenderá por:
 a) Almacenamiento de datos, la conservación o custodia
de datos en un registro o banco de datos.
 b) Bloqueo de datos, la suspensión temporal de
cualquier operación de tratamiento...</texto>
        <referencias>
          <ref articulo="2"/>
        </referencias>
      </articulo>
    </titulo>
  </contenido>
</ley>
```

### Ejemplo 2: Código con Libros

```xml
<?xml version="1.0" encoding="utf-8"?>
<ley xmlns="https://leychile.cl/schema/ley/v1" version="1.0" idioma="es-CL"
     id_norma="1984" tipo="Código" numero="PENAL" estado="vigente"
     fecha_promulgacion="1874-11-12" fecha_publicacion="1874-11-12">
  
  <metadatos>
    <titulo>CÓDIGO PENAL</titulo>
    <identificacion>
      <tipo>Código</tipo>
      <numero>PENAL</numero>
    </identificacion>
    <organismos>
      <organismo>MINISTERIO DE JUSTICIA</organismo>
    </organismos>
    <fechas>
      <promulgacion>1874-11-12</promulgacion>
      <publicacion>1874-11-12</publicacion>
    </fechas>
  </metadatos>
  
  <encabezado>CÓDIGO PENAL...</encabezado>
  
  <contenido total_articulos="677" total_libros="3" total_titulos="18">
    <libro id="l1" tipo_original="Libro" fecha_modificacion="1927-10-12">
      <titulo_seccion>LIBRO PRIMERO</titulo_seccion>
      <texto>LIBRO PRIMERO</texto>
      
      <titulo id="t1" tipo_original="Título" fecha_modificacion="1927-10-12">
        <titulo_seccion>TÍTULO PRIMERO DE LOS DELITOS...</titulo_seccion>
        <contexto>LIBRO PRIMERO</contexto>
        <texto>TÍTULO PRIMERO DE LOS DELITOS...</texto>
        
        <parrafo id="p1" tipo_original="Párrafo" fecha_modificacion="1927-10-12">
          <titulo_seccion>§ I. De los delitos.</titulo_seccion>
          <contexto>LIBRO PRIMERO &gt; TÍTULO PRIMERO</contexto>
          <texto>§ I. De los delitos.</texto>
          
          <articulo id="a1" tipo_original="Artículo" numero="1" fecha_modificacion="1927-10-12">
            <contexto>LIBRO PRIMERO &gt; TÍTULO PRIMERO &gt; § I. De los delitos.</contexto>
            <contenido>
              <parrafo>ARTÍCULO 1.</parrafo>
              <parrafo>Es delito toda acción u omisión voluntaria penada por la ley.</parrafo>
            </contenido>
          </articulo>
        </parrafo>
      </titulo>
    </libro>
  </contenido>
</ley>
```

### Ejemplo 3: Artículo con Incisos Estructurados

```xml
<articulo id="a2" tipo_original="Artículo" numero="2" fecha_modificacion="2014-03-08">
  <contexto>TÍTULO I Disposiciones generales</contexto>
  <contenido>
    <parrafo>Artículo 2º.- Para los efectos de esta ley se entenderá por:</parrafo>
    
    <inciso numero="1">Lobby: aquella gestión o actividad remunerada,
ejercida por personas naturales o jurídicas, chilenas o
extranjeras, que tiene por objeto promover, defender o
representar cualquier interés particular...</inciso>
    
    <inciso numero="2">Lobbista: La persona natural o jurídica, chilena o
extranjera, remunerada, que realiza lobby...</inciso>
  </contenido>
  <referencias>
    <ref articulo="8"/>
    <ref articulo="2"/>
  </referencias>
</articulo>
```

---

## Algoritmo de Conversión

### Paso 1: Preprocesamiento

```python
def preprocesar_texto(texto_raw: str) -> str:
    """
    1. Normalizar saltos de línea
    2. Eliminar caracteres de control
    3. Normalizar espacios múltiples
    4. Detectar y preservar estructura de columnas (si aplica)
    """
    texto = texto_raw.replace('\r\n', '\n').replace('\r', '\n')
    texto = re.sub(r'[^\S\n]+', ' ', texto)  # Espacios a uno solo
    return texto.strip()
```

### Paso 2: Extracción de Metadatos

```python
def extraer_metadatos(texto: str) -> dict:
    """
    Extraer del encabezado:
    - Tipo de norma (LEY, DECRETO, DFL, etc.)
    - Número
    - Fecha
    - Organismo
    - Título
    """
    patrones = {
        'tipo_numero': r'(LEY|DECRETO|D\.?F\.?L\.?|D\.?L\.?)\s*N[º°]?\s*(\d+[\.\d]*)',
        'fecha': r'(\d{1,2})\s+de\s+(enero|febrero|marzo|...)\s+de\s+(\d{4})',
        'ministerio': r'MINISTERIO\s+DE\s+([A-ZÁÉÍÓÚÑ\s]+)',
    }
    # ... implementación
```

### Paso 3: Identificación de Divisiones

```python
PATRONES_DIVISION = [
    (r'^LIBRO\s+(PRIMERO|SEGUNDO|TERCERO|CUARTO|[IVXLC]+)', 'libro'),
    (r'^T[ÍI]TULO\s+(PRELIMINAR|PRIMERO|[IVXLC]+|[0-9]+)', 'titulo'),
    (r'^CAP[ÍI]TULO\s+([IVXLC]+|[0-9]+)', 'capitulo'),
    (r'^P[ÁA]RRAFO\s+([0-9]+[º°]?|[IVXLC]+)', 'parrafo'),
    (r'^§\s*[0-9]+', 'seccion'),
]

def identificar_division(linea: str) -> tuple[str, str] | None:
    linea_upper = linea.strip().upper()
    for patron, tipo in PATRONES_DIVISION:
        if match := re.match(patron, linea_upper, re.IGNORECASE):
            return (tipo, match.group(0))
    return None
```

### Paso 4: Identificación de Artículos

```python
PATRON_ARTICULO = re.compile(
    r'^(ART[ÍI]CULO|Art\.?)\s*'
    r'([0-9]+)\s*'
    r'(BIS|TER|QUATER|QUINQUIES|SEXIES|SEPTIES|OCTIES|NOVIES|DECIES)?'
    r'\s*[º°]?\s*\.?\s*[-–—]?\s*',
    re.IGNORECASE | re.UNICODE
)

def identificar_articulo(linea: str) -> dict | None:
    if match := PATRON_ARTICULO.match(linea):
        numero = match.group(2)
        sufijo = match.group(3)
        if sufijo:
            numero = f"{numero} {sufijo.upper()}"
        return {
            'numero': numero,
            'texto_inicio': linea[match.end():],
        }
    return None
```

### Paso 5: Estructuración de Contenido de Artículos

```python
def estructurar_contenido_articulo(texto: str) -> dict:
    """
    Analiza el contenido del artículo y detecta:
    - Párrafos simples
    - Incisos numerados (1), 2), 1°, etc.)
    - Letras (a), b), c))
    - Numerales romanos
    """
    elementos = []
    lineas = texto.split('\n')
    
    buffer = []
    for linea in lineas:
        # Detectar inciso
        if match := re.match(r'^(\d+)[°º]?\)\s*(.+)', linea):
            if buffer:
                elementos.append({'tipo': 'parrafo', 'texto': ' '.join(buffer)})
                buffer = []
            elementos.append({'tipo': 'inciso', 'numero': match.group(1), 'texto': match.group(2)})
        # Detectar letra
        elif match := re.match(r'^([a-zñ])\)\s*(.+)', linea, re.IGNORECASE):
            if buffer:
                elementos.append({'tipo': 'parrafo', 'texto': ' '.join(buffer)})
                buffer = []
            elementos.append({'tipo': 'letra', 'letra': match.group(1), 'texto': match.group(2)})
        else:
            buffer.append(linea.strip())
    
    if buffer:
        elementos.append({'tipo': 'parrafo', 'texto': ' '.join(buffer)})
    
    return elementos
```

### Paso 6: Generación de XML

```python
def generar_xml(datos: dict) -> str:
    from xml.etree.ElementTree import Element, SubElement, tostring
    from xml.dom import minidom
    
    root = Element('ley')
    root.set('xmlns', 'https://leychile.cl/schema/ley/v1')
    root.set('version', '1.0')
    root.set('idioma', 'es-CL')
    root.set('tipo', datos['tipo'])
    root.set('numero', datos['numero'])
    root.set('estado', 'vigente')
    
    # Metadatos
    metadatos = SubElement(root, 'metadatos')
    SubElement(metadatos, 'titulo').text = datos['titulo']
    # ... más metadatos
    
    # Contenido
    contenido = SubElement(root, 'contenido')
    _construir_jerarquia(contenido, datos['estructura'])
    
    # Formatear
    xml_str = tostring(root, encoding='unicode')
    return minidom.parseString(xml_str).toprettyxml(indent="  ")
```

---

## Validación

### Reglas de Validación

1. **Estructura jerárquica válida**: Los elementos deben estar correctamente anidados
2. **IDs únicos**: Cada `id` debe ser único en el documento
3. **Números de artículo secuenciales**: Advertencia si hay saltos
4. **Contexto coherente**: El `<contexto>` debe reflejar la jerarquía real
5. **Fechas válidas**: Formato ISO 8601 (YYYY-MM-DD)
6. **Referencias existentes**: Las referencias deben apuntar a artículos existentes

### Esquema XSD (Simplificado)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="https://leychile.cl/schema/ley/v1"
           xmlns:ley="https://leychile.cl/schema/ley/v1"
           elementFormDefault="qualified">
  
  <xs:element name="ley" type="ley:LeyType"/>
  
  <xs:complexType name="LeyType">
    <xs:sequence>
      <xs:element name="metadatos" type="ley:MetadatosType"/>
      <xs:element name="encabezado" type="xs:string"/>
      <xs:element name="contenido" type="ley:ContenidoType"/>
    </xs:sequence>
    <xs:attribute name="version" type="xs:string" use="required"/>
    <xs:attribute name="idioma" type="xs:string" use="required"/>
    <xs:attribute name="id_norma" type="xs:string"/>
    <xs:attribute name="tipo" type="ley:TipoNormaType" use="required"/>
    <xs:attribute name="numero" type="xs:string" use="required"/>
    <xs:attribute name="estado" type="ley:EstadoType" use="required"/>
    <!-- más atributos -->
  </xs:complexType>
  
  <xs:simpleType name="TipoNormaType">
    <xs:restriction base="xs:string">
      <xs:enumeration value="Ley"/>
      <xs:enumeration value="Decreto"/>
      <xs:enumeration value="Decreto Ley"/>
      <xs:enumeration value="Decreto con Fuerza de Ley"/>
      <xs:enumeration value="Código"/>
      <xs:enumeration value="Reglamento"/>
    </xs:restriction>
  </xs:simpleType>
  
  <xs:simpleType name="EstadoType">
    <xs:restriction base="xs:string">
      <xs:enumeration value="vigente"/>
      <xs:enumeration value="derogada"/>
      <xs:enumeration value="parcial"/>
    </xs:restriction>
  </xs:simpleType>
  
  <!-- Más definiciones... -->
</xs:schema>
```

---

## Resumen de Elementos XML

| Elemento | Padre | Hijos | Descripción |
|----------|-------|-------|-------------|
| `<ley>` | (raíz) | metadatos, encabezado, contenido | Elemento raíz |
| `<metadatos>` | ley | titulo, identificacion, organismos, materias, fechas, etc. | Información descriptiva |
| `<encabezado>` | ley | (texto) | Preámbulo de la norma |
| `<contenido>` | ley | libro, titulo, capitulo, parrafo, seccion, articulo | Estructura del articulado |
| `<libro>` | contenido | titulo_seccion, texto, titulo, capitulo, articulo | División mayor (códigos) |
| `<titulo>` | contenido, libro | titulo_seccion, contexto, texto, capitulo, parrafo, seccion, articulo | División principal |
| `<capitulo>` | contenido, titulo | titulo_seccion, contexto, texto, parrafo, seccion, articulo | Subdivisión |
| `<parrafo>` | titulo, capitulo | titulo_seccion, contexto, texto, articulo | Párrafo estructural |
| `<seccion>` | titulo, capitulo, parrafo | titulo_seccion, contexto, texto, articulo | Sección (§) |
| `<articulo>` | cualquier división | contexto, texto\|contenido, referencias | Unidad fundamental |
| `<contenido>` (en artículo) | articulo | parrafo, inciso | Contenido estructurado |
| `<parrafo>` (en artículo) | contenido | (texto) | Párrafo interno |
| `<inciso>` | contenido | (texto) | Inciso numerado |
| `<referencias>` | articulo | ref | Referencias a otros artículos |

---

## Notas de Implementación

1. **Preservar texto original**: Mantener el texto lo más fiel posible al original
2. **IDs estables**: Usar hashes o secuencias que permitan referencias cruzadas estables
3. **Contexto navegable**: El elemento `<contexto>` permite ubicar rápidamente el artículo
4. **Extensibilidad**: El esquema permite agregar elementos adicionales con namespaces
5. **Codificación**: Siempre usar UTF-8
6. **Fechas**: Usar formato ISO 8601 (YYYY-MM-DD)

---

## Limitaciones Conocidas del Parser

El parser `text_to_xml_parser.py` tiene las siguientes limitaciones conocidas al convertir texto plano:

### Detección de Artículos
- ✅ Artículos numerados estándar (`Artículo 1`, `Art. 2`, etc.)
- ✅ Artículos con sufijos latinos (`Artículo 3 BIS`, `Art. 177 TER`, `QUÁTER`, etc.)
- ✅ Artículos con letra simple (`Artículo 355 A`, `Art. 54 Ñ`)
- ✅ Artículos transitorios textuales (`Artículo PRIMERO`, `SEGUNDO`, etc.)
- ✅ Artículos transitorios numerados (`Artículo 1 TRANSITORIO`)
- ⚠️ Puede generar falsos positivos con referencias internas ("artículo 100 de la ley...")

### Detección de Divisiones
- ✅ Libros (`LIBRO PRIMERO`, `LIBRO I`)
- ✅ Títulos (`TÍTULO I`, `TÍTULO PRELIMINAR`)
- ✅ Capítulos (`CAPÍTULO I`, `CAPÍTULO ÚNICO`)
- ✅ Párrafos estructurales (`PÁRRAFO 1º`, `§ 1`)
- ✅ Secciones (`SECCIÓN PRIMERA`)
- ⚠️ La distinción entre "párrafo estructural" y "párrafo de contenido" puede variar

### Limitaciones Generales
1. **Texto vs XML de BCN**: El texto plano puede perder información estructural que el XML de BCN preserva
2. **Artículos derogados**: Si el texto incluye artículos derogados, se parsearán como activos
3. **Incisos complejos**: Incisos con sub-niveles pueden no estructurarse perfectamente
4. **Referencias cruzadas**: Solo se detectan referencias explícitas tipo "artículo X"

### Resultados de Validación (v1.1)

Comparación del parser contra 10 XMLs de la biblioteca BCN:

| Archivo | Tipo | Art. Orig | Art. Parse | Diff | Estado |
|---------|------|-----------|------------|------|--------|
| ley_19628_proteccion_datos.xml | Ley | 27 | 27 | 0 | ✅ |
| ley_19496_consumidor.xml | Ley | 148 | 148 | 0 | ✅ |
| dl_825_iva.xml | DL | 114 | 112 | -2 | ⚠️ |
| codigo_penal.xml | Código | 677 | 46 | -631 | ❌ |
| constitucion.xml | Constitución | 168 | 170 | +2 | ⚠️ |
| codigo_comercio.xml | Código | 1524 | 1524 | 0 | ✅ |
| ley_20730_lobby.xml | Ley | 27 | 27 | 0 | ✅ |
| codigo_civil.xml | Código | 2841 | 2903 | +62 | ❌ |
| ley_19880_procedimiento_administrativo.xml | Ley | 73 | 73 | 0 | ✅ |
| ley_18046_sociedades_anonimas.xml | Ley | 176 | 176 | 0 | ✅ |

**Resumen:**
- ✅ **6/10 archivos con 100% coincidencia** en artículos
- ⚠️ 2 archivos con diferencia menor (±2 artículos)
- ❌ 2 archivos con diferencias estructurales (códigos con formato especial)

**Mejoras v1.1:**
- Eliminado `re.IGNORECASE` de patrones de artículos
- Los artículos ahora deben comenzar con mayúscula ("Artículo", "ARTÍCULO", "Art.")
- Esto evita falsos positivos con referencias en el texto ("artículo 100 de la ley...")

Las diferencias restantes se deben principalmente a:
- Estructura especial del Código Penal (usa "Art." seguido directamente de número)
- Artículos transitorios sin la palabra "Transitorio" explícita
- Diferencias estructurales entre texto plano y XML de BCN

---

*Documento generado para el proyecto LeyChile ePub Generator*  
*Versión del esquema: 1.0*  
*Fecha: 2026-01-12*
