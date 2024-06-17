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

def minXminY():
    # Save the MIN X point into the variable
    minX = min(convex_hull, key=lambda point: (point[0], -point[1]))
    minY = min(convex_hull, key=lambda point: (point[1], -point[0]))
    # Find the position of minX in convex_hull list
    position_minX = convex_hull.index(minX)
    position_minY = convex_hull.index(minY)
    return position_minX, position_minY

# Read points from CSV file
csv_filename = "dataset.csv"
points = []

with open(csv_filename, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Assuming 'awards_count' and 'dblp_records' are used as coordinates
        point = (int(row['awards_count']), int(row['dblp_records']), row['name'])
        points.append(point)

# Arxika trexoume graham scan me ta arxika points
convex_hull = graham_scan(points)

x = []
y = []

# O xrhsths dinei ton arithmo epanalipsewn
userin = int(input("Enter the number of layer: "))

for i in range(0, userin-1):
    # Ksanatrexoume to function minmin gia na paroume ta index pou anhkoun sta min points 
    position_minX, position_minY = minXminY()
    # Afou paroume ta indexes vriskoume akrivws ta points pou antistixoun kai ta vazoyme stis antistixes listes
    x.append(convex_hull[position_minX])
    y.append(convex_hull[position_minY])
    # Ftiaxnoume enan pinaka new_points gia na apothikeuoume ta nea points pou tha doulepsoume
    new_points = []
    # Kanoume elegxo gia na filtraroume ta points
    for point in points:
        # An kapoio point exei x or y syntetagmenh idia me ta prohgoumena min points den to kanoume append sto new_points
        if all(point[0] != x_val[0] and point[1] != y_val[1] for x_val, y_val in zip(x, y)):
            new_points.append(point)
    # Trexoume apo thn arxh to graham scan me ta new points kai pairnoume to neo hull
    convex_hull = graham_scan(new_points)

# Define the pairs you want to connect
pairs_to_connect = []

# Choose a subset
position_minX, position_minY = minXminY()


if (position_minX == len(convex_hull)-1):
    pairs_to_connect.append((len(convex_hull)-1, 0))

if (position_minX < position_minY and position_minX < len(convex_hull)):
    for i in range(position_minX, position_minY):
        pairs_to_connect.append((i, i + 1))

if (position_minX > position_minY):
    for i in range(position_minX, len(convex_hull)-1):
        pairs_to_connect.append((i, i + 1))
    pairs_to_connect.append((len(convex_hull)-1, 0))
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

  