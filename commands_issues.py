import pymysql
from exceptions import IssueTrackerError


def cmd_list(args, conn):    
    print('not implemented')

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
    print('not implemented')

def cmd_reassing_issue(args, conn):
    print('not implemented')