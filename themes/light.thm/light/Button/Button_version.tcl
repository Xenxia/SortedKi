# Button version
set name "version."

ttk::style configure ${name}TButton \
    -width -10 \
    -anchor center \
    -background $colors(-bg) \
    -foreground "#aa0000"

ttk::style map ${name}TButton \
    -background [list disabled $colors(-bg)] \
    -foreground [list disabled "#00aa00"] \
    -relief [list {pressed !disabled} flat]