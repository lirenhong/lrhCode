class Solution:
    # @return a tuple, (index1, index2)
    def twoSum(self, num, target):
        process={}
        for index in range(len(num)):
            if target-num[index] in process:
                return [process[target-num[index]],index]
            process[num[index]]=index

if __name__ == "__main__":
    s = Solution()
    nums = [1,3,1,5,5]
    print s.twoSum(nums, 4)
