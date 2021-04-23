import time


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
    ser_left, ser_mid, ser_right = [], [], []
    for i in range(len(server)):
        price = int(server[i][3]) + int(server[i][4]) * day
        if int(server[i][1]) > int(server[i][2]) * 2:
            value_ = price / int(server[i][1])
            server[i].insert(0, value_)
            ser_left.append(server[i])
        elif int(server[i][1]) * 2 < int(server[i][2]):
            value_ = price / int(server[i][2])
            server[i].insert(0, value_)
            ser_right.append(server[i])
        else:
            value_ = (price / int(server[i][1]) + price / int(server[i][2])) / 2
            server[i].insert(0, value_)
            ser_mid.append(server[i])
    ser_left.sort()  # 左边大
    ser_right.sort()  # 差不多
    ser_mid.sort()  # 右边大
    server = ser_left + ser_mid + ser_right
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
    for i in range(1, len(demand) + 1):
        de_nubs += int(nubs[i + 2])
        do = demand[i]
        for j_ in range(len(do)):
            if do[j_][0] == 'add':
                v_ = vm[do[j_][1].replace(' ', '')]
                core += int(v_[0])
                ram += int(v_[1])
    avg_core_ = int(core / de_nubs)
    avg_ram_ = int(ram / de_nubs)
    return server, vm, demand, day, avg_core_, avg_ram_, nubs, len(ser_left), len(ser_mid)


# 定义服务器操作
class Server:
    def __init__(self, s_, n_):
        self.core = int(s_[2]) / 2
        self.ram = int(s_[3]) / 2
        self.index = [[self.core, self.ram], [self.core, self.ram]]
        self.deployed = {}
        self.n = n_  # 服务器编码

    def get_core(self):
        return self.index[0][0]

    def get_ram(self):
        return self.index[0][1]

    def min_(self):
        A = self.index[0][0] + self.index[0][1]
        B = self.index[1][0] + self.index[1][1]
        if A < B:
            return 0
        else:
            return 1

    def judge1(self, v_):
        if int(v_[2]) == 0:
            A = self.index[0][0] >= int(v_[0]) and self.index[0][1] >= int(v_[1])
            B = self.index[1][0] >= int(v_[0]) and self.index[1][1] >= int(v_[1])
            if not A and not B:
                return False
            else:
                return True
        else:
            return False

    def judge2(self, v_):
        if int(v_[2]) == 1:
            A = self.index[0][0] >= int(v_[0]) / 2 and self.index[0][1] >= int(v_[1]) / 2
            B = self.index[1][0] >= int(v_[0]) / 2 and self.index[1][1] >= int(v_[1]) / 2
            if A and B:
                return True
            else:
                return False
        else:
            return False

    def deploy(self, v_, demand_n):
        if int(v_[2]) == 0:
            loc_ = self.min_()
            for i in range(2):
                if self.index[loc_][0] >= int(v_[0]) and self.index[loc_][1] >= int(v_[1]):
                    self.index[loc_][0] -= int(v_[0])
                    self.index[loc_][1] -= int(v_[1])
                    if loc_ == 0:
                        zm = 'A'
                    else:
                        zm = 'B'
                    self.deployed[demand_n] = [self.n, zm]
                    return True
                if loc_ == 0:
                    loc_ = 1
                else:
                    loc_ = 0
            return False
        else:
            if (self.index[0][0] >= int(v_[0]) / 2 and self.index[0][1] >= int(v_[1]) / 2) and \
                    (self.index[1][0] >= int(v_[0]) / 2 and self.index[1][1] >= int(v_[1]) / 2):
                self.index[0][0] -= int(v_[0]) / 2
                self.index[0][1] -= int(v_[1]) / 2
                self.index[1][0] -= int(v_[0]) / 2
                self.index[1][1] -= int(v_[1]) / 2
                self.deployed[demand_n] = [self.n]
                return True
            else:
                return False


