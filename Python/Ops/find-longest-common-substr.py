
# used following functino to find longest common substring. This is to confirm if received Azure email is part of earlier alert.
def longestComSubstr(str1: str, str2: str) -> int:
    m, n = len(str1), len(str2)
    # initlize a 2D array for DP
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m+1):
        for j in range(1,n+1):
            # if match, add 1 to the previous value
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = 0
    print(dp)
    return dp[m][n]

# if we use a temp arr to store the previous dp[i-1][j-1], we can reduce the space complexity to O(n)
# NOTE lenth fo the str matters, we shall always initialize the array with the longer string.
def longestComSubstr1D(str1: str, str2: str) -> int:
    longstr, shortstr = (str1, str2) if len(str1) > len(str2) else (str2, str1)
    m, n = len(longstr), len(shortstr)
    # initlize a 1D array for DP
    dp = [0] * (m + 1)

    for i in range(1, n+1):
        temp = [0] * (m + 1)
        for j in range(1,m+1):
            # if match, add 1 to the previous value
            if longstr[j-1] == shortstr[i-1]:
                temp[j] = dp[j-1] + 1
            else:
                temp[j] = 0
        dp = temp
    return dp[m]

# test case
str1 = "abcde"
str2 = "ababcde"
print(longestComSubstr1D(str1, str2))