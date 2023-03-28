# Button
set name ""

# ttk::style layout TButton {
#     Button.button -children {
#         # Button.focus -children {
#             Button.padding -children {
#                 Button.label -expend true
#             }
#         # 
#     }
# }

# ttk::style layout TButton {
#     Button.button -children {
#         Button.padding -children {
#             Button.label -side left -expand true -anchor center
#         } 
#     }
# }

ttk::style configure ${name}TButton \
    -anchor center \
    -background $colors(-other) \
    -border $colors(-other)

ttk::style map ${name}TButton \
    -background [list disabled $colors(-disabledbg) active $colors(-selectbg)] \
    -foreground [list disabled $colors(-disabledfg) ] \
    -relief [list {pressed !disabled} groove]

