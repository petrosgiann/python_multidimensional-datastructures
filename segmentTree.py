import csv
import json

def buildTree(node, start, end, year_index_map):
    if(start == end):
        # Leaf node will have a single element, initialize it as an empty list
        year = A[start][1]
        if tree[node] is None:
            tree[node] = {}
        
        #Update the dictionary of the leaf node
        if year in tree[node]:
            tree[node][year].append(A[start])
        else: #If the year is not in the dictionary, create a new entry
            tree[node][year] = [A[start]]
            
        #Update the year-index mappin
        if year not in year_index_map:
            year_index_map[year] = start
        
    else:
        mid = (start + end) // 2
        #Recurse on the left child
        buildTree(2 * node, start, mid, year_index_map)
        #Recurse on the right child
        buildTree(2 * node + 1, mid + 1, end, year_index_map)
        
        #Merge the dictionaries of the left and right children
        if tree[node] is None:
            tree[node] = {} # Initialize with an empty dictionary
            
        if tree[2 * node] is not None:
            tree[node].update(tree[2 * node])
            
        if tree[2 * node + 1] is not None:
            for year, scientists in tree[2 * node + 1].items():
                if year in tree[node]:
                    tree[node][year].extend(scientists)
                else:
                    tree[node][year] = scientists    
        
def query(tree, qlow, qhigh, low, high, pos, year):
    if qlow > high or qhigh < low:
        # No intersection between the query range and the current segment
        return []
    if qlow <= low and qhigh >= high:
        # Full overlap: the current segment is fully contained within the query range
       # Return names of scientists with the queried year
        return [entry[0] for entry in tree[pos][year]]
    mid = (low + high) // 2
    
    # Recur for left and right children
    left_result = query(tree, qlow, qhigh, low, mid, 2 * pos, year)
    right_result = query(tree, qlow, qhigh, mid + 1, high, 2 * pos + 1, year)
    
    # Merge the results from left and right children
    return left_result + right_result


if __name__ == "__main__" :
    
    # Define input array A
    A = []
    
    # Read data from CSV file and insert into the interval tree
    with open('dataset.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            years_str = row['years']
            if years_str:  # Check if years_str is not empty
                years = json.loads(years_str)
                for year_range in years:
                    start_year, end_year = year_range
                    for year in range (start_year, end_year + 1):
                        A.append([name, year])

    # Initialize the segment tree
    tree = [None] * ((len(A)) * 4)  # Initialize with None values
    year_index_map = {}  # Initialize an empty dictionary for year-index mapping
    
    # Build the segment tree
    buildTree(1, 0, len(A) - 1, year_index_map)
        
    # Simple menu to get user input for date range
    while True:
        print("Enter the date you want to search for (YYYY):")
        query_year = input()

        try:
            query_year = int(query_year)
        except ValueError:
            print("Please enter a valid year (numeric value).")
            continue
        
        index = year_index_map[query_year]
        query_result = query(tree, index, index, 0, len(A) - 1, 1, query_year)
        if query_result:
            print("Scientists published in", query_year, ":")
            for name in query_result:
                print(name)
        else:
            print("No publications found for the year", query_year)
            
        print("Do you want to search again? (yes/no)")
        choice = input().strip().lower()
        if choice != 'yes':
            break