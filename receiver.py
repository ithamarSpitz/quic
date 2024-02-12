import asyncio
import socket

async def handle_stream(stream_socket, port):
    print(f"Started handling stream {port}")
    try:
        while True:
            data, _ = stream_socket.recvfrom(1024)
            message = data.decode()
            print(f"Received chunk from stream {port}: {message}")
            if message == "EXIT":
                print(f"Received exit signal from stream {port}. Stopping...")
                break
            await asyncio.sleep(0)  
    except Exception as e:
        print(f"Exception occurred in stream {port}: {e}")
    finally:
        print(f"Stopped handling stream {port}")
        stream_socket.close()

async def receive_file():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Server address and port
    server_address = ('localhost', 12345)

    # Bind the socket to the server address
    server_socket.bind(server_address)
    num_streams = 0
    try:
        while True:
            # Receive number of streams
            data, _ = server_socket.recvfrom(1024)
            msg = data.decode()
            print(msg)
            if msg == "CLOSE":
                break
            num_streams = int(msg.split(':')[1])

            print(f"Received number of streams: {num_streams}")
            if num_streams>20:
                break
            ports = []
            for i in range(num_streams):
                data, _ = server_socket.recvfrom(1024)
                print(data.decode())
                port_num = int(data.decode().split(':')[1])
                ports = ports + [port_num]

            # Start a coroutine for each stream
            tasks = []
            for i in range(num_streams):
                port = ports[i]  # Base port + stream index
                print(f"num streams is: {num_streams}")
                print(f"Creating task for stream {port}")
                stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                stream_socket.bind(('localhost', port))
                print(f"Bound stream socket to port {port}")
                task = asyncio.create_task(handle_stream(stream_socket, port))
                tasks.append(task)

            await asyncio.gather(*tasks)

    finally:
        # Close socket
        server_socket.close()
        print(num_streams)

if __name__ == "__main__":
    asyncio.run(receive_file())
