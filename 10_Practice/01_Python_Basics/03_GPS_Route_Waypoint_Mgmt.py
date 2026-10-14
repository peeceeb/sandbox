"""
Challenge 1: GPS Route Waypoint Management (Tuple Unpacking & Immutability)
Scenario:
You are building a navigation system for a vehicle (like your Mahindra XUV700). 
Each route waypoint needs to be stored as a fixed geographical coordinate consisting of (latitude, longitude, altitude_meters). 
Because coordinates shouldn't accidentally change in memory while navigating, tuples are ideal.

Your Task:

Create a list or tuple of 3 waypoints (e.g., Starting Point, Toll Plaza, Destination).
Use tuple unpacking in a loop to extract and print each coordinate component clearly 
(e.g., "Approaching waypoint at Lat: 18.5204, Long: 73.8567, Altitude: 560m").
Attempt to modify one of the coordinates directly (e.g., waypoint[0] = 19.0) and observe/explain the Python error it raises, 
reinforcing why tuples are chosen for read-only fixed data.

"""
##########################----Response----#################################
print(f"####################----Response----###############################")
waypoints=("Starting_Point","Toll Plaza","Destination")

waypoint1,waypoint2,waypoint3=waypoints


print(f"""Waypoint Events at 
          {waypoint1},
          {waypoint2},
          {waypoint3}""")




waypoints=(18.5204,73.8567,560)

print(waypoints)


print(f"""Approaching waypoint at 
          Latitude:  {waypoints[0]},
          Longitude: {waypoints[1]},
          Altitude:  {waypoints[2]}""")

waypoint1=19
print(f"""Approaching waypoint at 
          Latitude:  {waypoint1},
          Longitude: {waypoint2},
          Altitude:  {waypoint3}""")


print("\n\n ****************EXPECTED**************")
################################Expected##################################
# 1. Store a tuple of multiple waypoints 
# (each individual waypoint is a nested tuple: name, latitude, longitude, altitude)
route_waypoints = (
    ("Starting_Point", 18.5204, 73.8567, 560),
    ("Toll_Plaza", 18.5642, 73.7765, 540),
    ("Destination", 18.5590, 73.7868, 550)
)

print("--- Navigating Route (Unpacking in a Loop) ---")
# 2. Use tuple unpacking directly in the loop to extract each component
for name, lat, lon, alt in route_waypoints:
    print(f"Approaching {name} at Lat: {lat}, Long: {lon}, Altitude: {alt}m")

print("\n--- Testing Tuple Immutability ---")
try:
    # 3. Attempting to modify an element inside the tuple directly
    # This will raise a TypeError because tuples are immutable (read-only)
    route_waypoints[0] = ("New_Start", 19.0, 73.0, 500)
    
except TypeError as e:
    print(f"Caught expected error: {e}")
    print("Conclusion: Tuples protect your fixed data from accidental in-place modifications!")



print("\n\n ****************EXPECTED (Using Lists)**************")
################################Expected##################################
# 1. Store a list of multiple waypoints 
# (each individual waypoint is a nested list: name, latitude, longitude, altitude)
route_waypoints = [
    ["Starting_Point", 18.5204, 73.8567, 560],
    ["Toll_Plaza", 18.5642, 73.7765, 540],
    ["Destination", 18.5590, 73.7868, 550]
]

print("--- Navigating Route (Unpacking in a Loop) ---")
# 2. Use unpacking directly in the loop to extract each component
for name, lat, lon, alt in route_waypoints:
    print(f"Approaching {name} at Lat: {lat}, Long: {lon}, Altitude: {alt}m")

print("\n--- Testing List Mutability ---")
# 3. Modifying an element inside the list directly succeeds because lists are mutable
route_waypoints[0] = ["New_Start", 19.0, 73.0, 500]

for name, lat, lon, alt in route_waypoints:
    print(f"Approaching {name} at Lat: {lat}, Long: {lon}, Altitude: {alt}m")
print(f"Successfully updated first waypoint to: {route_waypoints[0]}")
print("Conclusion: Lists allow you to modify data in-place when your collection needs to be dynamic!")
    
