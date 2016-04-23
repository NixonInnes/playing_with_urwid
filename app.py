import os
import urwid


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
        self.palette = [
            ('header', 'white', 'dark green', 'bold'),
            ('tile', 'dark gray', 'white'),
            ('edit', 'black', 'light gray'),
            ('qbutton', 'white', 'dark red')
        ]
        self.build_widgets()

    # Widgets
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

    # Events
    def cli_on_return(self, text):
        text = self.tile1.base_widget.text + '\n' + text
        self.tile1.base_widget.set_text(text)

    def fload_on_return(self, fname):
        if not os.path.isfile(fname):
            self.tile2.base_widget.set_text('File Not Found.')
            return
        with open(fname) as file:
            self.tile2.base_widget.set_text(file.read())

    def quit_on_clicked(self, button):
        raise urwid.ExitMainLoop()

    def build_widgets(self):
        self.header = self.create_header('My Urwid Application')
        self.tile1 = self.create_tile()
        self.tile2 = self.create_tile()
        self.cli = self.create_input('> ', '', self.cli_on_return)
        self.fload = self.create_input('file: ', '', self.fload_on_return)

    # View
    def build_view(self):
        view = urwid.Frame(
            urwid.Pile([
                (1, urwid.Filler(self.fload)),
                urwid.Columns([
                    self.tile1,
                    self.tile2
                ]),
            ]),
            header=self.header,
            footer=self.cli
        )
        return view

    def run(self):
        urwid.MainLoop(
            self.build_view(),
            palette=self.palette
        ).run()


if __name__ == '__main__':
    app = Main()
    app.run()