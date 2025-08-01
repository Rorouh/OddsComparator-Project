# OddsComparator – Sistema de Información para Comparar Cuotas Deportivas

> **Proyecto de Ingeniería de Sistemas de Información** que integra *web‑scraping* / consumo de APIs, persistencia en MySQL y una interfaz web ligera para visualizar y comparar cuotas (odds) de casas de apuestas.

---

## Índice

1. [Visión General](#visión-general)
2. [Arquitectura](#arquitectura)
3. [Estructura del Repositorio](#estructura-del-repositorio)
4. [Dependencias y Requisitos](#dependencias-y-requisitos)
5. [Instalación Rápida](#instalación-rápida)
6. [Flujo de ETL](#flujo-de-etl)
7. [Base de Datos](#base-de-datos)
8. [Front‑end](#front-end)
9. [Tareas Automáticas](#tareas-automáticas)
10. [Roadmap](#roadmap)
11. [Créditos](#créditos)
12. [Licencia](#licencia)

---

## Visión General

El objetivo es **agregar información de cuotas deportivas** procedente de distintas fuentes públicas (principalmente la API [https://the-odds-api.com](https://the-odds-api.com)) y mostrar la oferta de varias *bookies* de forma comparativa.

* **Scraper/API Consumer** (Python) recolecta deportes, eventos y cuotas.
* **Persistencia** en AWS RDS MySQL mediante un *schema* relacional normalizado.
* **ETL scripts** convierten el JSON de la API en ficheros intermedios (`*.txt`/`*.html`) y lo cargan en la BD.
* **Front‑end** estático (HTML + CSS + JS) que consume una capa *back‑end* ligera (pendiente) o lee archivos HTML generados.

Actualmente el prototipo se centra en **La Liga española**, pero el pipeline admite cualquier deporte soportado por la API.

---

## Arquitectura

```mermaid
graph TD;    A[API The‑Odds‑API] -- JSON --> B[Scripts Python];    B -- tablas intermedias --> C[MySQL];    C -- JSON / REST (TODO) --> D[Back‑end Flask];    D -- fetch --> E[Front‑end HTML + JS];    style D stroke-dasharray: 5 5;    classDef todo fill:#fff3cd,stroke:#f0ad4e,color:#8a6d3b;    class D todo;
```

| Capa               | Archivo(s) clave                                                    | Función                                                                         |
| ------------------ | ------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Ingesta**        | `conexion_api.py`, `la_liga.py`, `Obtener_cuotas_API.py`            | Descargan lista de deportes, eventos y cuotas en formato JSON → `.txt`/`.html`. |
| **Transformación** | `crear_tabla_bookies.py`                                            | Genera una tabla HTML con cuotas *head‑to‑head* (`h2h`) de cada bookie.         |
| **Carga**          | `guardar_cuotas.py`                                                 | Construye el *schema*, limpia tablas y carga los datos en MySQL.                |
| **Front‑end**      | `index.html`, `styles.css`, `obtener_deportes.js` (por implementar) | Interfaz de usuario para seleccionar eventos y comparar cuotas.                 |

---

## Estructura del Repositorio

```
.
├── data/                 # Ficheros intermedios generados (txt/html)
├── src/                  # Scripts Python de ingesta y ETL
│   ├── conexion_api.py
│   ├── la_liga.py
│   ├── Obtener_cuotas_API.py
│   ├── crear_tabla_bookies.py
│   └── guardar_cuotas.py
├── web/                  # Front‑end estático
│   ├── index.html
│   ├── styles.css
│   └── assets/
│       ├── odds_logo.jpg
│       └── odds_comparator.jpg
├── docs/                 # Diagramas y especificación de BD
└── README.md             # (este archivo)
```

> **Nota:** el ZIP original contenía los scripts y ficheros HTML/TXT en raíz; aquí proponemos una organización más limpia.

---

## Dependencias y Requisitos

### Software

| Herramienta              | Versión mínima        | Uso                                   |
| ------------------------ | --------------------- | ------------------------------------- |
| Python                   | 3.9                   | Scripts de scraping/ETL               |
| `requests`               | 2.25                  | Llamadas HTTP a la API                |
| `mysql‑connector‑python` | 8.x                   | Inserción en MySQL                    |
| MySQL                    | 8.x (local o AWS RDS) | Almacenamiento relacional             |
| Docker (opcional)        | ≥20                   | Contenedor de la BD / futuro back‑end |

### Variables de Entorno

| Nombre                                     | Descripción                               |
| ------------------------------------------ | ----------------------------------------- |
| `ODDS_API_KEY`                             | API key de The‑Odds‑API (no *hardcodear*) |
| `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME` | Credenciales MySQL                        |

> ⚠️ **Seguridad:** en el repo de ejemplo las claves estaban en texto plano. Muévelas a variables de entorno o `.env`.

---

## Instalación Rápida

```bash
# 1. Clonar
$ git clone https://github.com/tu‑usuario/odds‑comparator.git && cd odds‑comparator

# 2. Crear entorno virtual
$ python -m venv .venv && source .venv/bin/activate

# 3. Instalar dependencias
$ pip install -r requirements.txt  # requests, mysql‑connector‑python, python‑dotenv, etc.

# 4. Configurar variables
$ export ODDS_API_KEY="tu‑api‑key"
$ export DB_HOST="xxxx.rds.amazonaws.com"  DB_USER="admin" DB_PASS="•••" DB_NAME="ISI"

# 5. Ejecutar el pipeline completo
$ python src/Obtener_cuotas_API.py      # Descarga todos los deportes
$ python src/guardar_cuotas.py          # Crea esquema + carga datos
$ python src/crear_tabla_bookies.py     # Genera tabla HTML (La Liga)

# 6. Levantar front‑end
$ cd web && python -m http.server 8080   # Navega a http://localhost:8080
```

---

## Flujo de ETL

```text
┌──────────────┐      ┌────────┐      ┌───────────────┐
│  API REST    │ →   │  JSON  │ →   │  Ficheros TXT  │
└──────────────┘      └────────┘      └───────────────┘
                                      │
                                      ▼
                           ┌────────────────────┐
                           │  guardar_cuotas.py │
                           └────────────────────┘
                                      │
                                      ▼
                           ┌────────────────────┐
                           │      MySQL         │
                           └────────────────────┘
                                      │
                                      ▼
                           ┌────────────────────┐
                           │ Front‑end (HTML)   │
                           └────────────────────┘
```

1. **Ingesta** (`Obtener_cuotas_API.py`)

   * Recorre una lista de *sports keys* → `deportes`.
   * Solicita mercado `h2h` en formato decimal (`oddsFormat=decimal`).
   * Filtra solo las *bookies* de interés (`888sport`, `1xBet`, `Betfair`, etc.).
   * Persiste todo en `cuotas_totales.txt`.
2. **Carga** (`guardar_cuotas.py`)

   * Elimina tablas si existen y las recrea (`DROP TABLE IF EXISTS …`).
   * Inserta **Deportes**, **Eventos**, **Bookies** y **Cuotas**.
3. **Transformación HTML** (`crear_tabla_bookies.py`)

   * Consulta nuevamente la API (solo *La Liga*) y produce `cuotas_liga_espanola.html` con una columna por bookie y 1/X/2 de cada partido.

---

## Base de Datos

```sql
CREATE TABLE Deportes (
    id_deporte INT AUTO_INCREMENT PRIMARY KEY,
    nombre_deporte VARCHAR(255) UNIQUE
);

CREATE TABLE Eventos (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    id_deporte INT,
    nombre_evento VARCHAR(255),
    FOREIGN KEY (id_deporte) REFERENCES Deportes(id_deporte)
);

CREATE TABLE Bookies (
    id_bookie INT AUTO_INCREMENT PRIMARY KEY,
    nombre_bookie VARCHAR(255) UNIQUE
);

CREATE TABLE Cuotas (
    id_cuota INT AUTO_INCREMENT PRIMARY KEY,
    id_evento INT,
    id_bookie INT,
    tipo_apuesta CHAR(1),  -- '1', 'X', '2'
    cuota DECIMAL(10,2),
    FOREIGN KEY (id_evento) REFERENCES Eventos(id_evento),
    FOREIGN KEY (id_bookie) REFERENCES Bookies(id_bookie)
);
```

### Poblar manualmente

```bash
$ mysql -h $DB_HOST -u $DB_USER -p $DB_NAME < docs/schema.sql
```

---

## Front‑end

| Elemento              | Descripción                                                                 |
| --------------------- | --------------------------------------------------------------------------- |
| `index.html`          | Página principal con `<select>` de deportes/eventos y tabla de cuotas.      |
| `styles.css`          | Paleta lighweight (#faefee & #cb6466) y layout responsive.                  |
| `obtener_deportes.js` | **Pendiente:** debería hacer *fetch* al back‑end y rellenar los `<select>`. |

> ✨ Se recomienda migrar a React/Vue o, al menos, separar la lógica JS en módulos.

---

## Tareas Automáticas

Ejemplo de *cron* (Linux) para actualizar cuotas cada hora:

```cron
0 * * * * cd /home/ec2-user/odds‑comparator && /usr/bin/python src/Obtener_cuotas_API.py >> logs/etl.log 2>&1
```

* Después del refresh, lanza `guardar_cuotas.py` para mantener la BD actualizada.

---

## Roadmap

* [ ] Implementar *obtener\_deportes.js* y API REST con Flask/FastAPI.
* [ ] Docker Compose con servicio `scraper`, `db` y `web`.
* [ ] Histórico de cuotas para detectar *value bets*.
* [ ] Autenticación y panel de usuario con picks favoritos.
* [ ] CI/CD en GitHub Actions.

---

## Créditos

Proyecto desarrollado por **\[Miguel Angel Lopez Sanchez y Victor Perez Gomez]** para la asignatura *Ingeniería de Sistemas de Información* (2025).

*API utilizada: [The‑Odds‑API.com](https://the-odds-api.com)*.

---
