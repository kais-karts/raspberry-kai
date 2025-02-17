import numpy as np
import cv2 as cv
import pickle
from itertools import product
import time
from typing import Dict, Tuple, List, Optional
from globals import *
from constvars import *

def circle_intersection(point: Tuple[int, int], radius: float, track_set: set) -> List[Tuple[int, int]]:
    """Find intersection points of a circle centered at 'point' with 'track'."""
    angles = np.linspace(0, 2 * np.pi, int(abs(radius * 8)))
    x_points = np.round(point[1] + radius * np.cos(angles)).astype(int)
    y_points = np.round(point[0] + radius * np.sin(angles)).astype(int)
    circle_points = set(zip(x_points, y_points))

    # Only check intersections with the track_set for fast lookup
    intersections = [(x, y) for x, y in circle_points if (x, y) in track_set]

    return intersections

def get_location(
    close_beacons: Dict[str, float],
    track_set: set,
    last_point: Optional[Tuple[int, int]],
    beacons: Dict[str, Tuple[int, int]],
) -> Optional[Tuple[int, int]]:
    """Estimate the location based on beacon distances."""
    if len(close_beacons) == 1:
        beacon_name = next(iter(close_beacons))  # Get the single beacon name
        beacon_position = beacons[beacon_name]
        track_intersection_points = circle_intersection(beacon_position, close_beacons[beacon_name], track_set)

        if last_point is None:
            return track_intersection_points[0]
        
        if not track_intersection_points:
            return last_point

        # Find the closest intersection point to last_point
        best_point = min(track_intersection_points, key=lambda p: np.linalg.norm(np.array(p) - np.array(last_point)))
        return best_point

    else:
        track_intersection_points = []
        for beacon_name in close_beacons:
            beacon_position = beacons[beacon_name]
            intersections = circle_intersection(beacon_position, close_beacons[beacon_name], track_set)
            if intersections:
                track_intersection_points.append(intersections)

        if len(track_intersection_points) < 2:
            return last_point  # Not enough intersection points to compute location

        all_combinations = np.array(list(product(*track_intersection_points)))  # All possible combinations

        # Compute pairwise distances for each set
        diffs = all_combinations[:, :, np.newaxis, :] - all_combinations[:, np.newaxis, :, :]
        dists = np.linalg.norm(diffs, axis=-1)  # Compute Euclidean distances

        # Sum pairwise distances within each set (ignore self-distances using np.triu)
        total_dists = np.sum(np.triu(dists, k=1), axis=(1, 2))

        # Find the best set with minimum total distance
        best_idx = np.argmin(total_dists)
        best_set = all_combinations[best_idx]
        location = tuple(np.mean(best_set, axis=0).astype(int))  # Compute average location
        return location
    
def recieve_anchors(data: dict) -> int:
    # Expect data = {distances: [distance, ...]}
    global TRACK_LIST, TRACK_SET, BEACONS, last_point, BRANCH_INFO
    uwb_data = dict()
    # Convert distances from cm to feet
    for ix, distance in enumerate(data["distances"]):
        uwb_data[ix] = distance * 0.03280841666667

    location = get_location(uwb_data, TRACK_LIST, TRACK_SET, last_point, BEACONS)
    last_point = location
    print(location)
    # start and end track index and location
    if inRect((0,100), (0, 500), location) or inRect((200,100), (200, 500), location):
        #scaled distance of BRANCH_INFO["end_pos"]
        distance_to_branch_end = np.linalg.norm(np.array(location) - np.array(BRANCH_INFO["end_pos"]))
        return int(BRANCH_INFO["start_idx"] + (distance_to_branch_end - BRANCH_INFO["max_dist"]) * (BRANCH_INFO["end_idx"] - BRANCH_INFO["start_idx"]) / -BRANCH_INFO["max_dist"])
    else:
        location_index = TRACK_LIST.index(location)

    return location_index

def inRect(bottom_left, top_right, point):
    return bottom_left[0] <= point[0] <= top_right[0] and bottom_left[1] <= point[1] <= top_right[1] 

def init():
    # Load image and track data
    global TRACK_LIST, TRACK_SET, BEACONS, last_point, BRANCH_INFO
    TRACK_LIST = pickle.load(open('ordered_points.pkl', 'rb'))
    TRACK_SET = set(TRACK_LIST)  # Create the set for fast lookup
    BRANCH_INFO = {"start_pos": (100,200), "start_idx": 800, "end_pos": (300,400), "end_idx": 1100}
    BRANCH_INFO["max_dist"] = np.linalg.norm(np.array(BRANCH_INFO["start_pos"]) - np.array(BRANCH_INFO["end_pos"]))

    # Define beacons location
    BEACONS = {
        "0": (200, 27),  # y, x top left IN FOOT
        "1": (300, 30),  # mid
        "Beacon 3": (500, 27)   # left
    }

    last_point = None

# # Run the localization algorithm
# if __name__ == '__main__':
#     ser = serial.Serial('COM27', 9600)

#     # Load image and track data
#     track_list = pickle.load(open('ordered_points.pkl', 'rb'))
#     track_set = set(track_list)  # Create the set for fast lookup

#     # Define beacons
#     beacons: Dict[str, Tuple[int, int]] = {
#         "0": (200, 27),  # y, x top left IN FOOT
#         "1": (300, 30),  # mid
#         "Beacon 3": (500, 27)   # left
#     }

#     update_time = .1
#     last_point = None
#     start_time = time.time()

#     while True:
#         # Read serial data 
#         try:
#             beacons_data = ser.readline().decode('utf-8').strip()
#             if not beacons_data:
#                 continue
#             try:
#                 uwb_data = json.loads(beacons_data)
#                 # Convert distances from cm to feet
#                 for key in uwb_data:
#                     uwb_data[key] = uwb_data[key] * 0.03280841666667
#             except json.JSONDecodeError:
#                 continue

#             location = get_location(uwb_data, track_list, track_set, last_point, beacons)
#             last_point = location
#             print(location)
#             # find the index of location in the track_list
#             location_index = track_list.index(location)
#             # send json PE data for location
#             data = {
#                 "id": uuid.uuid4().int & (1<<32)-1,
#                 "tags": "pe",
#                 "args": {   
#                     "from": 0,
#                     "position": {
#                         "loc_index": location_index,
#                     }
#                 }
#             }
#             ser.write(json.dumps(data).encode())
#         except KeyboardInterrupt:
#             break
        
# cv.destroyAllWindows()
# ser.close()
