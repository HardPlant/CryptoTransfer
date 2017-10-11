# -*- coding: utf-8 -*-
#
# Python Ping Sweep GUI Program
#


import wx
import sys
import socket
import traceback

from time import gmtime, strftime

import client
import server

#
# pingScan Button Handler
#
def pingScan(event):
    if hostEnd.GetValue() < hostStart.GetValue():
        # Invalid Setting
        # 대화상자를 띄워 사용자에게 알린다.
        dlg = wx.MessageDialog(mainWin, "잘못된 호스트 선택입니다."
                               , "확인", wx.OK | wx.ICON_EXCLAMATION)
        result = dlg.ShowModal()
        dlg.Destroy()
        return

    # 유효한 범위가 있는 경우 상태 표시줄 갱신
    mainWin.StatusBar.SetStatusText("Ping Sweep 실행 중...")

    # 시작 시간 기록, 결과 창 갱신
    utcStart = gmtime()
    utc = strftime("%a, %d %b %Y %X +0000", utcStart)
    results.AppendText("\n\nPing Sweep Started: "+ utc+ "\n\n")

    # GUI에서 설정된 baseIP 기준으로 ip 범위를 만듬
    baseIP = str(serverPort.GetValue()) + '.'  \
             + str(clientPort.GetValue()) + '.'\

    ipRange = []

    for i in range(hostStart.GetValue(), (hostEnd.GetValue()+1)):
        ipRange.append(baseIP+str(i))

    for ipAddress in ipRange:
        try:
            # 상태 표시줄 갱신
            mainWin.StatusBar.SetStatusText('Pinging IP:' + ipAddress)

            delay = ping.do_one(ipAddress, timeout=2)

            results.AppendText(ipAddress+'\t')

            if delay != None:
                # 성공한 경우 결과와 응답시간 표시
                results.AppendText('Response Success')
                results.AppendText('Response Time:'+str(delay)+' Seconds')
                results.AppendText('\n')
            else:
                # 지연이 없는 경우 요청이 시간 초과함
                results.AppendText('Response Timeout')
                results.AppendText('\n')

        except socket.error as e:
            # 소켓 오류 정보 + 잘못된 아이디 표시
            results.AppendText(ipAddress)
            results.AppendText(' Response Failed: ')
            results.AppendText(e)
            traceback.print_exc()
            results.AppendText('\n')

        # 모든 주소 처리 후 종료 시간 기록, 표시
    utcEnd = gmtime()
    utc = strftime("%a, %d %b %Y %X +0000", utcEnd)
    results.AppendText("\nPing Sweep Ended: " + utc + '\n\n')

    # 상태 표시바 정리
    mainWin.StatusBar.SetStatusText('')

    return

def programExit(event):
    sys.exit()

def sendChat(event):
    pass
#
# Setting Window
#
class RedirectText:
    def __init__(self,textCtrl):
        self.out = textCtrl

    def write(self, string):
        self.out.WriteText(string)



