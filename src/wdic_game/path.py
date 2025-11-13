
import math

from .utils import time
from .consts import SCREEN_WIDTH


class Path:
    def __init__(self, start_time: float, points: list[tuple[float, float]], speed: float):
        self.start_time = start_time
        self.points = points
        self.speed = speed
        self.segment_lengths = []
        self.cumulative_lengths = [0.0]

        for i in range(len(points) - 1):
            dx = points[i + 1][0] - points[i][0]
            dy = points[i + 1][1] - points[i][1]
            seg_length = math.sqrt(dx**2 + dy**2)
            self.segment_lengths.append(seg_length)
            self.cumulative_lengths.append(self.cumulative_lengths[-1] + seg_length)

        self.total_length = self.cumulative_lengths[-1]
    
    def get_position(self, time: float) -> tuple[float, float]:
        if time < self.start_time:
            return None

        distance = self.speed * (time - self.start_time)
        if distance >= self.total_length:
            return None

        # Find the segment
        for i in range(len(self.segment_lengths)):
            if distance <= self.cumulative_lengths[i + 1]:
                dist_into_seg = distance - self.cumulative_lengths[i]
                fraction = dist_into_seg / self.segment_lengths[i]
                p1 = self.points[i]
                p2 = self.points[i + 1]
                x = p1[0] + fraction * (p2[0] - p1[0])
                y = p1[1] + fraction * (p2[1] - p1[1])
                return (x, y)

        return self.points[-1]
    
    def is_finished(self, time: float) -> bool:
        distance = self.speed * (time - self.start_time)
        return distance >= self.total_length


def build_dive_path(time_offset: float, depth: int = 300, speed: int = 200, width: int = SCREEN_WIDTH - 200) -> Path:
    x = SCREEN_WIDTH / 2 - width / 2
    return Path(time() + time_offset, [(x, -100), (x, depth), (SCREEN_WIDTH - x, depth), (SCREEN_WIDTH - x, depth), (SCREEN_WIDTH - x, -100)], speed)