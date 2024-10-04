import heapq
import networkx as nx
import matplotlib.pyplot as plt
import pytz
from datetime import datetime, timedelta
import requests

# Currency conversion using a placeholder for real-time API integration
def convert_currency(amount, from_currency, to_currency):
    # You can integrate a real API for currency conversion here
    # Example API: ExchangeRate-API (https://www.exchangerate-api.com/)
    api_url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(api_url)
    if response.status_code == 200:
        exchange_rates = response.json().get("rates", {})
        conversion_rate = exchange_rates.get(to_currency, 1)  # Fallback to 1 if not found
        return amount * conversion_rate
    else:
        print(f"Error fetching conversion rate. Status code: {response.status_code}")
        return amount  # Fallback to no conversion if API fails

# Function to implement Dijkstra's algorithm
def dijkstra(graph, source, target, optimize_by='time'):
    distances = {airport: float('inf') for airport in graph}
    distances[source] = 0
    pq = [(0, source)]
    previous_nodes = {airport: None for airport in graph}
    
    while pq:
        current_distance, current_airport = heapq.heappop(pq)
        
        if current_airport == target:
            break
        
        for neighbor, travel_time, cost in graph[current_airport]:
            weight = travel_time if optimize_by == 'time' else cost
            new_distance = current_distance + weight
            
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_airport
                heapq.heappush(pq, (new_distance, neighbor))
    
    return distances, previous_nodes

# Function to reconstruct the optimal path from source to target
def reconstruct_path(previous_nodes, source, target):
    path = []
    current_airport = target
    while current_airport is not None:
        path.append(current_airport)
        current_airport = previous_nodes[current_airport]
    return path[::-1]

# Function to visualize the flight routes and highlight the optimal path
def visualize_routes(graph, optimal_path=None):
    G = nx.DiGraph()
    
    for airport in graph:
        for neighbor, travel_time, cost in graph[airport]:
            G.add_edge(airport, neighbor, weight=travel_time)
    
    pos = nx.spring_layout(G)
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    if optimal_path:
        path_edges = [(optimal_path[i], optimal_path[i + 1]) for i in range(len(optimal_path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='green', width=3)
    
    plt.title("Flight Routes")
    plt.show()

# Function to display flight details (total travel time and total cost)
def calculate_total_time_and_cost(graph, optimal_path):
    total_cost = 0
    total_time = 0
    for i in range(len(optimal_path) - 1):
        current_city = optimal_path[i]
        next_city = optimal_path[i + 1]
        for neighbor, travel_time, cost in graph[current_city]:
            if neighbor == next_city:
                total_time += travel_time
                total_cost += cost
                break
    return total_time, total_cost

# Time zone management
def calculate_arrival_time(departure_time, flight_duration, source_tz, destination_tz):
    # Convert the departure time to a timezone-aware datetime object
    tz_source = pytz.timezone(source_tz)
    tz_target = pytz.timezone(destination_tz)
    
    departure_time = tz_source.localize(departure_time)
    arrival_time = departure_time + timedelta(hours=flight_duration)
    
    # Convert arrival time to destination time zone
    arrival_time_in_target_tz = arrival_time.astimezone(tz_target)
    return departure_time, arrival_time_in_target_tz

# Main function to run the itinerary optimization with currency and time zone handling
def flight_itinerary_optimization(graph, source, target, optimize_by='time', currency='INR'):
    # Run Dijkstra's algorithm
    distances, previous_nodes = dijkstra(graph, source, target, optimize_by)
    
    # Reconstruct the optimal path
    optimal_path = reconstruct_path(previous_nodes, source, target)
    
    if distances[target] == float('inf'):
        print(f"No path found from {source} to {target}.")
    else:
        print(f"Optimal itinerary: {' -> '.join(optimal_path)}")
        print(f"Total {optimize_by}: {distances[target]}")
        
        # Calculate total time and cost
        total_time, total_cost = calculate_total_time_and_cost(graph, optimal_path)
        
        # Convert cost to preferred currency
        total_cost_converted = convert_currency(total_cost, 'INR', currency)
        
        print(f"Total travel time: {total_time} hours")
        print(f"Total cost: {total_cost_converted:.2f} {currency}")
        
        # Visualize routes
        visualize_routes(graph, optimal_path)
        
        # Time zone handling
        # Placeholder time zone mappings for cities
        city_timezones = {
            'Delhi': 'Asia/Kolkata',
            'Mumbai': 'Asia/Kolkata',
            'Bengaluru': 'Asia/Kolkata',
            'Chennai': 'Asia/Kolkata',
            'Kolkata': 'Asia/Kolkata'
        }
        
        # Example departure time for the first flight (assumed)
        departure_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        
        print("\nFlight Schedule:")
        for i in range(len(optimal_path) - 1):
            current_city = optimal_path[i]
            next_city = optimal_path[i + 1]
            
            for neighbor, travel_time, cost in graph[current_city]:
                if neighbor == next_city:
                    # Calculate local times for departure and arrival
                    dep_time, arr_time = calculate_arrival_time(
                        departure_time, 
                        travel_time, 
                        city_timezones[current_city], 
                        city_timezones[next_city]
                    )
                    
                    print(f"Flight from {current_city} to {next_city}:")
                    print(f"  Departure: {dep_time.strftime('%Y-%m-%d %H:%M %Z')}")
                    print(f"  Arrival: {arr_time.strftime('%Y-%m-%d %H:%M %Z')}")
                    
                    # Update departure time for the next leg
                    departure_time = arr_time

# Example Graph: Indian Cities and Flight Routes (Adjacency List)
graph = {
    'Delhi': [('Mumbai', 2, 3000), ('Bengaluru', 3, 4500)],
    'Mumbai': [('Bengaluru', 1, 2000), ('Chennai', 3, 2500)],
    'Bengaluru': [('Chennai', 2, 1500), ('Kolkata', 4, 4000)],
    'Chennai': [('Kolkata', 3, 3000)],
    'Kolkata': []
}

# User input for source, target, and optimization criteria
print("Available cities:", ', '.join(graph.keys()))
source = input("Enter the source city: ").strip().title()
target = input("Enter the target city: ").strip().title()
optimize_by = input("Optimize by (time or cost): ").strip().lower()
currency = input("Preferred currency (e.g., USD, EUR, INR): ").strip().upper()

# Validate inputs
if source not in graph:
    print("Invalid source city!")
elif target not in graph:
    print("Invalid target city!")
elif optimize_by not in ['time', 'cost']:
    print("Invalid optimization criteria! Please choose 'time' or 'cost'.")
else:
    # Call the flight itinerary optimization function
    flight_itinerary_optimization(graph, source, target, optimize_by, currency)
