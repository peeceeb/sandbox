def twoSum(numbers, target):
# Left pointer starts from the beginning.
    left = 0
# Right pointer starts from the end.
    right = len(numbers) - 1
# Continue until the two pointers meet.
    while left < right:
# Calculate the sum of the two numbers.
        current_sum = numbers[left] + numbers[right]
# If we've found the target,
        # return 1-based indices.
        if current_sum == target:
            return [left + 1, right + 1]
# If the sum is too small,
        # move the left pointer to a larger number.
        elif current_sum < target:
            left += 1
# Otherwise, the sum is too large,
        # so move the right pointer to a smaller number.
        else:
            right -= 1

print(twoSum([2, 7, 11, 15], 18))
