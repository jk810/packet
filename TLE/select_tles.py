with open('10000.txt', 'r') as fin:
    lines = [line for line in fin]

fin.close()

nums = [100, 200, 300, 400, 500]
names = [f'{n}.txt' for n in nums]

step = [int(10000/x) for x in nums]

for i, s in enumerate(step):
    with open(names[i], 'w') as fout:
        for x in range(0, 10000, s):
            fout.writelines(lines[2*x])
            fout.writelines(lines[2*x + 1])
