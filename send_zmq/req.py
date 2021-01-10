import math
import zmq
import json


class SendZMQRequest:
    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port
        self.tcp_address = f"tcp://{self.host}:{self.port}"
        print(self.tcp_address)

    @staticmethod
    def make_socket():
        cxt = zmq.Context()
        sock = cxt.socket(zmq.REQ)
        sock.setsockopt(zmq.REQ_CORRELATE, True)
        sock.setsockopt(zmq.REQ_RELAXED, True)
        sock.setsockopt(zmq.RCVTIMEO, 1000)
        sock.setsockopt(zmq.SNDTIMEO, 1000)

        return sock

    def make_sub_socket(self):
        cxt = zmq.Context()
        sock = cxt.socket(zmq.SUB)
        sock.connect(self.tcp_address)
        sock.setsockopt(zmq.SUBSCRIBE, ''.encode("utf-8"))
        return sock

    def submit_request(self, os: dict, flags: int = 0):
        sock = self.make_socket()
        sock.connect(self.tcp_address)
        print(f"Submit Request to {self.tcp_address}, flags: {flags}...")
        sock.send_json(os, flags)
        print("Success")
        if flags != zmq.SNDMORE:
            res = sock.recv()
        else:
            res = None

        return res

    def submit_multi_request(self, list_req: list):
        sock = self.make_socket()
        sock.connect(self.tcp_address)
        print(f"Submit multipart request to {self.tcp_address}...")
        sock.send_multipart(list_req)
        print("Success.")
        res = sock.recv()

        return res

    def send_actor_message(self, endpoint: str, command: dict = None):
        os = {
            "Type": "ActorMsg",
            "Endpoint": endpoint
        }

        list_req = [json.dumps(os, indent=2).encode("utf-8"), json.dumps(command, indent=2).encode("utf-8")]
        print(f"Send message to actor, {endpoint}: {list_req}...")
        res = self.submit_multi_request(list_req)
        print(res)

        return res

    def receive_data(self):
        sock = self.make_sub_socket()
        data = json.loads(sock.recv())

        return data

    def set_flw(self, endpoint: str, v: float, l: float, w: float):
        req = {
            'CmdType': 'VW',
            'V': float(v) * 100,
            'L': float(l) * 100,
            'W': round(float(w) * 180 / math.pi, 2)
        }

        return self.send_actor_message(endpoint, req)
