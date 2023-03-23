#!/bin/bash
import sys
import math


def read_util_ok():
    while input() != "OK":
        pass


def read_data():
    L = []
    data = sys.stdin.readline()
    while data != "OK":
        L.append(data)
        data = sys.stdin.readline()
    return L


def finish():
    sys.stdout.write('OK\n')
    sys.stdout.flush()


def create_orders(robots_task):
    # [robot_id, 朝向, x, y, goal_workbench_xy[x,y], 'sell']
    '''
        1. 计算旋转角度，正值逆时针旋转
        2. 计算距离
        3. 计算该指令需要执行多少个周期才能达到目标（因只能给机器人设置速度）
    '''
    orders = []
    for task in robots_task:
        x_robot, y_robot, x_bench, y_bench = task[2], task[3], 0, 0
        for i in range(len(task[4])-1):
            # sys.stderr.write( str(task[4][i]) +'  i=' + str(i) + '\n')
            x_bench = task[4][i]
            y_bench = task[4][i+1]
        # sys.stderr.write(str(y_bench)+'\n')
        angle = math.atan2(y_robot-y_bench, x_robot-x_bench)
        if angle > 0:
            angle_speed = math.pi
        else:
            angle_speed = -math.pi
        distance = ((x_robot-x_bench)**2+(y_robot-y_bench)**2)**0.5
        # sys.stderr.write('distance='+str(distance)+'\n')
        FPS1 = int(abs(angle/math.pi)*50)  # 以最大速度旋转需要的帧数
        FPS2 = int(distance/6*50)  # 以最大速度移动需要的帧数
        # sys.stderr.write('FPS2='+str(FPS2)+'\n')
        orders.append([task[0], FPS1, FPS2, angle_speed, task[5]])
    return orders


