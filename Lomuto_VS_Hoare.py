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

def PERF_TEST(epochs,size,*function,**keys) : #測試函數 輸入排序函數與其keyword即可
    global call 
    ave = np.zeros(len(function))
    calls = np.zeros(len(function))
    for epoch in tqdm(range(epochs),desc=str(size)) :
        nums = [ randint(0,10**6) for i in range(size)] #產生隨機資料
        #randint(0,10**6)
        for i in range(len(function))  :
            call = 0
            fn = function[i]
            num = nums[:]
        
            beg = time.perf_counter()        
            fn(num, 0, len(num)-1, **keys)   
            
            end = time.perf_counter()        

            ave[i] += end - beg
            calls[i] += call
    
    return ave / epochs , calls/epochs

#---------------測試參數----------------------
execution_times = 6 #資料量步數增加的次數
step = 0.2 #資料量步數 以10**step增加
epochs = 100 #測試樣本數 
base = 3
#最大資料量 = 10**(base + step*(execution_times-1))
#---------------------------------------------

axis_Lomuto = [] #Lomuto所需時間
axis_Hoare = [] #Hoare所需時間

axis_Lomuto_Call = [] #Lomuto交換次數
axis_Hoare_Call = [] #Hoare交換次數
axis_size = [] #資料大小軸

for times in range(execution_times) :
    size = int(10**(times*step+base)) #資料大小
    
    T,C = PERF_TEST(epochs, size, HOARE_QUICKSORT, LOMUTO_QUICKSORT)
    axis_Lomuto.append(T[1])
    axis_Lomuto_Call.append(C[1])
    axis_Hoare.append(T[0])
    axis_Hoare_Call.append(C[[0]])
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
