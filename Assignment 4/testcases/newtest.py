book_titles = ["book1", "book2"]
texts = [["The", "name", "of", "this", "book", "contains", "a", "number"],
             ["You", "can", "name", "this", "book", "anything"]]

def merge_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr

    def merge(left, right, key):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)

    return merge(left, right, key)

books=merge_sort(list(zip(book_titles,texts)))
for i in range(len(books)):
    books[i]=(books[i][0],merge_sort(books[i][1]))
print(books)
