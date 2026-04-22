import pymysql


def cmd_add_developer(args, conn):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO developer (username, first_name, last_name) VALUES (%s, %s, %s)"

            last_name = args.last_name.capitalize() if args.last_name else None

            values = (args.username, args.first_name.capitalize(), last_name)
            cursor.execute(sql, values)
            conn.commit()
    except pymysql.err.IntegrityError:
        conn.rollback()
        print(f'El nombre de usuario {args.username} ya existe, elige otro por favor')

def cmd_remove_developer(args, conn):
    print('not implemented')