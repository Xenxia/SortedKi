option add *TCombobox*Listbox.background $colors(-other)

ttk::style map TCombobox -selectforeground [list \
    {!focus} $colors(-selectfg) \
    {readonly hover} $colors(-selectfg) \
    {readonly focus} $colors(-selectfg) \
]

ttk::style element create Combobox.field \
    image [list $I(box-basic) \
        {readonly disabled} $I(rect-basic) \
        {readonly pressed} $I(rect-basic) \
        {readonly focus hover} $I(button-hover) \
        {readonly focus} $I(button-hover) \
        {readonly hover} $I(button-hover) \
        {focus hover} $I(box-accent) \
        readonly $I(rect-basic) \
        invalid $I(box-invalid) \
        disabled $I(box-basic) \
        focus $I(box-accent) \
        hover $I(box-hover) \
    ] -border 2
    
ttk::style element create Combobox.button \
    image [list $I(combo-button-basic) \
            {!readonly focus} $I(combo-button-focus) \
            {readonly focus} $I(combo-button-hover) \
            {readonly hover} $I(combo-button-hover)
    ] -border 2

ttk::style element create Combobox.arrow image $I(down) \
    -width 10 -sticky e

ttk::style layout TCombobox {
    Combobox.field -sticky nswe -children {
        Combobox.padding -expand true -sticky nswe -children {
            Combobox.textarea -sticky nswe
        }
    }
    Combobox.button -side right -sticky ns -children {
        Combobox.arrow -sticky nsew
    }
}

ttk::style layout TCombobox {
    Combobox.field -sticky nswe -children {
        Combobox.padding -expand true -sticky nswe -children {
            Combobox.textarea -sticky nswe
        }
    }
    Combobox.button -side right -sticky ns -children {
        Combobox.arrow -sticky nsew
    }
}