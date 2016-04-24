import socket
import urwid
from threading import Thread


class Input(urwid.Edit):
    def __init__(self, label, text, on_return):
        super().__init__(label, text)
        self.multiline = False
        self.on_return = on_return

    def keypress(self, size, key):
        if key == 'enter':
            self.on_return(self.get_edit_text())
            self.set_edit_text('')
        if not self.valid_char(key):
            return super().keypress(size, key)
        self.insert_text(key)


class Main(object):
    def __init__(self):
        self.sock = None
        self.palette = [
            ('header', 'white', 'dark green', 'bold'),
            ('tile', 'dark gray', 'white'),
            ('edit', 'black', 'light gray'),
            ('qbutton', 'white', 'dark red')
        ]
        self.build_widgets()

    # Connection
    def connect(self, host, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
                self.update_screen('Connecting to %s:%s...' % (host, port))
                self.sock.connect((host, port))
                while True:
                    data = str(self.sock.recv(1024), 'utf-8')
                    self.update_screen(data)
                self.sock.close()
                self.update_screen('Connection closed.')
        except ConnectionRefusedError:
            self.update_screen('[ERROR] Connection Refused.')

    # Define Widgets
    def create_header(self, header):
        widget = urwid.Columns([
            urwid.AttrWrap(urwid.Text(header, align='center'), 'header'),
            ('weight', 0.05, urwid.AttrWrap(urwid.Button('x', on_press=self.quit_on_clicked), 'qbutton'))
        ])
        return widget

    def create_input(self, label, text, on_return):
        widget = Input(label, text, on_return)
        widget = urwid.AttrWrap(widget, 'edit')
        return widget

    def create_tile(self):
        widget = urwid.LineBox(urwid.Filler(urwid.Text('', align='left'), valign='top'))
        widget = urwid.AttrWrap(widget, 'tile')
        return widget

    # Define Events
    def cli_on_return(self, text):
        text_ = self.history.base_widget.text + '\n' + text
        self.history.base_widget.set_text(text_)
        if self.sock:
            self.sock.send(bytes(text, 'utf-8'))

    def address_on_return(self, address):
        try:
            host, port = address.split(':')
        except Exception as e:
            self.update_screen('{msg}\n{error}'.format(msg='Unable to parse address', error=e))
            return
        self.connection = Thread(target=self.connect, args=(host, int(port)))
        self.connection.start()

    def quit_on_clicked(self, button):
        if self.sock:
            self.sock.close()
        raise urwid.ExitMainLoop()

    # Create Widgets
    def build_widgets(self):
        self.header = self.create_header('NixCat')
        self.screen = self.create_tile()
        self.history = self.create_tile()
        self.cli = self.create_input('> ', '', self.cli_on_return)
        self.address = self.create_input('address: ', '', self.address_on_return)

    # Build View
    def build_view(self):
        view = urwid.Frame(
            urwid.Pile([
                (1, urwid.Filler(self.address)),
                urwid.Columns([
                    self.screen,
                    ('weight', 0.2, self.history)
                ]),
            ]),
            header=self.header,
            footer=self.cli
        )
        return view

    # Helper methods
    def update_screen(self, text):
        self.screen.base_widget.set_text(
            self.screen.base_widget.text + text
        )

    # Run
    def run(self):
        urwid.MainLoop(
            self.build_view(),
            palette=self.palette
        ).run()


if __name__ == '__main__':
    app = Main()
    app.run()