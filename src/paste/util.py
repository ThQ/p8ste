import math

def make_filesize_readable (byte_size):
    result = []
    unit = 0
    size = 0
    while byte_size >= 1024:
        if unit < 4:
            tmp = math.floor(byte_size / 1024)
            size = (size * unit * 10) + tmp
            byte_size = byte_size - (tmp * 1024)
            unit += 1
        else:
            break

    if unit != 0:
        size += byte_size / (1024 * unit)
    else:
        size += byte_size

    size = round(size, 2)
    if size == int(size):
        size = int(size)

    return [size, ["B", "kB", "mB", "gB", "tB"][unit]]
