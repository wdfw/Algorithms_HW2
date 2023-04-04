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
def LOMUTO_QUICKSORT(nums, p, r) :
    if r <= p : return
    pivot  = LOMUTO_PARTITION(nums, p, r)
    LOMUTO_QUICKSORT(nums, p, pivot-1)
    LOMUTO_QUICKSORT(nums, pivot+1, r)

def PERF_TEST(epochs,nums,fn,*par) :
    ave = 0
    for epoch in tqdm(range(epochs)) :
        num = nums[:]
        
        beg = time.perf_counter()        
        fn(num, 0, len(num)-1,*par)        
        end = time.perf_counter()        
        
        ave += end - beg
    return ave / epochs

#---------------測試參數----------------------
execution_times = 21 #資料量步數增加的次數
step = 0.2 #資料量步數 以10**step增加
epochs = 100 #測試樣本數 
par_M = [1,5,10,15,20,25] #M的大小
#最大資料量 = 10**(step*(execution_times-1))
#---------------------------------------------


axis_ISS = [[0]*execution_times for i in par_M]#Hoare所需時間
axis_size = [0]*execution_times


for times in range(execution_times) :
    
    size = int(10**(times*step))
    nums = [randint(0,10**6)  for i in range(size)]
    axis_size[times] = size
    for i in range(len(par_M)) :            
        t = PERF_TEST(epochs, nums, ISS_QUICKSORT, par_M[i])
        axis_ISS[i][times] = t
        
#不同M的表現        
for i in range(len(par_M)) : plt.plot(axis_size,axis_ISS[i] ,label = str(par_M[i]))
plt.title("Time Performance")
plt.xlabel('Elements', fontsize="10") # 設定 x 軸標題內容及大小
plt.ylabel('Time(sec)', fontsize="10") # 設定 y 軸標題內容及大小
plt.legend()
plt.show()

#M的表現曲線
axis_ISS_Last = [i[-1] for i in axis_ISS]
plt.plot(par_M,axis_ISS_Last,color="red",label= "Performance Curve with M",marker="o")
plt.xlabel('M', fontsize="10") # 設定 x 軸標題內容及大小
plt.ylabel('Time(sec)', fontsize="10") # 設定 y 軸標題內容及大小
plt.legend()
plt.show()
