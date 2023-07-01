# Button version
set name "version."

ttk::style configure ${name}TButton \
    -width -10 \
    -anchor center \
    -background $colors(-background) \
    -foreground "#F70000"

ttk::style map ${name}TButton \
    -background [list disabled $colors(-background)] \
    -foreground [list disabled "#00F700"] \
    -relief [list {pressed !disabled} flat]