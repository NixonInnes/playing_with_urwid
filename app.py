import urwid


class Main(object):
    def __init__(self):
        self.build_widgets()

    palette = [
        ('header', 'white', 'dark green', 'bold'),
        ('tile', 'dark grey', 'white'),
        ('edit', 'light grey', 'dark green')
    ]

    # Widgets
    def create_header(self, header):
        widget = urwid.Columns([
            urwid.AttrWrap(urwid.Text(header), 'header'),
            urwid.Button('x', on_press=self.quit_on_clicked)
        ])
        return widget

    def create_edit(self, label, text, on_change):
        widget = urwid.Edit(label, text, multiline=False)
        urwid.connect_signal(widget, 'change', on_change)
        on_change(widget, text)
        widget = urwid.AttrWrap(widget, 'edit')
        return widget

    def create_tile(self):
        widget = urwid.LineBox(urwid.Filler(urwid.Text('', align='left')))
        widget = urwid.AttrWrap(widget, 'tile')
        return widget

    # Events
    def edit_change_event(self, widget, text):
        pass

    def quit_on_clicked(self, button):
        raise urwid.ExitMainLoop()

    def build_widgets(self):
        self.header = self.create_header('My Urwid Application')
        self.edit = self.create_edit('>', '', self.edit_change_event)
        self.tile1 = self.create_tile()
        self.tile2 = self.create_tile()

    # View
    def build_view(self):
        view = urwid.Frame(
            urwid.Columns([
                self.tile1,
                self.tile2
            ]),
            header=self.header,
            footer=self.edit
        )
        return view

    def run(self):
        urwid.MainLoop(
            self.build_view()
        ).run()


class Input(urwid.Edit):
    def __init__(self):
        super().__init__('> ')
        self.multiline = False

    def keypress(self, size, key):
        if key != 'enter':
            return super().keypress(size, key)
        self.set_edit_text('')


if __name__ == '__main__':
    app = Main()
    app.run()