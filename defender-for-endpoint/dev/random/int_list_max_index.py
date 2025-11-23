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
