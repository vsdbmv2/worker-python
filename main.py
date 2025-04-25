import socketio
from src.handleWork import handleWorks

socket = socketio.Client()
socket.connect('ws://192.168.0.25:4242')

class Worker():
  local_work = []

  def on_connect(self):
      print('Connected')

  def on_pong(self, data):
      # print('I received a pong!')
      if len(self.local_work) == 0:
        print('trying to get a work')
        socket.emit('get-work', {'worksAmount': 2})
      elif len(self.local_work) > 0 and all(work['status'] == 'DONE' for work in self.local_work):
        print(f'finishing {len(self.local_work)} works')
        socket.emit('work-complete', self.local_work)
        self.local_work.clear()
      else:
        pass
        # print('nothing', len(self.local_work))

  def on_work(self, data):
    if data:
      self.local_work = data
      print(f'getting {len(self.local_work)} works')
      processed_work = handleWorks(self.local_work)
      print('got it', len(self.local_work))
      for index,work in enumerate(self.local_work):
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