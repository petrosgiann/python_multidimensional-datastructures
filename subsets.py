from math import atan2
import matplotlib.pyplot as plt
import csv

def orientation(p, q, r):
    """
    Function to determine the orientation of triplet (p, q, r).
    Returns:
    0: Collinear points
    1: Clockwise orientation
    2: Counterclockwise orientation
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def graham_scan(points):
    """
    Function to find the convex hull of a set of points using Graham's Scan algorithm.
    """
    n = len(points)
    if n < 3:
        print("Convex hull not possible with less than 3 points.")
        return

    # Find the point with the lowest y-coordinate (and leftmost if ties)
    pivot = min(points, key=lambda point: (point[1], point[0]))

    # Sort the points based on polar angle with respect to the pivot
    sorted_points = sorted(points, key=lambda point: (atan2(point[1] - pivot[1], point[0] - pivot[0]), point))

    # Firstly, the hull has the pivot and the first sorted point
    hull = [pivot, sorted_points[0]]

    for i in range(1, n):
        while len(hull) > 1 and orientation(hull[-2], hull[-1], sorted_points[i]) != 2:
            hull.pop()
        hull.append(sorted_points[i])

    return hull

# Read points from CSV file
csv_filename = "dataset.csv"
points = []

with open(csv_filename, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Assuming 'awards_count' and 'dblp_records' are used as coordinates
        point = (int(row['awards_count']), int(row['dblp_records']), row['name'])
        points.append(point)

# Example usage with the imported points
convex_hull = graham_scan(points)

# Visualization of the CH
#for simplex in zip(convex_hull, convex_hull[1:] + [convex_hull[0]]):
    #plt.plot([simplex[0][0], simplex[1][0]], [simplex[0][1], simplex[1][1]], 'k-')

def maxXmaxY():
    # Save the MAX X point into the variable
    maxX = min(convex_hull, key=lambda point: (-point[0], point[1]))
    maxY = min(convex_hull, key=lambda point: (-point[1], point[0]))
    # Find the position of maxX in convex_hull list
    position_maxX = convex_hull.index(maxX)
    position_maxY = convex_hull.index(maxY)
    return position_maxX, position_maxY

def maxXminY():
    # Save the MAX Y point into the variable
    maxX = min(convex_hull, key=lambda point: (point[0], point[1]))
    minY = min(convex_hull, key=lambda point: (-point[0], point[1]))
    # Find the position of maxY in convex_hull list
    position_maxX = convex_hull.index(maxX)
    position_minY = convex_hull.index(minY)
    return position_maxX, position_minY

def minXminY():
    # Save the MIN X point into the variable
    minX = min(convex_hull, key=lambda point: (-point[1], point[0]))
    minY = min(convex_hull, key=lambda point: (point[1], -point[0]))
    # Find the position of minX in convex_hull list
    position_minX = convex_hull.index(minX)
    position_minY = convex_hull.index(minY)
    return position_minX, position_minY

def minXmaxY():
    # Save the MIN Y point into the variable
    minX = min(convex_hull, key=lambda point: (point[0], -point[1]))
    maxY = min(convex_hull, key=lambda point: (point[1], point[0]))
    # Find the position of minY in convex_hull list
    position_minX = convex_hull.index(minX)
    position_maxY = convex_hull.index(maxY)
    return position_minX, position_maxY


# Define the pairs you want to connect
pairs_to_connect = []

selection = int(input("\n1. MIN X, MIN Y\n2. MIN X, MAX Y\n3. MAX X, MIN Y\n4. MAX X, MAX Y\n5. Show all the CH\n\nChoose one:"))

# Choose a subset
if (selection == 1):
    position_minX, position_minY = minXminY()
elif (selection == 2):
    position_minX, position_minY = minXmaxY()
elif (selection == 3):
    position_minX, position_minY = maxXminY()
elif (selection == 4):
    position_minX, position_minY = maxXmaxY()
elif (selection == 5):
    position_minX = 0
    position_minY = len(convex_hull) - 1
    pairs_to_connect.append((len(convex_hull)-1, 0))


if (position_minX == len(convex_hull)-1):
    pairs_to_connect.append((len(convex_hull)-1, 0))

if (position_minX < position_minY and position_minX < len(convex_hull)):
    for i in range(position_minX, position_minY):
        pairs_to_connect.append((i, i + 1))

if (position_minX > position_minY):
    for i in range(0, position_minY):
        pairs_to_connect.append((i, i + 1))

# Visualization
first_point = convex_hull[pairs_to_connect[0][0]][:2]
for pair in pairs_to_connect:
    point1 = convex_hull[pair[0]][:2]  # Extracting only the coordinates
    point2 = convex_hull[pair[1]][:2]  # Extracting only the coordinates
    plt.plot([point1[0], point2[0]], [point1[1], point2[1]], 'k-')

# Plot the points
x, y, names = zip(*points)
plt.plot(x, y, 'o', label='Data Points')

# Annotate the points with names
#for i, txt in enumerate(points):
    #plt.annotate(f'({txt[0]}, {txt[1]}) {txt[2]}', (txt[0], txt[1]), textcoords="offset points", xytext=(0,5), ha='center')

plt.xlabel('awards_count')
plt.ylabel('dblp_record')
plt.title('Convex Hull Visualization')
plt.legend()
plt.show()

  