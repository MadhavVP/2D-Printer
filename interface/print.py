import sys
from time import sleep
from movement import Head

def main():
    if len(sys.argv) < 2:
        print("Error: specify a .mcode file as argument")
        return

    fname = sys.argv[1]
    if not fname.endswith(".mcode"):
        print(f'Error: {fname} is not a .mcode file')
        return

    head = Head()

    try:
        with open(fname, 'r') as f:
            for line in f:
                clean = line.strip()
                if clean[0] == 'Z':
                    if clean[1] == '0':
                        #eventually
                        #head.release()
                        sleep(0.0001)
                    else:
                        #head.activate()
                        sleep(0.0001)
                else:
                    coords = clean.split()
                    x = int(coords[0][1:])
                    y = int(coords[1][1:])
                    head.move(x, y)
                    print(f'Moved to ({x}, {y})')

    except FileNotFoundError:
        print(f'Error: {fname} was not found')
    except Exception as e:
        print(f'Error: {e}')

    head.close()

if __name__ == "__main__":
    main()
