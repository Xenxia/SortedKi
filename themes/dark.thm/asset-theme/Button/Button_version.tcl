# Button version
set name "version."

ttk::style configure ${name}TButton \
    -width -10 \
    -anchor center \
    -background $colors(-background) \
    -foreground "#aa0000"

ttk::style map ${name}TButton \
    -background [list disabled $colors(-background)] \
    -foreground [list disabled "#00aa00"] \
    -relief [list {pressed !disabled} flat]