# Scrollbar
ttk::style element create Horizontal.Scrollbar.trough image $I(hor-basic) \
    -sticky ew

ttk::style element create Horizontal.Scrollbar.thumb \
        image [list $I(hor-accent) \
        disabled $I(hor-basic) \
        pressed $I(hor-hover) \
        active $I(hor-hover) \
    ] -sticky ew

ttk::style element create Vertical.Scrollbar.trough image $I(vert-basic) \
    -sticky ns

ttk::style element create Vertical.Scrollbar.thumb \
    image [list $I(vert-accent) \
        disabled  $I(vert-basic) \
        pressed $I(vert-hover) \
        active $I(vert-hover) \
    ] -sticky ns

ttk::style layout Vertical.TScrollbar {
    Vertical.Scrollbar.trough -sticky ns -children {
        Vertical.Scrollbar.thumb -expand true
    }
}

ttk::style layout Horizontal.TScrollbar {
    Horizontal.Scrollbar.trough -sticky ew -children {
        Horizontal.Scrollbar.thumb -expand true
    }
}