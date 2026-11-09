"""Inicia la API sin detener procesos ajenos si el puerto está ocupado."""
import argparse
import errno
import socket
import uvicorn

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("El puerto debe estar entre 0 y 65535")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        try:
            listener.bind((args.host, args.port))
        except OSError as exc:
            if exc.errno not in {errno.EADDRINUSE, 10048}:
                raise
            print(f"El puerto HTTP {args.port} está ocupado; se elegirá uno libre.", flush=True)
            listener.bind((args.host, 0))
        listener.listen(128)
        port = listener.getsockname()[1]
        print(f"Swagger: http://{args.host}:{port}/docs", flush=True)
        config = uvicorn.Config("app.main:app", host=args.host, port=port)
        uvicorn.Server(config).run(sockets=[listener])

if __name__ == "__main__":
    main()
