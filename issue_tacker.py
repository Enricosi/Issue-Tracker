from parser import parse_args
from dispatch import *
from connect import get_connections


def main():
    args = parse_args()
    conn = get_connections()
    try:
        dispatch(args, conn)
    finally:
        if conn.open:    
            conn.close()

if __name__ == '__main__':
    main()