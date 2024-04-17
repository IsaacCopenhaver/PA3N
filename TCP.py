from socket import *
import time
import random

def simulate_packet_transmission(probability_loss):
    return random.random() > probability_loss

def sim(congestion_algorithm):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(("localhost", 12350))

    packets_sent = 0
    packets_received = 0
    good_packets_received = 0
    cwnd = 1
    threshold = 16

    start_time = time.time()

    while time.time() - start_time < 10:
        if congestion_algorithm == "tahoe":
            if simulate_packet_transmission(0.2):
                packets_sent += 1
                sock.sendall(b"Hello, world!")

                data = sock.recv(1024)
                if data:
                    packets_received += 1
                    good_packets_received += 1

                if packets_received == cwnd:
                    cwnd *= 2

            time.sleep(0.01)

        if congestion_algorithm == "reno":
            if simulate_packet_transmission(0.1):
                packets_sent += 1
                sock.sendall(b"test")

                data = sock.recv(1024)
                if data:
                    packets_received += 1
                    good_packets_received += 1

                if packets_received >= cwnd:
                    if cwnd < threshold:
                        cwnd *= 2
                    else:
                        cwnd += 1
            time.sleep(0.01)

    end_time = time.time()
    throughput = packets_received / (end_time - start_time)
    goodput = good_packets_received / packets_sent if packets_sent > 0 else 0

    sock.close()
    return packets_sent, packets_received, good_packets_received, throughput, goodput

def main():
    tahoe = sim("tahoe")
    reno = sim("reno")

    print("TCP Tahoe:\nPackets Sent:", tahoe[0])
    print("\nPackets Sent:", tahoe[0])
    print("\nPackets Received:", tahoe[1])
    print("\nGood Packets Received:", tahoe[2])
    print("\nThroughput:", tahoe[3], "packets per second")
    print("\nGoodput:", tahoe[4])

    print("\nTCP Reno:")
    print("\nPackets Sent:", reno[0])
    print("\nPackets Received:", reno[1])
    print("\nGood Packets Received:", reno[2])
    print("\nThroughput:", reno[3], "packets per second")
    print("\nGoodput:", reno[4])

if __name__ == "__main__":
    main()
