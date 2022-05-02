'''
list=['st',32,'fafr',250]
print(list[1:3])
new_list=['fsa','fgh',245]
print(list+new_list)
'''
'''
products=[["iphone",6888],["Macpro",14800],["小米6",2499],["coffe",31],["Book",60],["Nike",699]]
for i in range(len(products)):
    print("%d\t%s\t%d"%(i,products[i][0],products[i][1]))

buy_car=[]
while(1):
    my_input=input("您想要购买什么商品？（请输入商品编号）")
    if (my_input=="q"):
        break
    index=int(my_input)-int("0")

    if(index <=5 and index>=0):
        buy_car.append(products[index])
        print("已成功将%s加入购物车"%products[index][0])


num=0
print("-"*20)
print("您一共选择了以下商品：")
for i in range(len(buy_car)):
    print("%d\t%s\t%d"%(i,buy_car[i][0],buy_car[i][1]))
    num+=buy_car[i][1]

print("您选择的商品总共花费了%d元"%num)
'''

tup=(1,2,3,4,5,6,7,8,9)
print(tup.index(7,3))
