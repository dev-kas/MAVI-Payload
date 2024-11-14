import fcntl
import os
import struct
import subprocess
import sys
import termios
import socketio
from info import get_info
import pty
import config
# from autoupdater import check_for_updates, perform_update

print('Program started.')

socket = socketio.Client(logger=True, reconnection_attempts=9999999, reconnection=True, reconnection_delay=5, reconnection_delay_max=50)
info = get_info()
ptys = {}

@socket.event
def connect():
    print(f"connected as {socket.sid}")
    socket.emit("verifyIdentity", info)

@socket.event
def writeToPTY(data):
    thisPTY = ptys[data["ptyID"]]
    os.write(thisPTY["master_fd"], data["data"])


@socket.event
def spawnPTY(data):
    id = data["id"]
    shell = data["shell"] if data["shell"] is not None else os.getenv("COMSPEC") if info["os"] == "Windows" else os.getenv("SHELL")
    rows = data["rows"] if data["rows"] is not None else 24
    cols = data["cols"] if data["cols"] is not None else 80
    print("spawnning PTY for " + id, f"{shell=}", f"{rows}x{cols}")

    master_fd, slave_fd = pty.openpty()

    proc = subprocess.Popen(
        args=[shell],
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        env=os.environ,
        close_fds=True,
        shell=True,
    )

    winsize = struct.pack('HHHH', rows, cols, 0, 0)
    fcntl.ioctl(master_fd, termios.TIOCSWINSZ, winsize)

    os.close(slave_fd)
    ptys[id] = {}
    ptys[id]["proc"] = proc
    ptys[id]["master_fd"] = master_fd

    try:
        while True:
            output = os.read(master_fd, 1024)
            if not output:
                break
            sys.stdout.buffer.write(output)
            sys.stdout.flush()
            socket.emit("PTYdata", {"ptyID": id, "data": output.decode("utf-8")})
    except KeyboardInterrupt:
        proc.terminate()
    finally:
        os.close(master_fd)
        proc.wait()
        killPTY(id)

@socket.event
def disconnect():
    print("disconnected")
    for ptyID in ptys:
        killPTY(ptyID)

@socket.event
def killPTY(ptyID):
    ptys[ptyID]["proc"].terminate()
    del ptys[ptyID]



def main():
    try:
        socket.connect(url=config.SERVER_URL, namespaces="/", transports=["websocket"], headers={ "type": "host" })
        socket.wait()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
    # check_for_updates()
