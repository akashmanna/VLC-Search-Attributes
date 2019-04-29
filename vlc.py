import socket
import subprocess
import telnetlib
import time

class VLC:
    def __init__(self):
        self.SCREEN_NAME = 'vlc4'
        self.HOST = 'localhost'
        self.PORT = '9989'

        cmd = subprocess.run(
            ['screen', '-ls', self.SCREEN_NAME,],
            stdout=subprocess.DEVNULL)
        if cmd.returncode:
            subprocess.run([
                'screen',
                '-dmS',
                self.SCREEN_NAME,
                'vlc',
                '--intf',
                'qt',
                '--extraintf',
                'rc',
                '--rc-show-pos',
                '--rc-host',
                '%s:%s' % (self.HOST, self.PORT)
            ])

            time.sleep(0.500)
            try:
                self.vlcSock = telnetlib.Telnet(self.HOST, self.PORT)
            except:
                print("Failed to connect to VLC. Aborting.\n")
                exit(0)

    def send(self, cmd):
        '''Prepare a command and send it to VLC'''
        if not cmd.endswith('\n'):
            cmd = cmd + '\n'
        cmd = cmd.encode('ascii')
        try:
            self.vlcSock.write(cmd)
        except:
            print("Failed to send cmd\n")

    def pause(self):
        self.send('pause')

    def play(self):
        self.send('play')

    def stop(self):
        self.send('stop')

    def prev(self):
        self.send('prev')

    def next(self):
        self.send('next')

    def add(self, path):
        self.send('add %s'  % (path,))

    def seek(self, val):
        print('seek %s'  % (val,))
        self.send('seek %s'  % (val,))

    def enqueue(self, path):
        self.send('enqueue %s' % (path,))

    def clear(self):
        self.send('clear')

    def shutdown(self):
        self.send('shutdown')

