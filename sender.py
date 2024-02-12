import asyncio
import socket

async def send_data(stream_socket, file_path, port):
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(1024)
            if not chunk:
                break
            stream_socket.sendto(chunk, ('localhost', port))
            await asyncio.sleep(0)  # Allow other tasks to run

async def send_file(file_path, num_streams):
    # Create UDP socket for sending the number of streams
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Server address and port
    server_address = ('localhost', 12345)

    try:
        # Send number of streams
        client_socket.sendto(f"NUM_STREAMS:{num_streams}".encode(), server_address)

        # Start a coroutine for each stream and send file data
        coroutines = []
        for i in range(num_streams):
            stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            port = 54321 + i  # Base port + stream index
            client_socket.sendto(f"STREAM_PORT:{port}".encode(), server_address)  # Notify receiver of port
            coroutine = send_data(stream_socket, file_path, port)
            coroutines.append(coroutine)

        await asyncio.gather(*coroutines)

    finally:
        # Close socket
        client_socket.close()

if __name__ == "__main__":
    file_path = 'example.txt'
    num_streams = 3  # Number of streams to use
    asyncio.run(send_file(file_path, num_streams))
