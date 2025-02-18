import struct
import constvars
import globals
from liveTriJson import recieve_anchors
from speed_control import speed_control
from gpio_logic import light_button, reset_button
import utils
import random
import asyncio
from ui_comms import item_pickup, item_hit, item_use


def handle_anchor_distances(data):
    ''' 
    Takes in distances to each anchor and returns the location index
    '''
    print("AnchorDistances:", data)
    loc, loc_index = recieve_anchors({'distances': data})
    x, y = loc
    globals.update_position(x, y)
    write_packet(build_position_estimate_packet(constvars.KART_ID, x, y,loc_index))
    return

def handle_ranking_update(data):
    print("RankingUpdate:", data)
    positions = data['positions']
    if constvars.KART_ID in data['positions']:
        globals.kart_rank = data['positions'].index(constvars.KART_ID) + 1
    else:
        globals.kart_rank = len(data['positions']) + 1
        positions.append(constvars.KART_ID)
    # was for debugging
    # if globals.counter == None:
    #     globals.counter = 0
    # init_send(globals.counter)
    # globals.counter += 1
    return

def handle_get_item(data):
    print("GetItem:", data)
    kart_id = data['to']
    uid = data['uid']
    if kart_id == constvars.KART_ID and uid not in globals.seen_uids:
        globals.kart_item = utils.draw_item(globals.kart_rank)
        globals.seen_uids.add(uid)
        light_button()
        x, y = globals.get_position()
        asyncio.run(item_pickup(globals.kart_item, x, y))
    return

def handle_do_item(data):
    print("DoItem:", data)
    kart_id = data['to']
    item = data['item']
    uid = data['uid']
    if kart_id == constvars.KART_ID and uid not in globals.seen_uids:
        globals.seen_uids.add(uid)
        speed_control(item)
        x, y = globals.get_position()
        if constvars.ITEMS[item] in constvars.DEBUFF_ITEMS:
            asyncio.run(item_hit(item, x, y))
        elif constvars.ITEMS[item] in constvars.BUFF_ITEMS:
            asyncio.run(item_use(constvars.ITEM_DURATION[item], x, y))
        else:
            print("DoItem: Unknown item type")
    return

def use_item(channel):
    print(f"Button {channel} pressed, item {globals.kart_item} used")
    item = globals.kart_item 
    globals.kart_item = None
    if item is not None:
        uid = random.getrandbits(32)
        print(f"Kart {constvars.KART_ID}, item {item}, uid {uid}")
        x, y = globals.get_position()
        if constvars.ITEMS[item] in constvars.BUFF_ITEMS:
            speed_control(item)
            asyncio.run(item_use(constvars.ITEM_DURATION[item], x, y))
        else:
            asyncio.run(item_use(constvars.ITEM_DURATION[item], x, y))
            write_packet(build_use_item_packet(constvars.KART_ID, item, uid))
        reset_button()


def write_packet(packet):
    packet += bytes([0] * (constvars.PACKET_LEN_BYTES - len(packet)))
    print("writing packet twice", packet)
    globals.ser.write(packet)
    globals.ser.write(packet)
    globals.ser.flush()

def init_send(test: int = 0):
    write_packet(build_position_estimate_packet(constvars.KART_ID, 1, 8, 0))

def read_packet():
# look for magic number
    maybe_magic = bytes([0, 0, 0, 0])
    while True:
        # checking for timed out read
        serial_read = globals.ser.read(1)
        # print(f"reading {serial_read}")
        if (serial_read == b''):
            return
        maybe_magic = maybe_magic[1:] + serial_read
        magic = struct.unpack('<I', maybe_magic)[0]
        if magic == constvars.PACKET_START_MAGIC:
            break  # found the packet start
    print("Magic number found")
    print("seen", globals.seen_uids)
    # Now read the tag (assume it's a 4-byte integer in little-endian)
    tag_bytes = globals.ser.read(4)
    if len(tag_bytes) < 4:
        return None
    tag = struct.unpack('<I', tag_bytes)[0]
    print(f"Tag {tag}")

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
    
    elif tag == 5:  # GetItem: { u32 to; u32 uid }
        payload = globals.ser.read(4 + 4)  # 12 bytes total
        if len(payload) < 8:
            return None
        to_val, uid = struct.unpack('<II', payload)
        handle_get_item({'to': to_val, 'uid': uid})
        return {'tag': 'GetItem', 'to': to_val, 'uid': uid}
    
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

def build_position_estimate_packet(from_val, x, y, loc_index): #TODO: UPDATE ON ESP
    # tag 2
    payload = struct.pack('<IIII', from_val, x, y, loc_index)
    return build_packet(2, payload)

def build_use_item_packet(from_val, item, uid):
    # tag 3
    payload = struct.pack('<III', from_val, item, uid)
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

    