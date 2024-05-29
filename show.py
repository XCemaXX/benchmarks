import os
from collections import defaultdict
from collections import namedtuple
import csv
import math

TestInfo = namedtuple("Data", "cpu author compiler test subtest test_data")
TestData = namedtuple("TestData", "avg_time max_time")

def parse_csv(path):
    with open(path, 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.reader(file)
        header = list(next(reader))
        subtests = [dict(zip(header,row)) for row in reader]
    return subtests

file_list = defaultdict(list)
search_dir = './results'
for root, dirs, files in os.walk(search_dir):
    for file in files:
        path = os.path.join(root, file)
        test = file[:-4]
        splitted = path[len(search_dir):].split('/')
        if len(splitted) == 5: # work around
            start_index = -3
            compiler = splitted[-2]
        else:
            start_index = -2
            compiler = 'None'
        author = splitted[start_index]
        cpu = splitted[start_index - 1]

        subtests = parse_csv(path)
        for subtest in subtests:
            test_data = TestData(int(subtest['avg_time']), 
                                 math.floor(int(subtest['max_time']) / int(subtest['total_operations'])))
            file_list[(test, subtest['name'])].append(TestInfo(cpu, author, compiler, test, subtest['name'], test_data))
print(file_list)