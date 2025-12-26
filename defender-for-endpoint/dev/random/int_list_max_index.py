sample_int_array = [1, 2, 3, 4, 5]
find_max_with_index = lambda num: (max(num), num.index(max(num)))
largest, largest_index = find_max_with_index(sample_int_array)
print(f"The largest value is {largest} and the index is {largest_index}")
largest = max(sample_int_array)
largest_index = sample_int_array.index(largest)
print(f"The largest value is {largest} and the index is {largest_index}")
def find_max_with_index():
    largest = max(sample_int_array)
    largest_index = sample_int_array.index(largest)
    print(f"The largest value is {largest} and the index is {largest_index}")
find_max_with_index()
max_val, max_idx = sample_int_array[0], 0
for i, num in enumerate(sample_int_array):
    if num > max_val:
        max_val, max_idx = num, i
print(f"The largest value is {max_val} and the index is {max_idx}")
#max(list(enumerate(sample_int_array))
