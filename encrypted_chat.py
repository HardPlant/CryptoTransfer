import server
import client


def get_input(text):
    return input(text)

def wait_for_response():
    pass

def try_to_connect():
    return True, host, port

if __name__ == '__main__':
    server = server.EchoServer()
    server.start()
    get_connected = False
    host = ''
    port = 50007
    print("Waiting for connect...")
    print("You can connect with someone or wait for response.")
    print("Want to connect with someone?(Y/N)")
    if(input == 'Y'):
        get_connected, host, port = try_to_connect()

    if get_connected:
        pass
    else:
        host, port = server.get_connector()
    client = client.Client(host= host, port= port)

    while True:
        print()
        text = get_input("Input: ")
        response = client.send(text)
        print(response)
