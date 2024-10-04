# Flight Itinerary Optimizer with Currency Conversion and Time Zone Handling

This project is a Python-based application that helps users find the most optimal flight itinerary between cities, either by minimizing travel time or cost. It integrates **real-time currency conversion** and manages **time zone adjustments** for accurate arrival times at the destination.

---

## Features

- **Flight Itinerary Optimization**: Find the shortest or cheapest flight route between two cities using **Dijkstra's algorithm**.
- **Currency Conversion**: Automatically convert flight costs to the user's preferred currency using real-time exchange rates.
- **Time Zone Handling**: Manage time zone differences to provide accurate departure and arrival times for each leg of the journey.
- **Flight Route Visualization**: Displays a visual representation of the flight routes and highlights the optimal path.

---

## Technologies Used

- **Python**
- **NetworkX**: For representing and processing the graph of cities and flights.
- **Heapq**: For implementing Dijkstra's algorithm efficiently.
- **Matplotlib**: To visualize the flight routes.
- **Pytz**: For managing time zones and adjusting arrival times.
- **Requests**: For real-time currency conversion using an API (can be replaced with a real currency conversion API like ExchangeRate-API).

---

## How It Works

1. **Input**: The user selects:
   - The source and destination cities.
   - Whether they want to optimize by time or cost.
   - Their preferred currency for cost display.
  
2. **Dijkstra's Algorithm**: 
   - The program calculates the shortest or cheapest route between cities using the weighted graph, where weights represent either time or cost.
   
3. **Currency Conversion**: 
   - The cost of the itinerary is converted into the user's preferred currency using a real-time exchange rate.
   
4. **Time Zone Adjustments**: 
   - The departure and arrival times are adjusted to local time zones, providing accurate schedules for each flight leg.

5. **Visualization**:
   - A graph is generated showing the flight routes, with the optimal path highlighted in green.

---

## Installation

### Prerequisites

- Python 3.7 or higher
- Install the required libraries by running the following command:
  
```bash
pip install -r requirements.txt
