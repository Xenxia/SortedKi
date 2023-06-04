# Button no bg
set name "nobg."

ttk::style configure ${name}TButton \
    -width -10 \
    -anchor center \
    -background $colors(-bg)

ttk::style map ${name}TButton \
    -background [list disabled $colors(-bg) active $colors(-bg)] \
    -foreground [list disabled $colors(-fg)] \
    -relief [list {pressed !disabled} flat]
