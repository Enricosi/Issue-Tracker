import pymysql
from parser import parse_args
from dispatch import *
from connect import get_connection
from exceptions import IssueTrackerError



def main():
    args = parse_args()
    try:
        conn = get_connection()
    except(ValueError, pymysql.err.OperationalError) as e:
        print(e)
        return
    try:
        dispatch(args, conn)
    except IssueTrackerError as e:
        print(e)
    finally:
        if conn.open:    
            conn.close()

if __name__ == '__main__':
    main()