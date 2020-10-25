import urwid
import api

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    if not len(choices):
        button = urwid.Button('Fant ingen treff')
        urwid.connect_signal(button, 'click', exit_program)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    else:    
        for c in choices:
            button = urwid.Button(f"{c.get('stedsnavn')}, {c.get('kommunenavn')}, {c.get('fylkesnavn')}")
            urwid.connect_signal(button, 'click', item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, c):
    response = urwid.Text([u'Du valgte ', f"{c.get('stedsnavn')}, {c.get('kommunenavn')}, {c.get('fylkesnavn')}", u'\n'
    f"aust {c.get('aust')}, nord {c.get('nord')}"])
    done = urwid.Button(u'Ok')
    back = urwid.Button(u'Return')
    urwid.connect_signal(done, 'click', exit_program)
    urwid.connect_signal(back, 'click', back_to_menu)
    main.original_widget = urwid.Filler(urwid.Pile([response,
        urwid.AttrMap(done, None, focus_map='reversed'),
        urwid.AttrMap(back, None, focus_map='reversed')]))

def back_to_menu(button):
    main.original_widget = urwid.Padding(menu(u'Velg ein stad', choices), left=2, right=2)

def exit_program(button):
    raise urwid.ExitMainLoop()

class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        #nasty global incoming
        global choices
        choices = api.list_locations(edit.edit_text)
        main.original_widget = urwid.Padding(menu(u'Velg ein stad', choices), left=2, right=2)
        

edit = urwid.Edit(u"Skriv inn stadsnamn\n")
fill = QuestionBox(edit)
loop = urwid.MainLoop(fill)

#main = urwid.Padding(menu(u'Velg ein stad', choices), left=2, right=2)
main = urwid.Padding(QuestionBox(edit))
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 69),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
