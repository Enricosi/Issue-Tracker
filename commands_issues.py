import pymysql
from exceptions import IssueTrackerError


def cmd_list(args, conn):    
    print('not implemented')

def cmd_add_issue(args, conn):
    try:
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
    except pymysql.OperationalError:
        conn.rollback()
        raise IssueTrackerError('Ocurrio un error inesperado')

def cmd_delete_issue(args, conn):
    print('not implemented')

def cmd_change_status(args, conn):
    print('not implemented')

def cmd_reassing_issue(args, conn):
    print('not implemented')