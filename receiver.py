import asyncio
import socket

async def handle_stream(stream_socket, port):
    print(f"Started handling stream {port}")
    try:
        while True:
            data, _ = stream_socket.recvfrom(1024)
            print(f"Received chunk from stream {port}: {data.decode()}")
            await asyncio.sleep(0.1)  # Optional: add a small delay for better readability
    except Exception as e:
        print(f"Exception occurred in stream {port}: {e}")
    finally:
        print(f"Stopped handling stream {port}")

async def receive_file():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Server address and port
    server_address = ('localhost', 12345)

    # Bind the socket to the server address
    server_socket.bind(server_address)

    try:
        while True:
            # Receive number of streams
            data, _ = server_socket.recvfrom(1024)
            num_streams = int(data.decode().split(':')[1])

            print(f"Received number of streams: {num_streams}")

            # Start a coroutine for each stream
            tasks = []
            for i in range(num_streams):
                port = 54321 + i  # Base port + stream index
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

if __name__ == "__main__":
    asyncio.run(receive_file())
