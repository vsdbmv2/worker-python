import socketio
import os
from src.handleWork import handleWorks

# Obtendo variáveis de ambiente com valores padrão
SERVER_URL = os.getenv('SERVER_URL', 'ws://192.168.0.25:4242')
WORKS_AMOUNT = int(os.getenv('WORKS_AMOUNT', '2'))

socket = socketio.Client()
socket.connect(SERVER_URL)

class Worker():
    local_work = []

    def on_connect(self):
        print('Connected')

    def on_pong(self, data):
        if len(self.local_work) == 0:
            print('trying to get a work')
            socket.emit('get-work', {'worksAmount': WORKS_AMOUNT})
        elif len(self.local_work) > 0 and all(work['status'] == 'DONE' for work in self.local_work):
            print(f'finishing {len(self.local_work)} works')
            socket.emit('work-complete', self.local_work)
            self.local_work.clear()
        else:
            pass

    def on_work(self, data):
        if data:
            self.local_work = data
            print(f'getting {len(self.local_work)} works')
            processed_work = handleWorks(self.local_work)
            print('got it', len(self.local_work))
            for index, work in enumerate(self.local_work):
                work['payload'] = processed_work[index]
                work['status'] = 'DONE'
                print(processed_work[index])
            print(len(self.local_work))

    def catch_all(event, sid, data):
        print('Catched')
        print(event)

if __name__ == '__main__':
    worker = Worker()
    socket.on('connect', worker.on_connect)
    socket.on('pong', worker.on_pong)
    socket.on('work', worker.on_work)
    socket.on('*', worker.catch_all)