if __name__ == '__main__':
    # 读取地图信息，暂时不用，没保存数据
    read_util_ok()
    finish()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        parts = line.split(' ')
        frame_id = int(parts[0])

        K = int(sys.stdin.readline())  # 读取第二行，有K个工作台
        workbenchs = []
        robots = []
        [workbenchs.append(sys.stdin.readline()) for i in range(K)]
        [robots.append(sys.stdin.readline()) for i in range(4)]

        # list_of_workbench=[[类型,x,y,剩余生产时间,原料格,产品格],……]
        list_of_workbench = [i.split(' ') for i in workbenchs]
        # list_of_robot=[[所在工作台ID,携带物品类型int,无用,无用,角速度float,x线速度float,y线速度float,朝向float,x,y],……]
        list_of_robot = [i.split(' ') for i in robots]

        # 数据类型转换
        for workbench in list_of_workbench:
            workbench[0] = int(workbench[0])  # 工作台类型
            workbench[1] = float(workbench[1])  # x坐标
            workbench[2] = float(workbench[2])  # y坐标
            workbench[3] = int(workbench[3])  # 剩余生产时间
            workbench[4] = int(workbench[4])  # 原料格
            workbench[5] = int(workbench[5])  # 产品格 0=无 1=有
        for robot in list_of_robot:
            robot[0] = int(robot[0])  # 工作台ID
            robot[1] = int(robot[1])  # 携带物品类型
            # robot[2] = float(robot[2])
            # robot[3] = float(robot[3])
            # robot[4] = float(robot[4])  # 角速度
            # robot[5] = float(robot[5])  # x线速度
            # robot[6] = float(robot[6])  # y线速度
            robot[7] = float(robot[7])  # 朝向
            robot[8] = float(robot[8])  # x坐标
            robot[9] = float(robot[9])  # y坐标

        read_util_ok()
        # 输入完毕
        # 开始输出：
        '''
            1. go to buy
                1.1 计算: workbench[5]==1 的工作台 与 没携带东西的机器人 的距离
                1.2 移动：空闲机器人去改工作台
                1.3 购买
            2. go to sell
                2.1 以机器人为中心，查找能接收机器人所带物品的工作台
                2.2 移动
                2.3 出售
        '''
        sys.stdout.write('%d\n' % frame_id)

        goal_workbench_xy = []
        # 第一位用来做单次循环的标志位，剩余位添加已被选择的工作台，避免多个机器人去到同一个工作台
        black_workbench_id = [0]
        line_speed, angle_speed = 0.1, 1.5
        robots_task = []

        for robot_id in range(4):
            dis = 50.0**2+50**2
            robot = list_of_robot[robot_id]
            if robot[1] == 0:  # 未携带物品,要去买
                for seq in range(len(list_of_workbench)):
                    workbench = list_of_workbench[seq]
                    # workbench[5]=1表示物品格有东西
                    if not (seq in black_workbench_id) and workbench[5]:
                        if dis > (robot[8]-workbench[1])**2 + (robot[9]-workbench[2])**2:
                            dis = (robot[8]-workbench[1])**2 + \
                                (robot[9]-workbench[2])**2
                            goal_workbench_xy = [workbench[1], workbench[2]]
                            black_workbench_id[0] = seq
                black_workbench_id.append(black_workbench_id[0])
                robots_task.append(
                    [robot_id, robot[7], robot[8], robot[9], goal_workbench_xy, 'buy'])
            else:   # 带有东西robot[1]，要去卖
                if robot[1] == 1:
                    # workbench[0]=4,5,9
                    benchType = [4, 5, 9]
                    benchHolding = 0b1000110000
                elif robot[1] == 2:
                    # workbench[0]=4,6,9
                    benchType = [4, 6, 9]
                    benchHolding = 0b1001010000
                elif robot[1] == 3:
                    # workbench[0]=5,6,9
                    benchType = [5, 6, 9]
                    benchHolding = 0b1001100000
                else:
                    # workbench[0]=7,9
                    benchType = [7, 9]
                    benchHolding = 0b1010000000
                for seq in range(len(list_of_workbench)):
                    workbench = list_of_workbench[seq]
                    if not (seq in black_workbench_id) and workbench[0] in benchType and workbench[4] != benchHolding:
                        if dis > (robot[8]-workbench[1])**2 + (robot[9]-workbench[2])**2:
                            dis = (robot[8]-workbench[1])**2 + \
                                (robot[9]-workbench[2])**2
                            goal_workbench_xy = [workbench[1], workbench[2]]
                            black_workbench_id[0] = seq
                        black_workbench_id.append(black_workbench_id[0])
                        robots_task.append(
                            [robot_id, robot[7], robot[8], robot[9], goal_workbench_xy, 'sell'])

        # for robot_id in range(4):
        #     sys.stdout.write('forward %d %f\n' % (robot_id, line_speed))
        #     sys.stdout.write('rotate %d %f\n' % (robot_id, 0))
        # finish()

        '''控制算法1'''
        # [[robot_id,旋转帧数,移动帧数,角速度,buy/sell],……]
        # orders = create_orders(robots_task)
        # while True:
        #     for i in range(len(orders)):
        #         order = orders[i]
        #         if order[1]:
        #             sys.stdout.write('rotate %d %f\n' % (order[0], order[3]))
        #             sys.stdout.write('forward %d %f\n' % (order[0], 0))
        #             # sys.stderr.write(str(i)+'号order[1]='+str(order[1])+'\n')
        #             order[1] -= 1

        #         elif order[2]:
        #             sys.stdout.write('rotate %d %f\n' % (order[0], 0))
        #             sys.stdout.write('forward %d %f\n' % (order[0], 6))
        #             order[2] -= 1
        #             # sys.stderr.write(str(i)+'号order[2]='+str(order[2])+'\n')
        #         else:
        #             sys.stdout.write('forward %d %f\n' % (order[0], 0))
        #             # sys.stdout.write(order[4]+' %d' % order[0])

        #     if [order[2] for order in orders] == [0, 0, 0, 0]:
        #         sys.stderr.write('break\n')
        #         finish()
        #         break
        #     finish()

        #     line = sys.stdin.readline()
        #     if not line:
        #         break
        #     parts = line.split(' ')
        #     frame_id = int(parts[0])
        #     read_util_ok()
        #     sys.stdout.write('%d\n' % frame_id)

        '''控制算法2'''