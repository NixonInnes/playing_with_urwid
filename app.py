import urwid


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
        print(widget.contents)
        return widget

    def create_edit(self, label, text, on_change):
        widget = urwid.Edit(label, text, multiline=False)
        urwid.connect_signal(widget, 'change', on_change)
        widget = urwid.AttrWrap(widget, 'edit')
        return widget

    def create_tile(self):
        widget = urwid.LineBox(urwid.Filler(urwid.Text('', align='left'), valign='top'))
        widget = urwid.AttrWrap(widget, 'tile')
        return widget

    # Events
    def edit_change_event(self, widget, text):
        self.tile1.base_widget.set_text(text)

    def quit_on_clicked(self, button):
        raise urwid.ExitMainLoop()

    def build_widgets(self):
        self.header = self.create_header('My Urwid Application')
        self.tile1 = self.create_tile()
        self.tile2 = self.create_tile()
        self.edit = self.create_edit('> ', '', self.edit_change_event)

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
            self.build_view(),
            palette=self.palette
        ).run()


if __name__ == '__main__':
    app = Main()
    app.run()