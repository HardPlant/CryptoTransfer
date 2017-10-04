import server
import client


def get_input(text):
    return input(text)

if __name__ == '__main__':
    server = server.EchoServer()
    server.start()
    client = client.Client()

    while True:
        print()
        text = get_input("Input: ")
        response = client.send(text)
        print(response)
