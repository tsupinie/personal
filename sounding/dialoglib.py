
import Tkinter as Tk

class DialogBase(Tk.Toplevel):
    def __init__(self, parent, title=None):
        Tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Tk.Frame(self)
        self.initial_focus = self._body(body)
        body.grid(padx=5, pady=5)

        self._buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self._cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)
        return

    #
    # construction hooks
    def _body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        return

    def _buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = Tk.Frame(self)

        w = Tk.Button(box, text="OK", width=10, command=self._ok, default=Tk.ACTIVE)
        w.grid(row=1, column=1, padx=5, pady=5)
        w = Tk.Button(box, text="Cancel", width=10, command=self._cancel)
        w.grid(row=1, column=2, padx=5, pady=5)

        self.bind("<Return>", self._ok)
        self.bind("<Escape>", self._cancel)

        box.grid()
        return

    #
    # standard button semantics
    def _ok(self, event=None):
        if not self._validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self._apply()

        self._cancel()
        return

    def _cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
        return

    #
    # command hooks
    def _validate(self):
        return 1 # override

    def _apply(self):
        return # override

class SPCFileLoadDialog(DialogBase):
    _stations = [
        "AMA (Amarillo, TX)",
        "DDC (Dodge City, KS)",
        "DRT (Del Rio, TX)",
        "EPZ (El Paso, TX)",
        "FWD (Fort Worth, TX)",
        "MAF (Midland, TX)",
        "OUN (Norman, OK)",
        "SGF (Springfield, MO)",
        "TOP (Topeka, KS)",
    ]    

    _default = "OUN (Norman, OK)"

    def __init__(self, parent):
        self._station = Tk.StringVar(parent)
        self._station.set(SPCFileLoadDialog._default)

        DialogBase.__init__(self, parent)
        return

    def _body(self, parent):
        label = Tk.Label(text="Select a Station", master=parent)
        label.grid(row=1, column=1)

        option_menu = Tk.OptionMenu(parent, self._station, *SPCFileLoadDialog._stations)
        option_menu.grid(row=1, column=2)
        return

    def _apply(self):
        self.result = self._station.get()[:3]
        return
