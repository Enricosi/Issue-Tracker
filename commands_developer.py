import pymysql
from exceptions import IssueTrackerError


def cmd_add_developer(args, conn):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO developer (username, first_name, last_name) VALUES (%s, %s, %s)"

            last_name = args.last_name.capitalize() if args.last_name else None

            values = (args.username, args.first_name.capitalize(), last_name)
            cursor.execute(sql, values)
            conn.commit()
            print(f'Developer {args.username} agregado con exito')
    except pymysql.err.IntegrityError:
        conn.rollback()
        raise IssueTrackerError(f'El nombre de usuario {args.username} ya existe, elige otro por favor')

def cmd_remove_developer(args, conn):
    try:
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
                    print(f'Developer {args.username} removido con exito')
            else:
                raise IssueTrackerError(f'El desarrollador {args.username} no aparece en la base de datos') 
    except pymysql.err.OperationalError:
        conn.rollback()
        raise IssueTrackerError(f'No se pudo remover al developer {args.username} debido a un error inesperado')