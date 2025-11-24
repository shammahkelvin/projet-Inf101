def selection_sort(arr):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[j] < arr[i]:
                arr[i], arr[j] = arr[j], arr[i]
    return arr


print(selection_sort([64, 25, 12, 22, 11]))  # Output should be [11, 12, 22, 25, 64]