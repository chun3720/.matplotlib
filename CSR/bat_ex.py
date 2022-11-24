
class Solution:
    def reverseStr(self, s: str, k: int) -> str:

        # s = abcdefg , k =2
        # # first 2k character : abcd first reverse -> bacd
        # next 2k character: efg -> feg

        size = len(s)

        dummy = list(s)

        ans = ''


        for j in range(0, size, 2*k):

            i = j+k

            dummy[j:i] = dummy[j:i][::-1] 

            ans + "".join(dummy)

        return ans


soln = Solution()

s = "abcdefg"
k = 2
ans = soln.reverseStr(s, k)

