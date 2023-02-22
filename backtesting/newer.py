file2 = open('picks/mfi_topix_2023-02-21.txt','a+')
file1 = open('picks/mfi_topix_2023-02-20.txt','a+')


file2.seek(0)
file1.seek(0)


new=file2.read().splitlines()
old=file1.read().splitlines()

file2.close()
file1.close()
for x in new:
    if x not in old:
        print(x)


