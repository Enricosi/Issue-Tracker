import datetime
from exceptions import IssueTrackerError

def print_issue(lista):
    """Print a formatted row for each issue in lista.

    Expects each row to follow the column order:
    issue_id, title, posible_cause, creation_date, close_date, status, priority, username.
    """
    for i in lista:
        print(f'ID: {i[0]} | Title: {i[1]} | Posible Cause: {i[2] or "-"} | Creation Date: {i[3]}, | Close Date: {i[4] or "-"} | Status: {i[5]} | Priority: {i[6]} | Username: {i[7] or "-"}')

def cmd_list_issues(args, conn):
    """List issues, optionally filtered by status, username, or both.

    Builds the WHERE clause dynamically so a single query handles all filter
    combinations. Raises IssueTrackerError if the filtered result is empty,
    but prints nothing (no error) when no filters are given and the table is empty.
    """
    with conn.cursor() as cursor:
        username = args.username if args.username else None
        status = args.status if args.status else None
        
        sql = "SELECT i.issue_id, i.title, i.posible_cause, i.creation_date, i.close_date, i.status, i.priority, username" \
            " FROM issue i LEFT JOIN developer d ON i.developer_id = d.developer_id"
        
        conditions = []
        values = []

        if status:
            conditions.append("i.status = %s")
            values.append(status)

        
        if username:
            conditions.append("d.username = %s")
            values.append(username)

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        cursor.execute(sql,values)

        lista = cursor.fetchall()

        if status and username:
            if lista:
                print_issue(lista)
            else:
                raise IssueTrackerError(f'No hay ninguna tarea con estado "{status}" asignada al desarrollador {username}.')

        elif status:
            if lista:
                print_issue(lista)
            else:
                raise IssueTrackerError(f'No hay tareas en estado "{status}".')


        elif username:
            if lista:
                print_issue(lista)
            else:
                raise IssueTrackerError(f'El desarrollador {username} no tiene tareas asignadas.')
        else:
            raise IssueTrackerError(f'No hay tareas para mostrar.')

def cmd_add_issue(args, conn):
    """Insert a new issue, optionally assigned to a developer.

    If --username is given, verifies the developer exists before inserting.
    Raises IssueTrackerError if the username is not found in the database.
    """
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
    """Delete an issue only if its status is 'closed'.

    Raises IssueTrackerError if the issue does not exist or is still open/in_progress.
    """
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
    """Update the status of an issue and set close_date when transitioning to 'closed'.

    Raises IssueTrackerError if the issue does not exist or already has the requested status.
    """
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

            close_date = datetime.datetime.now() if args.new_status == 'closed' else None
            sql3 = "UPDATE issue SET status = %s, close_date = %s WHERE issue_id = %s"
            values3 = (args.new_status, close_date, issue_id[0])
            cursor.execute(sql3, values3)
            conn.commit()
            print('Estado del Issue actualizado con exito')                      

        else:
            raise IssueTrackerError(f'NO hay un Issue con el ID: {args.id}')

def cmd_reassign_issue(args, conn):
    """Reassign an issue to a different developer.

    Raises IssueTrackerError if the issue or the target developer does not exist,
    or if the issue is already assigned to that developer.
    """
    with conn.cursor() as cursor:
        sql = "SELECT issue_id, developer_id FROM issue WHERE issue_id = %s"
        values = (args.id,)
        cursor.execute(sql, values)

        issue = cursor.fetchone()

        issue_id = issue[0] if issue else None
        issue_dev_id = issue[1] if issue else None
        if issue_id == None:
            raise IssueTrackerError(f'No existe un issue con ID: {args.id}')

        sql2 = "SELECT developer_id, username FROM developer WHERE username = %s"
        values2 = (args.username,)
        cursor.execute(sql2, values2)

        dev = cursor.fetchone()
        
        developer_id = dev[0] if dev else None
        username = dev[1] if dev else None
        
        if developer_id == None:
            raise IssueTrackerError(f'No existe un desarrollador con username: {args.username}')
        
        if developer_id == issue_dev_id:
            raise IssueTrackerError(f'Este issue ya esta asigando al desarrollador: {args.username}')

        sql3 = "UPDATE issue SET developer_id = %s WHERE issue_id = %s"
        values3 = (developer_id, issue_id)
        cursor.execute(sql3, values3)
        conn.commit()
        print(f'El issue con ID: {issue_id} fue reasignado con exito al desarrollador: {username}')




