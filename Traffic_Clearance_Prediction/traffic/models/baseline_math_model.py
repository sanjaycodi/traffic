"""
baseline_math_model.py
------------------------
A simple formula-based (non-ML) estimate of traffic clearance time.
Used as a benchmark to compare against the ML model.
"""

SATURATION_FLOW_RATE = 0.5  # vehicles/sec (assumption, can be tuned)


def calculate_clearance_time(num_vehicles, avg_speed, road_length,
                              signal_time, arrival_rate):
    """
    Clearance Time = (N / saturation_flow_rate)
                      + travel_delay(road_length, speed)
                      + arrival_rate correction
    """
    speed_m_s = avg_speed * 1000 / 3600  # km/h -> m/s
    travel_delay = (road_length / speed_m_s) * 0.1 if speed_m_s > 0 else 0

    clearance_time = (num_vehicles / SATURATION_FLOW_RATE) + \
                      travel_delay + (arrival_rate * 5)

    return round(clearance_time, 2)


def get_traffic_level(num_vehicles):
    if num_vehicles < 40:
        return "Low"
    elif num_vehicles < 90:
        return "Medium"
    else:
        return "High"


if __name__ == "__main__":
    # Example usage
    result = calculate_clearance_time(
        num_vehicles=50,
        avg_speed=35.0,
        road_length=200.0,
        signal_time=45,
        arrival_rate=1.2
    )
    level = get_traffic_level(50)
    print(f"Traffic Level: {level}")
    print(f"Baseline Predicted Clearance Time: {result} seconds")
