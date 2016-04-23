import urwid


class Input(urwid.Edit):
    def __init__(self):
        super().__init__('> ')
        self.multiline = False

    def keypress(self, size, key):
        if key != 'enter':
            return super().keypress(size, key)
        
        self.set_edit_text('')


def main():

    title = urwid.Text('My Title')
    quit_button = urwid.Button('X')

    top_r = urwid.LineBox(urwid.Filler(urwid.Text('top r')))
    top_m = urwid.LineBox(urwid.Filler(urwid.Text('top m')))
    top_l = urwid.LineBox(urwid.Filler(urwid.Text('top l')))
    bot_r = urwid.LineBox(urwid.Filler(urwid.Text('bot r')))
    bot_m = urwid.LineBox(urwid.Filler(urwid.Text('bot m')))
    bot_l = urwid.LineBox(urwid.Filler(urwid.Text('bot l')))

    edit = Input()

    layout = urwid.Frame(
        urwid.Pile([
            urwid.Columns([top_l,top_m,top_r]),
            urwid.Columns([bot_l,bot_m,bot_r]),
        ]),
        header=urwid.Columns([title, quit_button]),
        footer=edit
    )

    def quit_on_clicked(button):
        raise urwid.ExitMainLoop()

    def unhandled_input(key):
        if key in ['q', 'Q']:
            raise urwid.ExitMainLoop()

    urwid.connect_signal(quit_button, 'click', quit_on_clicked)

    loop = urwid.MainLoop(
        layout,
        unhandled_input=unhandled_input
    )

    loop.run()


if __name__ == '__main__':
    main()