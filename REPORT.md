Machine: Windows 4Ghz CPU 16GB RAM, SSD
Language: Python
Version : 3.13.1

Pre-guess: comparisons = 2(n*m)

Note: All experiments performed with match_rate = 0.5
n       m       comparisons         wall time (s)       output_tuples
1000    1000    2,000,000           3                   500
2000    2000    8,000,000           11                  1000
4000    4000    32,000,000          42                  2000
8000    8000    128,000,000         167                 4000
16000   16000   512,000,000                             8000
32000   32000   2,048,000,000                           16000
64000   64000   8,192,000,000                           32000

Questions:
Q1. What is the exact relationship between n, m and your comparison count? Does the measured count match the formula exactly? If it does not, explain the discrepancy.
A1. Comparison count is exactly 2nm. It matches the formula exactly. Join performs times(n, m) which is exactly nm comparisons and gives a result of size nm. Select performs nm comparisons on the result of size nm, meaning there are nm + nm or 2nm comparisons total

Q2. Plot time against n on log-log axes. What is the slope, and what does that slope tell you about the algorithm?
A2. ![Graph](./tests/graph.png)

The relationship is between n and t is roughly linear on log-log axes with a slope of about 2. This indicates the execution times grows roughly quadratically with respect to n or O(n^2). This makes sense given the comparison count scales quadratically with n as well, meaning comparison count and time are related and grow at similar rates with respect to n

Q3. Measure select and project at the same sizes. How do those curves differ from the join, and why?
A3. 

Q4. Using your measurements, predict how long the join would take with one million tuples on each side. Show the arithmetic. Do not run it.
A4. n = 1,000,000
    m = 1,000,000
    comparisons = 2nm = 2 * 1,000,000 * 1,000,000 = 2,000,000,000,000
    t ≈ comparisons / 1,000,000 * 

Q5. Does changing the match rate change the comparison count? Does it change the wall time? Explain why those two answers differ.
A5. Changing match rate does not change comparison count. Times is unaffected in comparisons and time by match rate as it does not care about values, just amount of tuples per relation. Select is unaffected in comparisons by match rate as it always does one comparison per tuple regardless of result. Select is technically affected in time by match rate, as a higher match rate means more tuples have to be appended and stored to result rather than skipped, although this difference is almost nothing in comparison to the time due to comparisons.

Q6. In one paragraph, describe what you would have to change to make the million-tuple join feasible. You do not have to implement it.
A6. The main change necessary to make million-tuple join feasible in altering the functionality so that comparisons < O(n^2). Currently, comparisons scale quadratically with n, making joins infeasible for large n. One idea for how to implement this could be some sort of hash, where tuples are placed intoa has table based on join attribute, allowing matching tuples to be found without comparing every pair to every pair, ideally reducing complexity to O(n + m) making it much more feasible for million tuple joins