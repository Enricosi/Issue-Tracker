def print_issue(lista):
    for i in lista:
        print(f'ID: {i[0]} | Title: {i[1]} | Posible Cause: {i[2] or "-"} | Creation Date: {i[3]}, | Close Date: {i[4] or "-"} | Status: {i[5]} | Priority: {i[6]} | Username: {i[7] or "-"}')

def cmd_list_issues(args, conn):    
    with conn.cursor() as cursor:
        username = args.username if args.username else None
        status = args.status if args.status else None
        
        sql = "SELECT i.issue_id, i.title, i.posible_cause, i.creation_date, i.close_date, i.status, i.priority, username" \
            " FROM issue i LEFT JOIN developer d ON i.developer_id = d.developer_id"
        
        conditions = []
        values = []

        if status:
            conditions.append("i.status = %s")
            values.append(status,)

        
        if username:
            conditions.append("d.username = %s")
            values.append(username,)

        if conditions:
            sql += "WHERE" + "AND".join(conditions)
        

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