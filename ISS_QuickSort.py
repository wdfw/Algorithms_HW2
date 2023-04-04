import time
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from tqdm import tqdm

def SWAP(nums, i, j) :
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
def INSERTION_SORT(nums, p, r) :
    for i in range(p+1,r+1) :
        k = nums[i]
        while nums[i-1] > k and i-1 >= 0:
            nums[i] = nums[i-1]
            i -= 1
        nums[i] = k
def SORT3(nums, p, q, r) :
    A,B,C = nums[p],nums[q],nums[r]
    if A <= B :
        if B <= C : return
        else :
            if A <= C : nums[p],nums[q],nums[r] = A,C,B
            else : nums[p],nums[q],nums[r] = C,A,B
    else :
        if A <= C : nums[p],nums[q],nums[r] = B,A,C
        else :
            if B <= C : nums[p],nums[q],nums[r] = B,C,A
            else : nums[p],nums[q],nums[r] = C,B,A
                
def MEDIAN3_PARTITION(nums, p, r) :
    if r-p+1 >= 3 :
        q = (p+r) // 2
        SORT3(nums, p, q, r)
        SWAP(nums, q, r)
    return LOMUTO_PARTITION(nums, p, r)

def ISS_QUICKSORT(nums, p, r, M = 20) :
    if r - p + 1 >= M :
        q = MEDIAN3_PARTITION(nums, p, r)
        ISS_QUICKSORT(nums, p, q-1,M)
        ISS_QUICKSORT(nums, q+1, r,M)
    else :
        INSERTION_SORT(nums, p, r)
        
def LOMUTO_QUICKSORT(nums, p, r, **dummy) :
    if r <= p : return
    pivot  = LOMUTO_PARTITION(nums, p, r)
    LOMUTO_QUICKSORT(nums, p, pivot-1)
    LOMUTO_QUICKSORT(nums, pivot+1, r)

def PERF_TEST(epochs,size,*function,**keys) : #測試函數 輸入排序函數與其keyword即可

    ave = np.zeros(len(function))

    for epoch in tqdm(range(epochs),desc=str(size)) :
        nums = [ randint(0,10**6) for i in range(size)] #產生隨機資料
        
        for i in range(len(function))  :

            fn = function[i]
            num = nums[:]
            beg = time.perf_counter()        
            fn(num, 0, len(num)-1, **keys)   
            end = time.perf_counter()        
            ave[i] += end - beg
    return ave / epochs 
def Wrap(M) :
    def Sort(nums, p, r) :
        ISS_QUICKSORT(nums, p, r, M=M)
    return Sort
#---------------測試參數----------------------
execution_times = 3 #資料量步數增加的次數
step = 0.2 #資料量步數 以10**step增加
epochs = 100 #測試樣本數 
base = 3
#最大資料量 = 10**(base + step*(execution_times-1))
parM = [12,13] #設定M的大小
#---------------------------------------------
axis_ISS = [[0]*execution_times for i in parM]
axis_LU = [0]*execution_times
axis_size = [0]*execution_times

ISS_fn = [Wrap(i) for i in parM]
for times in range(execution_times) :
    
    size = int(10**(times*step+base))
    #size = 10**4 * times*step
    T = PERF_TEST(epochs, size, LOMUTO_QUICKSORT,*ISS_fn)
    
    axis_LU[times] = T[0]
    for i in range(len(ISS_fn)) : axis_ISS[i][times] = T[i+1]
    axis_size[times] = size
        
    
#不同M的表現        
plt.plot(axis_size,axis_LU ,color = "Red",label = "Lomuto")
for i in range(len(parM)) : plt.plot(axis_size,axis_ISS[i] ,label = "ISS M=%d" %(parM[i]))
plt.title("Time Performance")
plt.xlabel('Elements', fontsize="10") # 設定 x 軸標題內容及大小
plt.ylabel('Time(sec)', fontsize="10") # 設定 y 軸標題內容及大小
plt.legend()
plt.show()

#比較Lomuto與ISS(M = parM[0])的性能
axis_IS = np.array(axis_ISS[0])
axis_LU = np.array(axis_LU)
plt.title("Time Performance")
plt.plot(axis_size, ((axis_LU-axis_IS)/axis_LU)*100  ,color='blue' ,label = "Lomuto Compare tp ISS",marker = 'o')
plt.show()

#M的表現曲線(僅觀察最大值)
axis_ISS_Last = [i[-1] for i in axis_ISS] 
plt.plot(parM,axis_ISS_Last,color="red",label= "Performance Curve with M",marker="o")
plt.xlabel('M', fontsize="10") # 設定 x 軸標題內容及大小
plt.ylabel('Time(sec)', fontsize="10") # 設定 y 軸標題內容及大小
plt.legend()
plt.show()
