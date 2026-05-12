# Issue Tracker CLI

CLI para gestionar issues y desarrolladores desde la terminal, con persistencia en MySQL.

## Requisitos

- Python 3.8+
- MySQL
- Dependencias: `pymysql`, `python-dotenv`

```bash
pip install pymysql python-dotenv
```

## Configuración

Copia `.env.example` a `.env` y completa los valores:

```bash
cp .env.example .env
```

```env
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
```

## Uso

```bash
python issue_tracker.py <comando> [argumentos]
```

---

## Comandos

### Issues

#### `list_issues`
Lista los issues. Sin filtros muestra todos.

| Opción | Descripción |
|--------|-------------|
| `-s`, `--status` | Filtra por estado: `open`, `in_progress`, `closed` |
| `-u`, `--username` | Filtra por desarrollador asignado |

```bash
python issue_tracker.py list_issues
python issue_tracker.py list_issues -s open
python issue_tracker.py list_issues -u john -s in_progress
```

#### `add_issue`
Crea un nuevo issue.

| Argumento | Descripción |
|-----------|-------------|
| `title` | Título del issue |
| `priority` | Prioridad: `1`, `2` o `3` (3 = máxima) |
| `-u`, `--username` | Desarrollador asignado (opcional) |
| `-p`, `--posible_cause` | Posible causa (opcional) |

```bash
python issue_tracker.py add_issue "Login falla" 2
python issue_tracker.py add_issue "Login falla" 2 -u john -p "Token expirado"
```

#### `delete_issue`
Elimina un issue. Solo se pueden eliminar issues con estado `closed`.

```bash
python issue_tracker.py delete_issue <id>
```

#### `change_status`
Cambia el estado de un issue. Al pasar a `closed` se registra la fecha de cierre automáticamente.

```bash
python issue_tracker.py change_status <id> <new_status>
python issue_tracker.py change_status 5 closed
```

#### `reassing_issue`
Reasigna un issue a otro desarrollador.

```bash
python issue_tracker.py reassing_issue <id> <username>
```

---

### Desarrolladores

#### `list_developers`
Lista los desarrolladores con su cantidad de issues activos.

| Opción | Descripción |
|--------|-------------|
| `-u`, `--username` | Muestra solo ese desarrollador (opcional) |

```bash
python issue_tracker.py list_developers
python issue_tracker.py list_developers -u john
```

#### `add_developer`
Registra un nuevo desarrollador.

| Argumento | Descripción |
|-----------|-------------|
| `username` | Nombre de usuario (único) |
| `first_name` | Nombre |
| `-l`, `--last_name` | Apellido (opcional) |

```bash
python issue_tracker.py add_developer john John
python issue_tracker.py add_developer john John -l Doe
```

#### `remove_developer`
Elimina un desarrollador. No se puede eliminar si tiene issues activos asignados.

```bash
python issue_tracker.py remove_developer <username>
```
