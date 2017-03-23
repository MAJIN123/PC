#!/usr/bin/env python
# -*- coding: utf-8 -*-

' ping'

__author__ = 'Maloney'

import os
import socket
import struct #处理二进制数据
import select # 监听是否有可读、可写或异常事件产生
import time
import argparse

ICMP_ECHO_REQUEST = 8
# ICMP报文类型
DEFAULT_TIMEOUT = 2 # 默认超时时间
DEFAULT_COUNT = 4 # 默认发送报文的数量
class Pinger(object):
    def __init__(self, target_host, count=DEFAULT_COUNT,
        timeout=DEFAULT_TIMEOUT):
        self.target_host = target_host
        self.count = count
        self.timeout = timeout

    def do_checksum(self, source_string):
        sum = 0
        # 计算校验和
        max_count = (len(source_string)/2)*2
        count = 0
        # 取小于等于len(source_string)最大偶数
        while count < max_count:
            val = ord(source_string[count + 1])*256 +ord(source_string[count])
            sum = sum + val
            sum = sum & 0xffffffff
            count = count + 2
            # ord 返回单字符的ASCII码
            # 累加到sum
            # sum 取后32位
        if max_count<len(source_string):
        # 若len(source_string)为奇数,加上source_string的最后一位
            sum = sum + ord(source_string[len(source_string) - 1])
            sum = sum & 0xffffffff
        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)
        answer = ~sum
        # 将sum的高16位加上低16位
        # 将sum加上sum的高16位
        # 将sum取反
        answer = answer & 0xffff
        # 取answer的低16位
        answer = answer >> 8 | (answer << 8 & 0xff00) # 将answer右移8位与上answer左移8位
        return answer # 返回计算得到的校验和

    def send_ping(self, sock, ID):
        target_addr = socket.gethostbyname(self.target_host) # 获得目的 ip 地址
        my_checksum = 0
        # 初始化校验和为0
        # 将数据按“bbHHh“ 格式打包 b:integer 1B H:unsigned short 2B h:short 2B
        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0,my_checksum, ID, 1)
        bytes_In_double = struct.calcsize('d') # 得到 ’d’ 格式的数据字节数
        data = (100 - bytes_In_double) * 'd' #data 一共 100 字节 发送一些列 ’Q...’
        data = struct.pack('d', time.time()) + data # data 前加上时间
        # 根据header和data计算校验和
        my_checksum = self.do_checksum(header + data)
        header = struct.pack(
        "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1)
        # 打包header 并将校验和由主机字节顺序转为网络字节顺序
        packet = header + data # 将header和data组合成packet
        sock.sendto(packet, (target_addr, 1)) # 向目标地址发送packet

    def receive_ping(self, sock, ID, timeout):
        time_remaining = timeout
        # 设置超时时间
        while True:
            start_time = time.time()
            readable = select.select([sock], [], [], time_remaining)
            # 监听sock是否有数据可读
            time_spent = (time.time() - start_time)
            if readable[0] == []: # 没有可读数据
                return
        time_received = time.time()
        # 记录接收的时间
        recv_packet, addr = sock.recvfrom(1024) # 接收1024个字节数据
        icmp_header = recv_packet[20:28]
        # 前20字节为IP首部 icmp首部一共8个字节 ‘bbHHh’ 1+1+2+2+2=8
        type, code, checksum, packet_ID, sequence = struct.unpack("bbHHh", icmp_header)
        # 从 icmp_header 中解包
        if packet_ID == ID:
            # ID匹配
            bytes_In_double = struct.calcsize("d")
            time_sent = struct.unpack("d", recv_packet[28:28+bytes_In_double])[0]
            # 从 data 中得到发送的时间
            return time_received - time_sent # 返回所用的时间
        time_remaining = time_remaining - time_spent
        if time_remaining <= 0: # 超时返回
            return

    def ping_once(self):
        icmp = socket.getprotobyname("icmp") # 得到协议号
        try:
            # 创建原始套接字
            m_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except socket.error, (errno, msg):
            if errno == 1:
                # 没有权限
                msg += "ICMP messages can only be sent from root user processes"
                print msg
            else:
                print errno
        except Exception, e:
                print "Exception: %s" %(e)
        my_ID = os.getpid() & 0xFFFF
        # 进程id
        self.send_ping(m_sock, my_ID) # 发送报文
        delay = self.receive_ping(m_sock, my_ID, self.timeout) # 接收回应
        m_sock.close()
        return delay

    def ping(self):
        for i in xrange(self.count):
            print "Ping to %s..." % self.target_host,
            try:
                delay = self.ping_once() # 返回延迟时间
            except socket.error, e:
                print "Ping failed. (socket error: '%s')" % e[1]
                break
        if delay == None:
            print "Ping failed. (timeout within %ssec.)" % self.timeout
        else:
            delay = delay * 1000
            print "Get pong in %0.4fms" % delay


if __name__ == '__main__':
    target_host="www.baidu.com" # 目标主机
    pinger = Pinger(target_host=target_host) #创建Ping对象
    pinger.ping() # 调用ping方法

