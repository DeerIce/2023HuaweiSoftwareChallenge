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

        read_util_ok()
        # 输入完毕
        # 开始输出：
        '''
            1.
        '''
        sys.stdout.write('%d\n' % frame_id)
        line_speed, angle_speed = 0.1, 1.5
        for robot_id in range(4):
            sys.stdout.write('forward %d %f\n' % (robot_id, line_speed))
            sys.stdout.write('rotate %d %f\n' % (robot_id, 0))
        finish()

