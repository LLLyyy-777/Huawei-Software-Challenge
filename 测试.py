# 获取数据
def get_data(d_):
    n = -1
    test_dit = [[] for i in range(3)]
    nubs = []
    core, ram = 0, 0
    de_nubs = 0
    for line in d_:
        if line == '/n':
            continue
        if line.strip().isdigit():
            n += 1
            nubs.append(line.strip())
            if len(nubs) == 3:
                test_dit += [[] for i in range(int(nubs[-1]))]
            continue
        test_dit[n].append(line[1:len(line) - 2].split(','))
    server = test_dit[0]
    day = int(nubs[2])
    for i in range(len(server)):
        value_ = int(server[i][3])
        server[i].insert(0, value_)
    server.sort()
    server = server[::-1]
    virtual_machine = test_dit[1]
    vm = {}
    for i in range(len(virtual_machine)):
        vm[virtual_machine[i][0]] = virtual_machine[i][1:4]
    demand = {}
    t = 1
    for j_ in range(3, len(nubs)):
        demand[t] = test_dit[j_]
        t += 1
    # 计算平均数
    for i in range(1, len(demand)+1):
        de_nubs += int(nubs[i+2])
        do = demand[i]
        for j in range(len(do)):
            if do[j][0] == 'add':
                v_ = vm[do[j][1].replace(' ', '')]
                core += int(v_[0])
                ram += int(v_[1])
    avg_core_ = int(core/de_nubs)
    avg_ram_ = int(ram/de_nubs)
    return server, vm, demand, day, avg_core_, avg_ram_, nubs


if __name__ == '__main__':
    training_path = r'D:\YAN\上海交大\华为软件挑战\training-data\training-2.txt'
    with open(training_path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    servers, vms, total_demands, days, avg_core, avg_ram, digital_nub = get_data(data)  # 服务器、虚拟机、需求数据
    print(servers)
    '''core, ram, n = 0, 0, 0
    for i in range(1, len(total_demands)+1):
        demands = total_demands[i]
        for j in range(len(demands)):
            d = demands[j]
            if d[0] == 'add':  # 添加虚拟机
                v = vms[d[1].replace(' ', '')]  # 该需求的虚拟机信息[核数, 内存, 节点类型]
                core += int(v[0])
                ram += int(v[1])
                n += 1
    avg_core = core/n
    avg_ram = ram/n
    print('平均核数', avg_core)
    print('平均内存', avg_ram)'''