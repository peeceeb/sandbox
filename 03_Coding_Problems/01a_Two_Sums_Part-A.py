def twoSum(nums, target):
# Dictionary to store:
    # number -> index
    seen = {}
# Traverse the array once.
    for index, number in enumerate(nums):
# Calculate the value needed to reach the target.
        complement = target - number
# If we've already seen the complement,
        # we've found the required pair.
        if complement in seen:
            print(f"Indices of the two numbers that add up to {target}: [{seen[complement]}, {index}]")
# Store the current number and its index.
        seen[number] = index


nums=[3,2,9,23,12]
target=15
result = twoSum(nums, target)

