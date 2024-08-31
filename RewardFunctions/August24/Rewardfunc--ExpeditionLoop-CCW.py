import math

class Reward:
    def __init__(self):
        self.prev_speed = 0

    def reward_fun(self, params):
        ################## INPUT PARAMETERS ###################
        # Read input parameters
        distance_from_center = params['distance_from_center']
        is_offtrack = params['is_offtrack']
        is_left_of_center = params['is_left_of_center']
        all_wheels_on_track = params['all_wheels_on_track']
        speed = params['speed']
        steps = params['steps']
        progress = params['progress']
        steering_angle = params['steering_angle']
        track_width = params['track_width']
        waypoints = params['waypoints']
        closest_waypoints = params['closest_waypoints']
        heading = params['heading']

        # Set threshold values
        SPEED_THRESHOLD1 = 1.0  # Student League speed threshold
        DIRECTION_THRESHOLD1 = 3.0
        DIRECTION_THRESHOLD2 = 5.0
        MARKER1 = 0.1 * track_width
        benchmark_steps = 173

        # Waypoints for track optimization
        center = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 23, 27, 28, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 106, 107, 108, 109, 116, 117, 118, 119, 120, 125, 126, 127, 128, 129, 130, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 167, 168, 169, 170, 171, 172, 173, 174]
        off = []
        R = [24, 25, 26, 98, 99, 100, 101, 102, 103, 104, 105, 121, 122, 123, 124]
        L = [18, 19, 20, 21, 22, 29, 30, 31, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 110, 111, 112, 113, 114, 115, 131, 132, 133, 134, 135, 136, 137, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166]
       
        # Initialize reward
        reward = 1.0

        # Penalize if off track
        if is_offtrack:
            return 0.0001

        # Reward for completing the lap faster than benchmark steps
        if progress == 100:
            reward += 100 if steps <= benchmark_steps else 50

        # Track direction calculation
        next_point = waypoints[closest_waypoints[1]]
        prev_point = waypoints[closest_waypoints[0]]
        track_direction = math.degrees(math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]))
        direction_diff = abs(track_direction - heading)

        # Speed Reward
        if speed > SPEED_THRESHOLD1:
            reward += 200
        elif speed > SPEED_THRESHOLD1 - 0.5:
            reward += 100
        elif speed > SPEED_THRESHOLD1 - 1:
            reward += 50

        # Position on Track
        elif closest_waypoints[0] in center and distance_from_center <= MARKER1:
            reward += 150
        elif closest_waypoints[0] in L and is_left_of_center:
            reward += 150
        elif closest_waypoints[0] in R and not is_left_of_center:
            reward += 150
        else:
            reward -= 10

        # Direction and On-Track Bonus
        if direction_diff < DIRECTION_THRESHOLD1 and all_wheels_on_track:
            reward += 100

        # Progress and Steps Rewards
        if (steps % 50) == 0 and progress >= (steps / benchmark_steps) * 100:
            reward += 50
        elif steps > 10 and progress / steps < 1:
            reward -= 1
        else:
            reward += 20

        # Update previous speed
        self.prev_speed = speed

        return float(reward)

reward_obj = Reward()

def reward_function(params):
    return reward_obj.reward_fun(params)
