#
# A class to hold the railroad graph
#
class Routes():
  def __init__(self):
    self.cities = {}

  #
  # Add a route from string like 'AC8'
  #
  def add_route_from_string(self, route):
    (origin, destination, distance) = route
    self.add_route(origin, destination, distance)

  #
  # Add a route from its elements
  #
  def add_route(self, origin, destination, distance):
    if origin not in self.cities:
      self.cities[origin] = {}
    self.cities[origin][destination] = int(distance)

  #
  # Returns the total distance of a route
  #
  def distance(self, route, dist = 0):
    if len(route) <= 1:
      return dist
    elif route[1] not in self.cities[route[0]]:
      return 'NO SUCH ROUTE'
    else:
      new_distance = dist + self.cities[route[0]][route[1]]
      return self.distance(route[1:], new_distance)

  #
  # Returns the total number of stops of a route
  #
  def stops(self, trip):
    return len(trip) - 1

  #
  # Returns all routes between origin and destination up to a limit
  # - limit_func is the limiting function
  # - limit_value is the maximum value that limit_func can have
  #
  def find_all_routes(self, origin, destination, limit_func, limit_value, route=''):
    route = route + origin
    routes = []

    if limit_func(route) >= limit_value:
      if origin == destination:
        return [route]
      else:
        return []
    else:
      if len(route) > 1 and origin == destination:
        routes.append(route)
    
    for city in self.cities[origin]:
      new_routes = self.find_all_routes(city, destination, limit_func, limit_value, route)
      for new_route in new_routes:
        if limit_func(new_route) < limit_value:
          routes.append(new_route)
    return routes
    
  #
  # Returns the shortest route between origin and destination
  # - distance_func is the function used to calculate the route size
  #
  # This method assumes that a route exists.
  #
  def find_shortest_route(self, origin, destination):
    MAX_ROUTE_SIZE = 100
    i = 1
    while True and i < MAX_ROUTE_SIZE:
      routes = self.find_all_routes(origin, destination, self.distance, i)
      i += 1
      if len(routes) >= 1:
        return routes[0]
    return ''
    
  #
  # Returns all routes between origin and destination with exact N stops
  #
  def find_trips_with_n_stops(self, origin, destination, stops):
    return [x for x in self.find_all_routes(origin, destination, self.stops, stops + 1) if self.stops(x) == stops]

  #
  # Returns all routes between origin and destination up to N stops
  #
  def find_trips_up_to_n_stops(self, origin, destination, stops):
    return self.find_all_routes(origin, destination, self.stops, stops + 1)
  
  #
  # Returns all routes between origin and destination up to a certain distance
  #
  def find_all_routes_up_to_distance(self, origin, destination, distance):
    return self.find_all_routes(origin, destination, self.distance, distance)
  

########################################################
#
### MAIN ###
#
#

input = 'AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7'
routes = Routes()
for route in input.strip().replace(' ','').split(','):
  routes.add_route_from_string(route)

# 1. The distance of the route A-B-C.
print 'Output #1: %s' % routes.distance('ABC')

# 2. The distance of the route A-D.
print 'Output #2: %s' % routes.distance('AD')

# 3. The distance of the route A-D-C.
print 'Output #3: %s' % routes.distance('ADC')

# 4 . The distance of the route A-E-B-C-D.
print 'Output #4: %s' % routes.distance('AEBCD')

# 5. The distance of the route A-E-D.
print 'Output #5: %s' % routes.distance('AED')

# 6. The number of trips starting at C and ending at C with a maximum of 3 stops.
print 'Output #6: %s' % len(routes.find_trips_up_to_n_stops('C', 'C', 3))

# 7. The number of trips starting at A and ending at C with exactly 4 stops.
print 'Output #7: %s' % len(routes.find_trips_with_n_stops('A', 'C', 4))

# 8. The length of the shortest route (in terms of distance to travel) from A to C.
print 'Output #8: %s' % routes.distance(routes.find_shortest_route('A', 'C'))

# 9. The length of the shortest route (in terms of distance to travel) from B to B.
print 'Output #9: %s' % routes.distance(routes.find_shortest_route('B', 'B'))

# 10. The number of different routes from C to C with a distance of less than 30.
print 'Output #10: %s' % len(routes.find_all_routes_up_to_distance('C', 'C', 30))



