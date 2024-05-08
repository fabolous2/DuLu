#!/usr/bin/python3
import socket,struct


def loop_on_socket(s):
  while True:
    d, ctl, flg, addr = s.recvmsg(1500, 1024)
    # ctl contains the destination address information
    s.sendmsg(["ECHO: ".encode("utf8"),d], ctl, 0, addr)

if __name__ == "__main__":
   HOST, PORT = "0.0.0.0", 8000
   s = socket.socket(type=socket.SocketKind.SOCK_DGRAM)
   s.setsockopt(0,   # level is 0 (IPPROTO_IP)
                8,   # optname is 8 (IP_PKTINFO)
                1)

   s.bind((HOST, PORT))
   loop_on_socket(s)