# 找剩余容量最大的服务器
def find_max_volume(index_volume, s_id_):
    core_a = index_volume[0][0]
    core_b = index_volume[1][0]
    ram_a = index_volume[0][1]
    ram_b = index_volume[1][1]
    multiple = 1
    if s_id_ in max_volume:
        max_volume.remove(s_id_)
    if core_a >= avg_core * multiple and ram_a >= avg_ram * multiple:
        max_volume.add(s_id_)
    if core_b >= avg_core * multiple and ram_b >= avg_ram * multiple:
        max_volume.add(s_id_)


# 删除虚拟机
def delete_vms(vms_index):
    info_ = server_vms[int(vms_index)]  # 该编号的虚拟机所放置的服务器位置信息
    vms_name = id_vms[int(vms_index)]  # 该编号的虚拟机名称
    v_ = vms[vms_name]  # 该虚拟机需要的容量
    if len(info_) == 2:  # 单节点情况
        if info_[1] == 'A':
            loc = 0
        else:
            loc = 1
        volume = remain_servers_volume[info_[0]]
        volume[loc][0] += int(v_[0])
        volume[loc][1] += int(v_[1])
        remain_servers_volume[info_[0]] = volume
        find_max_volume(volume, info_[0])
    else:  # 双节点情况
        volume = remain_servers_volume[info_[0]]
        volume[0][0] += int(v_[0]) / 2
        volume[0][1] += int(v_[1]) / 2
        volume[1][0] += int(v_[0]) / 2
        volume[1][1] += int(v_[1]) / 2
        remain_servers_volume[info_[0]] = volume
        find_max_volume(volume, info_[0])


# 选择服务器
def chose_server(v_):
    if max_volume:
        for i in range(len(max_volume)):  # 先循环已有的服务器
            x_ = can_use_servers[0]  # 机型
            s_id_ = list(max_volume)[i]  # 服务器id
            s_ = Server(servers[x_], s_id_)
            s_.index = remain_servers_volume[s_id_]
            if s_.judge1(v_) or s_.judge2(v_):
                type_ = 'old'
                return x_, s_, s_id_, type_
    if int(v_[0]) >= int(v_[1]) * 2:
        can_use = can_use_servers[0:left]
        for i in range(len(can_use)):
            x_ = can_use[i]
            s_ = Server(servers[x_], server_id)
            if s_.judge1(v_) or s_.judge2(v_):
                type_ = 'new'
                return x_, s_, server_id, type_
    if int(v_[0]) * 2 <= int(v_[1]):
        can_use = can_use_servers[left:mid]
        for i in range(len(can_use)):
            x_ = can_use[i]
            s_ = Server(servers[x_], server_id)
            if s_.judge1(v_) or s_.judge2(v_):
                type_ = 'new'
                return x_, s_, server_id, type_
    else:
        can_use = can_use_servers[mid:len(can_use_servers)]
        for i in range(len(can_use)):
            x_ = can_use[i]
            s_ = Server(servers[x_], server_id)
            if s_.judge1(v_) or s_.judge2(v_):
                type_ = 'new'
                return x_, s_, server_id, type_


# 当日服务器购买数量超出限额
def purchase_limit(day_):
    if buy_nubs_all[day_] > max_servers:  # 如果当日购买超出最大值
        more = buy_nubs_all[day_] - max_servers  # 超出的数量
        move_servers = day_used_servers_all[day_][0:more]  # 需要移动的服务器
        day_used_servers_all[day_] = day_used_servers_all[day_][more:more + max_servers]
        buy_nubs_all[day_] = max_servers
        # 前一天
        day_used_servers_all[day_ - 1] = day_used_servers_all[day_ - 1] + move_servers
        buy_nubs_all[day_ - 1] = buy_nubs_all[day_ - 1] + more
        purchase_limit(day_ - 1)