class Frame(wx.Frame):
    def startServer(self, event):
        if self.rdoServerECB.GetValue() == True:
            mode = 'ECB'
        else:
            mode = 'CTR'
        self.server = server.EchoServer(host=self.serverHostText.GetValue(),
                                        port=int(self.serverPort.GetValue()),
                                        mode=mode)
        self.serverStartButton.Disable()
        self.serverExitButton.Enable()
        return


    def stopServer(self, event):
        self.server.stop()
        self.serverStartButton.Enable()
        self.serverExitButton.Disable()

    def startClient(self, event):
        if self.rdoClientECB.GetValue() == True:
            mode = 'ECB'
        else:
            mode = 'CTR'

        self.client = client.Client(host=self.ClientHostText.GetValue(),
                                        port=int(self.clientPort.GetValue()),
                                        mode=mode)
        self.clientStartButton.Disable()
        self.clientResetButton.Enable()
        self.clientChatConfirm.Enable()

    def sendMessage(self, event):
        self.client.send(self.clientChatText.GetValue())
        self.clientChatText.SetValue('')

    def stopClient(self, event):
        self.client = None
        self.clientStartButton.Enable()
        self.clientResetButton.Disable()
        self.clientChatConfirm.Disable()

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="LEA 통신")
        self.SetSize(1000,600)
        self.mainPanel = wx.Panel(self)

        # 액션 패널 : 버튼, 스피너 배치
        self.panelAction = wx.Panel(self.mainPanel)

        # 버튼 행위
        # 서버, 클라이언트 포트
        self.rdoServerECB = wx.RadioButton(self.panelAction, label = 'ECB', style=wx.RB_GROUP)
        self.rdoServerCTR = wx.RadioButton(self.panelAction, label = 'CTR')
        self.serverHostLabel = wx.StaticText(self.panelAction, label='서버 호스트: ')

        self.serverHostText = wx.TextCtrl(self.panelAction, value="localhost")
        self.serverHostText.Disable()

        self.serverStartButton = wx.Button(self.panelAction, label='서버 시작')
        self.serverStartButton.Bind(wx.EVT_BUTTON, self.startServer)

        self.serverExitButton = wx.Button(self.panelAction, label='서버 종료')
        self.serverExitButton.Disable()
        self.serverExitButton.Bind(wx.EVT_BUTTON, self.stopServer)

        self.rdoClientECB = wx.RadioButton(self.panelAction, label = 'ECB', style=wx.RB_GROUP)
        self.rdoClientCTR = wx.RadioButton(self.panelAction, label = 'CTR')
        self.clientHostLabel = wx.StaticText(self.panelAction, label='타겟 호스트: ')
        self.ClientHostText = wx.TextCtrl(self.panelAction, value='localhost')

        self.clientStartButton = wx.Button(self.panelAction, label='클라이언트 설정')
        self.clientStartButton.Bind(wx.EVT_BUTTON, self.startClient)
        self.clientResetButton = wx.Button(self.panelAction, label='클라이언트 종료')
        self.clientResetButton.Bind(wx.EVT_BUTTON, self.stopClient)

        self.clientChatLabel = wx.StaticText(self.panelAction, label='메시지: ')

        self.clientChatText = wx.TextCtrl(self.panelAction)
        self.clientChatText.Bind(wx.EVT_TEXT_ENTER, self.sendMessage)
        self.clientChatConfirm = wx.Button(self.panelAction, label='보내기')
        self.clientChatConfirm.Disable()
        self.clientChatConfirm.Bind(wx.EVT_BUTTON, self.sendMessage)


        # 결과가 표시되는 텍스트 영역
        self.results = wx.TextCtrl(self.panelAction, style =wx.TE_MULTILINE | wx.HSCROLL)

        # 서버, 클라이언트 포트
        self.serverPortLabel = wx.StaticText(self.panelAction, label='서버 포트: ')
        self.clientPortLabel = wx.StaticText(self.panelAction, label='타겟 포트: ')

        self.serverPort = wx.SpinCtrl(self.panelAction, -1, '')
        self.serverPort.SetRange(0, 65535)
        self.serverPort.SetValue(4097)

        self.clientPort = wx.SpinCtrl(self.panelAction, -1, '')
        self.clientPort.SetRange(0, 65535)
        self.clientPort.SetValue(4097)

        # BoxSizer
        # 패널 내에서 구성요소 차이를 자동 정렬해줌
        # HorizonalBox 내에 IP 범위 스핀 컨트롤, 버튼 추가

        self.actionBoxServer = wx.FlexGridSizer(rows=1, cols=8, hgap=5, vgap=5)
        self.actionBoxClient = wx.FlexGridSizer(rows=1, cols=8, hgap=5, vgap=5)
        self.actionBoxChat = wx.BoxSizer()

        self.actionBoxServer.Add(self.rdoServerECB, proportion=0,flag=wx.LEFT, border=5)
        self.actionBoxServer.Add(self.rdoServerCTR, proportion=0,flag=wx.LEFT, border=5)
        self.actionBoxClient.Add(self.rdoClientECB, proportion=0, flag=wx.LEFT, border=5)
        self.actionBoxClient.Add(self.rdoClientCTR, proportion=0, flag=wx.LEFT, border=5)

        self.actionBoxServer.Add(self.serverHostLabel, proportion=1, flag=wx.LEFT, border=5)
        self.actionBoxClient.Add(self.clientHostLabel, proportion=1, flag=wx.LEFT, border=5)

        self.actionBoxServer.Add(self.serverHostText,proportion = 2, flag=wx.LEFT, border=5)
        self.actionBoxClient.Add(self.ClientHostText,proportion = 2, flag=wx.LEFT, border=5)

        self.actionBoxServer.Add(self.serverPortLabel, proportion=0,flag=wx.LEFT, border=5)
        self.actionBoxClient.Add(self.clientPortLabel, proportion=0, flag=wx.LEFT, border=5)

        self.actionBoxServer.Add(self.serverPort, proportion=1, flag=wx.LEFT, border=5)
        self.actionBoxClient.Add(self.clientPort, proportion=1, flag=wx.LEFT, border=5)

        self.actionBoxServer.Add(self.serverStartButton, proportion=1,flag=wx.RIGHT, border=5)
        self.actionBoxServer.Add(self.serverExitButton, proportion=1,flag=wx.RIGHT, border=5)

        self.actionBoxClient.Add(self.clientStartButton, proportion=1,flag=wx.LEFT, border=5)
        self.actionBoxClient.Add(self.clientResetButton, proportion=1,flag=wx.LEFT, border=5)

        self.actionBoxChat.Add(self.clientChatLabel, proportion=0, flag=wx.LEFT, border=5)
        self.actionBoxChat.Add(self.clientChatText, proportion=1, flag=wx.LEFT, border=5)
        self.actionBoxChat.Add(self.clientChatConfirm, proportion=0, flag=wx.LEFT, border=5)

        # 결과 텍스트 영역
        # HorizonalBox와 결과창을 배치하는 최상위 VerticalBox를 만든다.
        self.vertBox = wx.BoxSizer(wx.VERTICAL)
        self.vertBox.Add(self.actionBoxServer, proportion=0, flag=wx.EXPAND | wx.ALL, border = 5)
        self.vertBox.Add(self.actionBoxClient, proportion=0, flag=wx.EXPAND | wx.ALL, border = 5)
        self.vertBox.Add(self.actionBoxChat, proportion=0, flag=wx.EXPAND | wx.ALL, border = 5)
        self.vertBox.Add(self.results,proportion=1,flag=wx.EXPAND | wx.LEFT| wx.BOTTOM | wx.RIGHT, border = 5)

        redir = RedirectText(self.results)
        sys.stdout = redir
        sys.stderr = redir


        # 상태 표시줄
        self.CreateStatusBar()

        # 박스 사이저를 설정한다.
        self.panelAction.SetSizer(self.vertBox)
        self.panelAction.SetSize(950,550)


if __name__ == '__main__':
    # 메인창 표시
    app = wx.App()
    frame = Frame()
    frame.Show()
    app.MainLoop()