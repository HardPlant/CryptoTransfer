import server
import client


def get_input(text):
    return input(text)


if __name__ == '__main__':
    server.EchoServer()
    client.Client()