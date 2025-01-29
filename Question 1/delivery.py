import math
from itertools import permutations
import ast

# Function to calculate the distance between two coordinates using the Haversine formula
def haversine(coord1, coord2):
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c  # Distance in kilometers

# Function to sort deliveries based on priority
def sort_deliveries(deliveries):
    priority_order = {'high': 1, 'medium': 2, 'low': 3}
    return sorted(deliveries, key=lambda x: priority_order[x['priority']])

# Function to find the shortest route using brute force (for small number of deliveries)
def find_shortest_route(deliveries):
    min_distance = float('inf')
    best_route = []

    # Generate all permutations of delivery points
    for perm in permutations(deliveries):
        current_distance = 0
        # Calculate the total distance for this permutation
        for i in range(len(perm) - 1):
            current_distance += haversine(perm[i]['coordinates'], perm[i + 1]['coordinates'])
        
        # Check if this is the shortest distance found
        if current_distance < min_distance:
            min_distance = current_distance
            best_route = perm

    return best_route, min_distance

# Main function to optimize delivery routes
def optimize_delivery_route(deliveries):
    # Step 1: Sort deliveries by priority
    sorted_deliveries = sort_deliveries(deliveries)

    # Step 2: Find the shortest route
    optimized_route, total_distance = find_shortest_route(sorted_deliveries)

    # Prepare output
    output = {
        "optimized_route": [delivery['coordinates'] for delivery in optimized_route],
        "total_distance": total_distance
    }
    return output

# Function to take user input for deliveries
def get_user_input():
    # Get input from the user
    locations_input = input("Enter locations (e.g., [(0, 0), (2, 3), (5, 1), (6, 4), (1, 2)]): ")
    priorities_input = input("Enter priorities (e.g., [high, medium, high, low, medium]): ")

    # Parse the input strings
    locations = ast.literal_eval(locations_input)
    priorities = ast.literal_eval(priorities_input)

    # Create deliveries list
    deliveries = []
    for i in range(len(locations)):
        deliveries.append({
            "location": f"Delivery {i + 1}",
            "priority": priorities[i],
            "coordinates": locations[i]
        })
    
    return deliveries

# Main execution
if __name__ == "__main__":
    deliveries = get_user_input()
    result = optimize_delivery_route(deliveries)
    
    # Format the output as specified
    print("Optimized Route:", result["optimized_route"])
    print(f"Total Distance: {result['total_distance']:.2f} units")