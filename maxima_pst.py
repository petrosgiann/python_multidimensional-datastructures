#Implement the point class
import csv
import json


class Point:
    def __init__(self, awards, dblp_records):
        self.awards = awards
        self.dblp_records = dblp_records
        
class Node:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right
    
#Implement the Priority Search Tree (PST) construction       
def construct_pst(points, dimensions=('awards', 'dblp_records')):
    if not points:
        return None
    
    # Alternate dimensions as you go down the tree
    dimension = dimensions[len(dimensions) % len(points[0].__dict__)]

    # Sort points based on the current dimension
    sorted_points = sorted(points, key=lambda point: getattr(point, dimension))
    
    # Find the median point
    median_index = len(sorted_points) // 2
    
    # Create a node for the median point
    median_point = sorted_points[median_index]
    
    # Recursively construct left and right subtrees
    left_subtree = construct_pst(sorted_points[:median_index], dimensions)
    right_subtree = construct_pst(sorted_points[median_index + 1:], dimensions)
    
    # Return the root node of the subtree
    return Node(median_point, left_subtree, right_subtree)

def calculate_max_max_skyline(pst_root, points):
    skyline_set = set((point.awards, point.dblp_records) for point in points)

    def traverse_and_prune(node):
        nonlocal skyline_set

        if node is None:
            return
        
        while node.right is not None:
            node = node.right

        selected_point = node.point

        dominated_points = set(
            (other_point[0], other_point[1]) 
            for other_point in skyline_set
            if selected_point.awards > other_point[0] or selected_point.dblp_records > other_point[1]
        )

        skyline_set.difference_update(dominated_points)

        traverse_and_prune(node.left)

    traverse_and_prune(pst_root)

    return skyline_set


def calculate_min_min_skyline(pst_root, points):
    skyline_set = set((point.awards, point.dblp_records) for point in points)

    def traverse_and_prune(node):
        nonlocal skyline_set

        if node is None:
            return

        while node.left is not None:
            node = node.left

        selected_point = node.point

        # Identify points dominated by the selected point (smallest X and Y coordinates)
        dominated_points = set(
        (other_point[0], other_point[1])
        for other_point in skyline_set
        if selected_point.awards < other_point[0] or selected_point.dblp_records < other_point[1])
        
        skyline_set.difference_update(dominated_points)

        traverse_and_prune(node.right)

    traverse_and_prune(pst_root)

    return skyline_set

def calculate_max_min_skyline(pst_root, points):
    skyline_set = set((point.awards, point.dblp_records) for point in points)

    def traverse_and_prune(node):
        nonlocal skyline_set

        if node is None:
            return

        max_x_point = node.point

        # Identify points dominated by the selected point (max X and min Y coordinates)
        dominated_points = set(
            (other_point[0], other_point[1])
            for other_point in skyline_set
            if max_x_point.awards > other_point[0] or (max_x_point.awards == other_point[0] and max_x_point.dblp_records < other_point[1])
        )

        skyline_set.difference_update(dominated_points)

        traverse_and_prune(node.left)
        traverse_and_prune(node.right)

    traverse_and_prune(pst_root)

    return skyline_set

def calculate_min_max_skyline(pst_root, points):
    skyline_set = set((point.awards, point.dblp_records) for point in points)

    def traverse_and_prune(node):
        nonlocal skyline_set

        if node is None:
            return

        min_x_point = node.point

        # Identify points dominated by the selected point (min X and max Y coordinates)
        dominated_points = set(
            (other_point[0], other_point[1])
            for other_point in skyline_set
            if min_x_point.awards < other_point[0] or (min_x_point.awards == other_point[0] and min_x_point.dblp_records < other_point[1])
        )

        skyline_set.difference_update(dominated_points)

        traverse_and_prune(node.right)

    traverse_and_prune(pst_root)

    return skyline_set

"""MAIN PROGRAM"""

points = []
# Read data from CSV file and insert into the interval tree
with open('dataset.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        awards = int(row['awards_count'])
        dblp = int(row['dblp_records'])
        points.append(Point(awards, dblp))

# Build PST based on awards dimension
pst_root = construct_pst(points, dimensions=['awards', 'dblp_records'])

max_max_skyline_points = calculate_max_max_skyline(pst_root, points)
print("MAX MAX Skyline Points:")
for point in max_max_skyline_points:
    print(f"({point[0]}, {point[1]})")


min_min_skyline_points = calculate_min_min_skyline(pst_root, points)
print("MIN MIN Skyline Points:")
for point in min_min_skyline_points:
    print(f"({point[0]}, {point[1]})")
    

max_min_skyline_points = calculate_max_min_skyline(pst_root, points)
print("MAX MIN Skyline Points:")
for point in max_min_skyline_points:
    print(f"({point[0]}, {point[1]})")
    
# Calculate MIN MAX skyline points
min_max_skyline_points = calculate_min_max_skyline(pst_root, points)
print("MIN MAX Skyline Points:")
for point in min_max_skyline_points:
    print(f"({point[0]}, {point[1]})")
    
# Display the entire tree
#display_tree(pst_root)

    