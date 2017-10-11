import server
import client


def get_input(text):
    return input(text)

if __name__ == '__main__':
    try:
        print("서버 모드로 ECB 모드 대신 CTR 모드를 사용합니까? (Y/N)")
        resp = input()
        if resp == 'Y':
            mode = 'CTR'
        else:
            mode = 'ECB'

        print("메시지를 들을 서버 포트: ")
        server_port = int(input())

        server = server.EchoServer(port=server_port, mode=mode)
        server.start()

        while True:
            print("메시지 모드로 ECB 모드 대신 CTR 모드를 사용합니까? (Y/N)")
            resp = input()
            if resp == 'Y':
                client_mode = 'CTR'
            else:
                client_mode = 'ECB'

            print("메시지를 보낼 서버 주소:")
            client_host = input()
            print("메시지를 보낼 서버 포트:")
            client_port = int(input())

            client = client.Client(host=client_host, port = client_port, mode = client_mode)
            while True:
                print("메시지를 입력하세요. (종료: X)")
                msg = input()
                if msg == 'X':
                    break

                client.send(msg)
                print("메시지를 잘 보냈습니다.")
    finally:
        if server:
            server.stop()



