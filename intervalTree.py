import csv
import json
#Implementation of an interval tree
class Node:
    def __init__(self, start, end, name):
        self.start = start
        self.end = end
        self.max = end
        self.left = None
        self.right = None
        self.name = name
        
class IntervalTree:
    def __init__(self):
        self.root = None
        
    def insert(self, start, end, name):
        if not self.root:
            self.root = Node(start, end, name)
        else:
            self._insert(self.root, start, end, name)
            
    def _insert(self, node, start, end, name):
        if start == node.start and end == node.end:
            # Interval already exists, store additional information (name)
            if isinstance(node.name, list):
                node.name.append(name)
            else:
                node.name = [node.name, name]
            return
        
        #Proper checks for the insert operation
        if end > node.max:
            node.max = end
        if start < node.start:
            if node.left:
                self._insert(node.left, start, end, name)
            else:
                node.left = Node(start, end, name)
        else:
            if node.right:
                self._insert(node.right, start, end, name)
            else:
                node.right = Node(start, end, name)
                
    def search(self, start, end):
        result = []
        self._search(self.root, start, end, result)
        return result
    
    def _search(self, node, start, end, result):
        
        #Proper checks for the search operation
        if not node:
            return node
        
        if start >= node.start and end <= node.end:
            #Check if node.name is a list or a string, to handle it properly and in a well-formatted output
            if isinstance(node.name, list):
                for name in node.name:
                    result.append(name)
            else:
                result.append(node.name)
        
        if node.left and node.left.max >= start:
            self._search(node.left, start, end, result)
            
        return self._search(node.right, start, end, result)

if __name__ == "__main__":
    #Main function to test the interval tree
    tree = IntervalTree()

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
                    tree.insert(start_year, end_year, name)
                    
    # Simple menu to get user input for date range
    while True:
        print("Enter the start date (YYYY):")
        query_start = input()
        print("Enter the end date (YYYY):")
        query_end = input()

        try:
            query_start = int(query_start)
            query_end = int(query_end)
        except ValueError:
            print("Please enter valid years (numeric values).")
            continue

        result_node = tree.search(query_start, query_end)
        if result_node:
            print("Scientists overlapping with the range [{}-{}]:".format(query_start, query_end,))
            for name in result_node:
                print(name)
        else:
            print("No intervals found overlapping with the range [{}-{}]".format(query_start, query_end))
            
        print("Do you want to search again? (yes/no)")
        choice = input().strip().lower()
        if choice != 'yes':
            break
    