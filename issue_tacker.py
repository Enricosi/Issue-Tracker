from parser import parse_args
from dispatch import *


def main():
    args = parse_args()
    dispatch(args)

if __name__ == '__main__':
    main()