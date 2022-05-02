# for i in "sdffgsa":
#     print(i,end='\t')
# a=['a','b','c']
# for i in a:
#     print(i,end="  ")
# print("\n")
# for i in range(len(a)):
#     print(a[i])

# i=0
# num=0
# while i<=100:
#  num+=i
#  i+=1
#
# print(num)


#
# for i in range(1,10):
#     for j in range(1,i+1):
#         print("%d*%d=%d"%(j,i,i*j),end='\t')
#     print('\n')

i=1
while i<10:
    j=1
    while j<(i+1):
        print("%d*%d=%d"%(j,i,i*j),end='\t')
        j+=1
    i+=1
    print("\n")
