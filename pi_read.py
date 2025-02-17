import struct
import constvars
import globals
from liveTriJson import recieve_anchors
from api import update_positions, item_pickup, item_hit, item_use
from speed_control import speed_control

def handle_anchor_distances(data):
    ''' 
    Takes in distances to each anchor and returns the location index
    '''
    print("AnchorDistances:", data)
    loc_index = recieve_anchors({'distances': data})
    write_packet(build_position_estimate_packet(constvars.KART_ID, loc_index))
    return

def handle_ranking_update(data):
    print("RankingUpdate:", data)
    update_positions(data["positions"])
    return

def handle_get_item(data):
    print("GetItem:", data)
    kart_id = data['to']
    item = data['item']
    uid = data['uid']
    if kart_id == constvars.KART_ID and uid not in globals.seen_uids:
        globals.seen_uids.add(uid)
        item_pickup(item)
    return

def handle_do_item(data):
    print("DoItem:", data)
    kart_id = data['to']
    item = data['item']
    uid = data['uid']
    if kart_id == constvars.KART_ID and uid not in globals.seen_uids:
        globals.seen_uids.add(uid)
        speed_control(item)
        item_hit(item, constvars.ITEM_DURATION[item])
    return

def write_packet(packet):
    packet += bytes([0] * (constvars.PACKET_LEN_BYTES - len(packet)))
    globals.ser.write(packet)

def read_packet():
# look for magic number
    maybe_magic = bytes([0, 0, 0, 0])
    while True:
        maybe_magic = maybe_magic[1:] + globals.ser.read(1)
        magic = struct.unpack('<I', maybe_magic)[0]
        if magic == constvars.PACKET_START_MAGIC:
            break  # found the packet start

    # Now read the tag (assume it's a 4-byte integer in little-endian)
    tag_bytes = globals.ser.read(4)
    if len(tag_bytes) < 4:
        return None
    tag = struct.unpack('<I', tag_bytes)[0]

    if tag == 1:  # AnchorDistances: { f32 distances[NUM_ANCHORS]; }
        payload = globals.ser.read(4 * constvars.NUM_ANCHORS)
        if len(payload) < 4 * constvars.NUM_ANCHORS:
            return None
        distances = struct.unpack('<' + 'f' * constvars.NUM_ANCHORS, payload)
        handle_anchor_distances(distances)
        return {'tag': 'AnchorDistances', 'distances': distances}
    
    elif tag == 4:  # RankingUpdate: { u8 positions[NUM_KARTS] }
        payload = globals.ser.read(constvars.NUM_KARTS)  # read NUM_KARTS bytes
        if len(payload) < constvars.NUM_KARTS:
            return None
        positions = struct.unpack('>' + 'B' * constvars.NUM_KARTS, payload)
        handle_ranking_update({'positions': positions})
        return {'tag': 'RankingUpdate', 'positions': positions}
    
    # elif tag == 5:  # GetItem: { u32 to; u32 item; u32 uid }
    #     payload = globals.ser.read(4 + 4 + 4)  # 12 bytes total
    #     if len(payload) < 12:
    #         return None
    #     to_val, item, uid = struct.unpack('<III', payload)
    #     handle_get_item({'to': to_val, 'uid': uid})
    #     return {'tag': 'GetItem', 'to': to_val, 'item': item, 'uid': uid}
    
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
    packet = struct.pack('<I', constvars.PACKET_START_MAGIC)
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


def tests():
    def test_anchor_distances():
        print("Testing AnchorDistances packet")
        handle_anchor_distances([1.0, 2.0, 3.0])
        print("Sent AnchorDistances packet")
    
    def test_ranking_update():
        print("Testing RankingUpdate packet")
        handle_ranking_update({'positions': [1, 2, 3, 4, 5, 6]})
        print("Sent RankingUpdate packet")

    def test_do_item():
        print("Testing DoItem packet")
        handle_do_item({'to': 1, 'item': 2, 'uid': 3})
        print("Sent DoItem packet")

    test_anchor_distances()
    test_ranking_update()
    test_do_item()

    