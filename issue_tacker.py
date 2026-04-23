from parser import parse_args
from dispatch import *
from connect import get_connections
from exceptions import IssueTrackerError


def main():
    args = parse_args()
    conn = get_connections()
    try:
        dispatch(args, conn)
    except IssueTrackerError as e:
        print(e)
    finally:
        if conn.open:    
            conn.close()

if __name__ == '__main__':
    main()