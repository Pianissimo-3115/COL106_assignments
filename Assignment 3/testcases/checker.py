a = []
b = []
with open("newout.txt", 'r') as f:
    a = f.readlines()
with open("newnewout.txt", 'r') as g:
    b = g.readlines()

# Ensure both files have the same number of lines
if len(a) != len(b):
    print(f"File length mismatch: output.txt has {len(a)} lines, expected_output.txt has {len(b)} lines")
else:
    check=True
    for i in range(len(a)):
        # Strip extra spaces or newlines from both lines before comparing
        if a[i].strip() != b[i].strip():
            check=False
            print(f"At line {i + 1}: '{a[i].strip()}' != '{b[i].strip()}'")
    if check:
        print("All lines mathched!")
