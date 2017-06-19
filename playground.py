import os
from os.path import isfile, join
import re

path = 'C:\\Users\\Samvel.Kocharyan\\Desktop\\reg_files'
files = [f for f in os.listdir(path) if isfile(join(path, f))]
nums = [re.findall('(\d{1,2}_\d{1,2}).xls', f)[0].split('_') for f in files]

for i in range(len(nums)):
    if (i < len(nums) - 1):
        n1, n1_next = (int(nums[i][0]), int(nums[i + 1][0]))
        n2, n2_next = (int(nums[i][1]), int(nums[i + 1][1]))
        if n1 == n1_next and n2_next!=n2+1:
            print(nums[i])
