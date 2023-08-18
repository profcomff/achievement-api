import struct


def is_png(data):
    return (data[:8] == b'\211PNG\r\n\032\n') and (data[12:16] == b'IHDR')


def is_old_png(data):
    return (data[:8] == b'\211PNG\r\n\032\n') and (data[12:16] != b'IHDR')


def get_image_dimensions(data):
    if len(data) < 16:
        return None, None

    elif is_png(data):
        w, h = struct.unpack('>LL', data[16:24])
        width = int(w)
        height = int(h)

    elif is_old_png(data):
        w, h = struct.unpack('>LL', data[8:16])
        width = int(w)
        height = int(h)

    else:
        return None, None

    return width, height