# 邻域搜索， 寻找更便宜的机型
def Field_Search(server_index, volume):
    s_ = Server(servers[total_used_servers[server_index]], server_index)
    primal_volume = s_.index
    used_A = [primal_volume[0][0]-volume[0][0], primal_volume[0][1]-volume[0][1]]
    used_B = [primal_volume[1][0]-volume[1][0], primal_volume[1][1]-volume[1][1]]
    remain_volume = volume[0][0] + volume[0][1] + volume[1][0] + volume[1][1]
    for i in can_use_servers:
        s_ = Server(servers[i], server_index)
        new_volume = s_.index
        a_0 = new_volume[0][0]-used_A[0]
        a_1 = new_volume[0][1]-used_A[1]
        b_0 = new_volume[1][0]-used_B[0]
        b_1 = new_volume[1][1]-used_B[1]
        old_cost = int(servers[total_used_servers[server_index]][4])
        new_cost = int(servers[i][4])
        if a_0 >= 0 and a_1 >= 0 and b_0 >= 0 and b_1 >= 0:
            new_remain_volume = a_0 + a_1 + b_0 + b_1
            if new_remain_volume < remain_volume and new_cost < old_cost:
                print(new_remain_volume-remain_volume)
                remain_servers_volume[server_index] = [[a_0, a_1], [b_0, b_1]]  # 更改容量
                day_ = sid_day[server_index]
                for a in range(len(day_used_servers_all[day_])):
                    if day_used_servers_all[day_][a][1] == server_index:
                        day_used_servers_all[day_][a][0] = i
                total_used_servers[server_index] = i
                return [[a_0, a_1], [b_0, b_1]]
    return False


