import socket

HOST = "::"  # Standard loopback interface address (localhost) Listens on both IPv4 and IPv6
PORT = 8002  # Port to listen on (non-privileged ports are > 1023)


def send_response(conn: socket.socket, data: bytes, status_code: int):
    response_header = (
        f"HTTP/1.1 {status_code}\r\n"
        f"Content-Length: {len(data.encode())}\r\n"
        f"Server: its-a-webserver\r\n"
        f"\r\n"
    )
    response = response_header.encode() + data.encode()
    conn.send(response)

with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
    print(f"Listing at {HOST}:{PORT}")
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        http_req = data.decode().split("\r\n")
        req_method, path, http_version = http_req[0].split(" ")

        if http_version != "HTTP/1.1":
            send_response(conn=conn, data="", status_code=505)

        if req_method != "GET":
            send_response(conn=conn, data="Sorry we only support GET.", status_code=405)

        to_serve = "index.html" if path == "/" else path[1:]

        try:
            with open(f"./super_cool_website/{to_serve}") as f:
                to_serve = f.read()
        except FileNotFoundError:
            send_response(conn=conn, data="<h1>Page Not Found!</h1>", status_code=404)
    
        send_response(conn=conn, data=to_serve, status_code=200)
        conn.close()
