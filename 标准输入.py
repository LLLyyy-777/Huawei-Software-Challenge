import sys


def get_data(d_):
    n = -1
    test_dit = [[] for i in range(3)]
    nubs = []
    for line in d_:
        if line == '/n':
            continue
        if line.isdigit():
            n += 1
            nubs.append(line)
            if len(nubs) == 3:
                test_dit += [[] for i in range(int(nubs[-1]))]
            continue
        test_dit[n].append(line[1:len(line)-1].split(','))
    server = test_dit[0]
    day = int(nubs[2])
    for i in range(len(server)):
        price = int(server[i][3]) + int(server[i][4]) * day
        value_ = (price / int(server[i][1]) + price / int(server[i][2])) / 2
        server[i].insert(0, value_)
    server.sort()
    virtual_machine = test_dit[1]
    vm = {}
    for i in range(len(virtual_machine)):
        vm[virtual_machine[i][0]] = virtual_machine[i][1:4]
    demand = {}
    t = 1
    for j_ in range(3, len(nubs)):
        demand[t] = test_dit[j_]
        t += 1
    return server, vm, demand, day


data = []
raw = 1
nubs = 0
day = -10
sk = 0
while True:
    line = sys.stdin.readline().strip()
    data.append(line)
    if line.isdigit():
        nubs += int(line) + 1  # 81 882 884 985
        sk += 1  # 1 2 3 4
        if sk == 3:
            day = int(line)  # 1
    if raw == nubs - day and sk == day + 3:
        break
    raw += 1  # 2..81 82...882 883 884 885
servers, vms, total_demands, days = get_data(data)  # 服务器、虚拟机、需求数据
# print(data[1])
print(total_demands[1])
