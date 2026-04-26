import pymysql
from exceptions import IssueTrackerError

def cmd_list_developers(args, conn):

    with conn.cursor() as cursor:
        sql = "SELECT d.developer_id, d.username, d.first_name, last_name, COUNT(i.issue_id) AS cantidad_tareas FROM developer d " \
        "LEFT JOIN issue i ON i.developer_id = d.developer_id AND i.status IN ('open', 'in_progress')" \
        "GROUP BY d.developer_id;"
        cursor.execute(sql)
        devs = cursor.fetchall()
        if devs:
            for d in devs:
                print(f'| ID: {d[0]} | Username: {d[1]} | First Name: {d[2]} | Last Name: {d[3]} Tareas activas: {d[4]} |')
        else:
            print('No hay desarrolladores que mostrar')

def cmd_add_developer(args, conn):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO developer (username, first_name, last_name) VALUES (%s, %s, %s)"
            last_name = args.last_name.capitalize() if args.last_name else None
            values = (args.username, args.first_name.capitalize(), last_name)
            cursor.execute(sql, values)
            conn.commit()
            print(f'Desarrollador {args.username} agregado con exito')
    
    except pymysql.err.IntegrityError:
        conn.rollback()
        raise IssueTrackerError(f'El nombre de usuario {args.username} ya existe, elige otro por favor')

def cmd_remove_developer(args, conn):

    with conn.cursor() as cursor:
        sql1 = "SELECT developer_id FROM developer WHERE username = %s"
        values1 = (args.username,)
        cursor.execute(sql1, values1)
        existe_dev = cursor.fetchone()
        
        if existe_dev != None:
            sql2 = "SELECT COUNT(*) FROM issue WHERE developer_id = %s"
            values2 = (existe_dev[0],)
            cursor.execute(sql2, values2)
            cantidad_issues = cursor.fetchone()
        
            if cantidad_issues[0] > 0:
                raise IssueTrackerError('No puedes eliminar un desarollador que tiene tareas pendientes')
            else:
                sql3 = "DELETE FROM developer WHERE developer_id = %s"
                values3 = (existe_dev[0],)
                cursor.execute(sql3, values3)
                conn.commit()
                print(f'Desarrollador {args.username} removido con exito')

        else:
            raise IssueTrackerError(f'El desarrollador {args.username} no aparece en la base de datos') 