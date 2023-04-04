import time
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from tqdm import tqdm

call = 0
def SWAP(nums, i, j) :
    global call
    call += 1
    nums[i],nums[j] = nums[j],nums[i]

def LOMUTO_PARTITION(nums, p, r) :
    x = nums[r]
    i = p-1
    for j in range(p,r) :
        if nums[j] <= x : 
            i += 1
            SWAP(nums, i, j)
    SWAP(nums, i+1, r)
    return i+1

def HOARE_PARTITION(nums, p, r) :
    x = nums[p]
    i = p - 1
    j = r + 1
    while True :
        i = i + 1
        j = j - 1
        while nums[j] > x : j -= 1
        while nums[i] < x : i += 1
        if i >= j : return j
        else : SWAP(nums,i,j) 

def HOARE_QUICKSORT(nums, p, r) :
    if r <= p : return
    pivot = HOARE_PARTITION(nums, p, r)
    HOARE_QUICKSORT(nums, p, pivot) 
    HOARE_QUICKSORT(nums, pivot+1, r)

def LOMUTO_QUICKSORT(nums, p, r) :
    if r <= p : return
    pivot  = LOMUTO_PARTITION(nums, p, r)
    LOMUTO_QUICKSORT(nums, p, pivot-1)
    LOMUTO_QUICKSORT(nums, pivot+1, r)

def PERF_TEST(epochs,nums,fn) :
    ave = 0
    global call
    call = 0
    for epoch in tqdm(range(epochs)) :
        num = nums[:]
        
        beg = time.perf_counter()        
        fn(num, 0, len(num)-1)        
        end = time.perf_counter()        
        
        ave += end - beg
    return ave / epochs , call/epochs

#---------------測試參數----------------------
execution_times = 26 #資料量步數增加的次數
step = 0.2 #資料量步數 以10**step增加
epochs = 100 #測試樣本數 
#最大資料量 = 10**(step*(execution_times-1))
#---------------------------------------------

axis_Lomuto = [] #Lomuto所需時間
axis_Hoare = [] #Hoare所需時間

axis_Lomuto_Call = [] #Lomuto交換次數
axis_Hoare_Call = [] #Hoare交換次數

axis_size = [] #資料大小

for times in range(execution_times) :
    size = int(10**(times*step)) #資料大小
    nums = [randint(0,10**6)  for i in range(size)] #產生隨機資料
    #randint(0,10**6)
    
    #HOARE_QUICKSORT測試
    t,c = PERF_TEST(epochs, nums, HOARE_QUICKSORT)
    axis_Hoare.append(t)
    axis_Hoare_Call.append(c)
    
    #LOMUTO_QUICKSORT測試
    t,c = PERF_TEST(epochs, nums, LOMUTO_QUICKSORT)
    axis_Lomuto.append(t)
    axis_Lomuto_Call.append(c)
    
    axis_size.append(size)

#比較執行時間
plt.title("Time Performance")
plt.plot(axis_size,axis_Hoare ,color='blue' ,label = "Hoare")
plt.plot(axis_size,axis_Lomuto ,color='red' ,label = "Lomuto")
plt.xlabel('Elements', fontsize="10") # 設定 x 軸標題內容及大小
plt.ylabel('Time(sec)', fontsize="10") # 設定 y 軸標題內容及大小
plt.legend()
plt.show()

#比較交換次數
plt.title("Call Swap")
plt.plot(axis_size,axis_Hoare_Call ,color='blue' ,label = "Hoare")
plt.plot(axis_size,axis_Lomuto_Call ,color='red' ,label = "Lomuto")
plt.xlabel('Elements', fontsize="10") # 設定 x 軸標題內容及大小
plt.ylabel('Swap Times', fontsize="10") # 設定 y 軸標題內容及大小
plt.legend()
plt.show()
