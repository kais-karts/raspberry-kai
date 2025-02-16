import struct
from constvars import *
import globals
from liveTriJson import recieve_anchors
from api import update_positions, item_pickup, item_hit, item_use

def handle_anchor_distances(data):
    ''' 
    Takes in distances to each anchor and returns the location index
    '''
    print("AnchorDistances:", data)
    loc_index = recieve_anchors({'distances': data})
    write_packet(build_position_estimate_packet(KART_ID, loc_index))
    return

def handle_ranking_update(data):
    print("RankingUpdate:", data)
    update_positions
    return

def handle_get_item(data):
    print("GetItem:", data)
    # Process get item here...
    global CURRENT_PACKET
    CURRENT_PACKET = data
    return

def handle_do_item(data):
    print("DoItem:", data)
    global CURRENT_PACKET
    CURRENT_PACKET = data
    # Process do item here...
    return

def write_packet(packet):
    global ser
    ser.write(packet)


def read_packet():
# look for magic number
    maybe_magic = bytes([0, 0, 0, 0])
    while True:
        maybe_magic = maybe_magic[1:] + globals.ser.read(1)
        # if len(data) < 4:
            # continue  # not enough data, try again
        # Unpack as a little-endian unsigned int
        magic = struct.unpack('<I', maybe_magic)[0]
        if magic == PACKET_START_MAGIC:
            break  # found the packet start

    # Now read the tag (assume it's a 4-byte integer in little-endian)
    tag_bytes = globals.ser.read(4)
    if len(tag_bytes) < 4:
        return None
    tag = struct.unpack('<I', tag_bytes)[0]

    # Tag definitions:
    # 0 = Ping, 1 = AnchorDistances, 2 = PositionEstimate,
    # 3 = UseItem, 4 = RankingUpdate, 5 = GetItem, 6 = DoItem
    if tag == 0:  # Ping: { u32 from; u32 data; }
        payload = globals.ser.read(4 + 4)  # 8 bytes total
        if len(payload) < 8:
            return None
        from_val, data_val = struct.unpack('<II', payload)
        return {'tag': 'Ping', 'from': from_val, 'data': data_val}
    
    elif tag == 1:  # AnchorDistances: { f32 distances[NUM_ANCHORS]; }
        payload = globals.ser.read(4 * NUM_ANCHORS)
        if len(payload) < 4 * NUM_ANCHORS:
            return None
        distances = struct.unpack('<' + 'f' * NUM_ANCHORS, payload)
        handle_anchor_distances(distances)
        return {'tag': 'AnchorDistances', 'distances': distances}
    
    elif tag == 2:  # PositionEstimate: { u32 from; i32 loc_index }
        payload = globals.ser.read(4 + 4)  # 8 bytes total
        if len(payload) < 8:
            return None
        from_val, loc_index = struct.unpack('<Ii', payload)
        return {'tag': 'PositionEstimate', 'from': from_val, 'loc_index': loc_index}
    
    elif tag == 3:  # UseItem: { u32 from; u32 item; }
        payload = globals.ser.read(4 + 4)  # 8 bytes
        if len(payload) < 8:
            return None
        from_val, item = struct.unpack('<II', payload)
        return {'tag': 'UseItem', 'from': from_val, 'item': item}
    
    elif tag == 4:  # RankingUpdate: { u8 positions[NUM_KARTS] }
        payload = globals.ser.read(NUM_KARTS)  # read NUM_KARTS bytes
        if len(payload) < NUM_KARTS:
            return None
        positions = struct.unpack('>' + 'B' * NUM_KARTS, payload)
        handle_ranking_update({'positions': positions})
        return {'tag': 'RankingUpdate', 'positions': positions}
    
    elif tag == 5:  # GetItem: { u32 to; u32 item; u32 uid }
        payload = globals.ser.read(4 + 4 + 4)  # 12 bytes total
        if len(payload) < 12:
            return None
        to_val, item, uid = struct.unpack('<III', payload)
        handle_get_item({'to': to_val, 'uid': uid})
        return {'tag': 'GetItem', 'to': to_val, 'item': item, 'uid': uid}
    
    elif tag == 6:  # DoItem: { u32 to; u32 item; u32 uid }
        payload = globals.ser.read(4 + 4 + 4)  # 12 bytes total
        if len(payload) < 12:
            return None
        to_val, item, uid = struct.unpack('<III', payload)
        handle_do_item({'to': to_val, 'item': item, 'uid': uid})
        return {'tag': 'DoItem', 'to': to_val, 'item': item, 'uid': uid}
    
    else:
        print("Unknown tag:", tag)
        return None


def build_packet(tag, payload_bytes):
    """Build a complete packet with start magic, tag, and payload."""
    packet = struct.pack('<I', PACKET_START_MAGIC)
    packet += struct.pack('<I', tag)
    packet += payload_bytes
    return packet

def build_position_estimate_packet(from_val, loc_index):
    # tag 2
    payload = struct.pack('<BI', from_val, loc_index)
    return build_packet(2, payload)

def build_use_item_packet(from_val, item):
    # tag 3
    payload = struct.pack('<BB', from_val, item)
    return build_packet(3, payload)
