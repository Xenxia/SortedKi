# Treeview
ttk::style element create Treeview.field image $I(card2) \
    -border 5

ttk::style element create Treeheading.cell \
    image [list $I(tree-basic)] \
    -border 5 -padding 1 -sticky ewns

ttk::style element create Treeitem.indicator \
    image [list $I(plus) \
        user2 $I(empty) \
        user1 $I(moins) \
    ] -width 16 -sticky {}

ttk::style configure Treeview \
    -background $colors(-background) \
    -font {"Segor Ui" 10} \
    -indent 10


ttk::style configure Treeview.Item -padding {2 0 0 0}

ttk::style map Treeview \
    -background [list selected #414141]
# -foreground [list selected $colors(-selectfg)]