if __name__ == '__main__':
    t0 = time.time()
    training_path = r'D:\YAN\上海交大\华为软件挑战\training-data\training-2.txt'
    with open(training_path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    servers, vms, total_demands, days, avg_core, avg_ram, digital_nub, left, mid = get_data(data)  # 服务器、虚拟机、需求数据
    max_servers = int(digital_nub[0])  # 每天最大购买量

    '''total_demands = {1: [['add', ' vmPCXA5', ' 264022204'], ['add', ' vmVDAZV', ' 381492167'],
                         ['add', ' vm2ORWH', ' 715382615'], ['add', ' vmKW3HG', ' 958781681'],
                         ['add', ' vm17VF0', ' 27713243'], ['add', ' vmWYJXR', ' 124689621'],
                         ['add', ' vm8YIT2', ' 101253437'], ['add', ' vmICVWV', ' 403601826'],
                         ['add', ' vm7FKND', ' 119864032'], ['add', ' vmV7MQX', ' 939102148'],
                         ['add', ' vm7S1GD', ' 148643139']],
                     2: [['add', ' vmDPUSD', ' 337257839'], ['add', ' vm1OE5E', ' 80438170'],
                         ['add', ' vmXVL5P', ' 298513275'], ['add', ' vm8YIT2', ' 896576493'],
                         ['add', ' vmIXIVZ', ' 32928845'], ['add', ' vm39VCY', ' 381414994'],
                         ['add', ' vm6XKXB', ' 52276313'], ['del', ' 264022204'], ['add', ' vmDR5XY', ' 831738814'],
                         ['del', ' 381492167']]}'''

    # 初始化
    can_use_servers = [q for q in range(len(servers))]  # 可用服务器
    total_used_servers = {}  # 总共已用的服务器,按需求更新  [服务器类型, index]
    remain_servers_volume = {}  # 剩余服务器剩余容量
    day_used_servers_all = {}  # 所有的日使用服务器集合
    buy_nubs_all = {}  # 所有的日购买数
    server_vms = {}  # 需求虚拟机放置的服务器
    id_vms = {}  # 需求编号-虚拟机散列表
    sid_day = {}  # 服务器编号和天的散列表
    max_volume = set()  # 最大容量的虚拟机编号[核数大，内存大)
    total_buy = 0  # 总购买服务器数量
    server_id = 0  # 新增服务器编号
    purchase = 0  # 每日服务器购买限制
    output = {}  # 输出

    # 天需求循环
    for j in range(1, len(total_demands) + 1):
        day_output = []  # 当日输出
        demands = total_demands[j]
        # 购买第一台服务器
        day_used_servers = []  # 日使用的服务器。按天更新
        # 解决当第一个需求是del的情况
        while demands[0][0] == 'del':
            delete_vms(demands[0][1])  # 删除
            demands.pop(0)
        # 第一个需求
        x, s, s_id, tp = chose_server(vms[demands[0][1].replace(' ', '')])
        if tp == 'new':
            server_id += 1
        # 需求循环
        for y in range(len(demands)):
            d = demands[y]
            if d[0] == 'add':  # 添加虚拟机
                if y != 0 and demands[y - 1][0] == 'del':  # 如果前一个是del则重选
                    x, s, s_id, tp = chose_server(vms[demands[0][1].replace(' ', '')])
                    if tp == 'new':
                        server_id += 1
                v = vms[d[1].replace(' ', '')]  # 该需求的虚拟机信息[核数, 内存, 节点类型]
                demand_id = int(d[2])  # 需求对应的id
                id_vms[demand_id] = d[1].replace(' ', '')  # 维护id-虚拟机散列表
                judge = s.deploy(v, demand_id)  # 判断是否放得下
                '''print(s.index)'''
                if judge is False:  # 虚拟机装不进服务器
                    remain_servers_volume[s_id] = s.index
                    sid_day[s_id] = j
                    find_max_volume(s.index, s_id)
                    server_vms.update(s.deployed)
                    if tp == 'new':
                        day_used_servers.append([x, s_id])
                        total_used_servers[s_id] = x  # 添加机型和编号
                    x, s, s_id, tp = chose_server(v)
                    if tp == 'new':
                        server_id += 1
                    s.deploy(v, demand_id)
                    '''print(s.index)'''
                if y == len(demands) - 1 or demands[y + 1][0] == 'del':  # 最后一个或者倒数第二个后遇到del
                    remain_servers_volume[s_id] = s.index
                    sid_day[s_id] = j
                    find_max_volume(s.index, s_id)
                    '''print(s.deployed)'''
                    server_vms.update(s.deployed)
                    if tp == 'new':
                        day_used_servers.append([x, s_id])
                        total_used_servers[s_id] = x
            elif d[0] == 'del':  # 删除虚拟机
                delete_vms(d[1])

        day_used_servers_all[j] = day_used_servers
        buy_nubs = len(day_used_servers)  # 当天需购买的服务器数量
        buy_nubs_all[j] = buy_nubs
        purchase_limit(j)
        if buy_nubs_all[j] > 100:
            purchase += 1
        total_buy += buy_nubs
        print('----第{}天-----'.format(j))
        print(len(max_volume))
        # print('天服务器：', day_used_servers)
        # print('服务器剩余容量：', used_servers_volume)
        # print('最大剩余容量的服务器：', max_volume)
        # print('服务器中的虚拟机：', server_vms)
        # print('编号-虚拟机：', id_vms)
        # print('---output---')
        # print(buy_nubs_all[j])
        # print(len(day_used_servers_all[j]))
        for y in range(len(demands)):
            if demands[y][0] == 'add':
                info = server_vms[int(demands[y][2])]
                if len(info) == 2:
                    day_output.append('({}, {})'.format(info[0], info[1]))
                    # print('({}, {})'.format(info[0], info[1]))
                else:
                    day_output.append('({})'.format(info[0]))
                    # print('({})'.format(info[0]))
        output[j] = day_output

    # 邻域搜索
    change = 0
    stop = 1
    while stop != 0:
        k_ch = 0
        for key, value in remain_servers_volume.items():
            if Field_Search(key, value):
                change += 1
                k_ch += 1
        if k_ch > 0:
            stop = 1
        else:
            stop = 0

    # 输出
    # print(day_used_servers_all)
    # print(buy_nubs_all)
    for o in range(1, len(output) + 1):
        print('---第{}天'.format(o))
        print('(purchase, {})'.format(buy_nubs_all[o]))
        for x in range(buy_nubs_all[o]):
            print('({}, 1)'.format(servers[day_used_servers_all[o][x][0]][1]))
        print('(migration, 0)')
        demand_op = output[o]
        for p in demand_op:
            print(p)
    # print('总服务器：', total_used_servers)
    # print('总服务器数量：', len(total_used_servers))
    print('改变机型：', change)
    print('总购买数：', total_buy)
    print('服务器剩余容量：', remain_servers_volume)
    print('最大剩余容量的服务器：', max_volume)
    print('超出购买限制：', purchase)
    print('平均：({}, {})'.format(avg_core, avg_ram))
    t1 = time.time()
    print('运行时间：{}'.format(t1 - t0))
