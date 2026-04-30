import datetime
from exceptions import IssueTrackerError

def print_issue(lista):
    for i in lista:
        print(f'ID: {i[0]} | Title: {i[1]} | Posible Cause: {i[2] or "-"} | Creation Date: {i[3]}, | Close Date: {i[4] or "-"} | Status: {i[5]} | Priority: {i[6]} | Username: {i[7] or "-"}')

def cmd_list_issues(args, conn):    
    with conn.cursor() as cursor:
        username = args.username if args.username else None
        status = args.status if args.status else None
        if status and username:
            sql3 = "SELECT i.issue_id, i.title, i.posible_cause, i.creation_date, i.close_date, i.status, i.priority, username" \
                    " FROM issue i LEFT JOIN developer d ON i.developer_id = d.developer_id WHERE i.status = %s AND d.username = %s"
            values3 = (status, username)
            cursor.execute(sql3, values3)
            lista_mixta = cursor.fetchall()

            if lista_mixta:
                print_issue(lista_mixta)

            else:
                raise IssueTrackerError(f'No hay ninguna tarea con estado "{status}" asignada al desarrollador {username}.')
    
        elif username:
            sql1 = "SELECT i.issue_id, i.title, i.posible_cause, i.creation_date, i.close_date, i.status, i.priority, d.username" \
                    " FROM issue i LEFT JOIN developer d ON i.developer_id = d.developer_id WHERE d.username = %s"
            values1 = (username,)
            cursor.execute(sql1, values1)
            lista_username = cursor.fetchall()

            if lista_username:    
                print_issue(lista_username)                 

            else:
                raise IssueTrackerError(f'El desarrollador {username} no tiene tareas asignadas.')

        elif status:
            sql2 = "SELECT i.issue_id, i.title, i.posible_cause, i.creation_date, i.close_date, i.status, i.priority, d.username" \
                    " FROM issue i LEFT JOIN developer d ON i.developer_id = d.developer_id WHERE i.status = %s"
            values2 = (status,)
            cursor.execute(sql2, values2)
            lista_status = cursor.fetchall()

            if lista_status:
                print_issue(lista_status)
            else:
                raise IssueTrackerError(f'No hay tareas en estado "{status}".')

        else:
            sql4 = "SELECT i.issue_id, i.title, i.posible_cause, i.creation_date, i.close_date, i.status, i.priority, d.username" \
                        " FROM issue i LEFT JOIN developer d ON i.developer_id = d.developer_id"
            cursor.execute(sql4)
            lista = cursor.fetchall()

            if lista:
                print_issue(lista)
            else:
                raise IssueTrackerError(f'No hay tareas para mostrar.')

def cmd_add_issue(args, conn):
    
    with conn.cursor() as cursor:
        posible_cause = args.posible_cause if args.posible_cause else None
        if args.username:
            sql1 = "SELECT developer_id FROM developer WHERE username = %s"
            values1 = (args.username,)
            cursor.execute(sql1, values1)
            id_dev = cursor.fetchone()
            if id_dev is None:
                raise IssueTrackerError(f'No existe un desarrollador con Username: {args.username}')
            sql2 = "INSERT INTO issue (title, posible_cause, priority, developer_id) VALUES (%s, %s, %s, %s)"
            values2 = (args.title, posible_cause, args.priority, id_dev[0])
            cursor.execute(sql2, values2)
        else:   
            sql3 = "INSERT INTO issue (title, posible_cause, priority) VALUES (%s, %s, %s)"
            values3 = (args.title, posible_cause, args.priority)
            cursor.execute(sql3, values3)
        conn.commit()
        print(f'El Issue {args.title} ha sido agregado con exito')

def cmd_delete_issue(args, conn):
    with conn.cursor() as cursor:
        sql = "SELECT issue_id FROM issue WHERE issue_id = %s"
        values = (args.id,)
        cursor.execute(sql, values)

        issue_id = cursor.fetchone()

        if issue_id:
            sql2 = "SELECT status FROM issue WHERE issue_id = %s AND status = 'closed'"
            values2 = (issue_id[0],)
            cursor.execute(sql2, values2)
            is_closed = cursor.fetchone()

            if is_closed:
                sql3 = "DELETE FROM issue WHERE issue_id = %s"
                values3 = (issue_id[0],)
                cursor.execute(sql3, values3)
                conn.commit()
                print(f'El Issue con ID: {issue_id[0]} fue eliminado correctamente')
            else:
                raise IssueTrackerError('No puedes eliminar un Issue con estado open o in_progress')
        else:
            raise IssueTrackerError(f'NO hay un Issue con el ID: {args.id}')

def cmd_change_status(args, conn):
    with conn.cursor() as cursor:
        sql = "SELECT issue_id FROM issue WHERE issue_id = %s"
        values = (args.id,)
        cursor.execute(sql, values)

        issue_id = cursor.fetchone()

        if issue_id:
            sql2 = "SELECT status FROM issue WHERE issue_id = %s"
            values2 = (issue_id,)
            cursor.execute(sql2, values2)
            
            status = cursor.fetchone()

            if status[0] == args.new_status:
                raise IssueTrackerError('El estado introducido es el estado actual del Issue')
        
            if args.new_status == 'closed':
                ahora = datetime.datetime.now()

                sql3 = "UPDATE issue SET status = %s, close_date = %s WHERE issue_id = %s"
                values3 = (args.new_status, ahora, issue_id[0])
                cursor.execute(sql3, values3)
                conn.commit()
                print('Estado del Issue actualizado con exito')
            else:
                close_date  = None

                sql4 = "UPDATE issue SET status = %s, close_date = %s WHERE issue_id = %s"
                values4 = (args.new_status, close_date, issue_id[0])
                cursor.execute(sql4, values4)
                conn.commit()       
                print('Estado del Issue actualizado con exito')                       
        else:
            raise IssueTrackerError(f'NO hay un Issue con el ID: {args.id}')

def cmd_reassing_issue(args, conn):
    print('not implemented')