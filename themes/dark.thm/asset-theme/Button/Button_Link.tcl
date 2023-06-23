# Button no bg
set name "link."

ttk::style configure ${name}TButton \
    -width -10 \
    -anchor center \
    -background $colors(-background) \
    -foreground "#03F4A5"

ttk::style map ${name}TButton \
    -background [list disabled $colors(-background) active $colors(-background)] \
    -foreground [list disabled $colors(-foreground)] \
    -relief [list {pressed !disabled} flat]
