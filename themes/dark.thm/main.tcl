
# Set name theme
set nameTheme [file tail [file rootname [file dirname [info script]]]]

# load file dark.tcl (./rootDir/proc.tcl)
source [file join [file dirname [info script]] proc.tcl]

# load Image
array set I [load_images [file join [file dirname [info script]] asset-theme/img]]

# found all sub TCL file
set fileTCL [findFiles [file join [file dirname [info script]] asset-theme] *.tcl]

ttk::style theme create "${nameTheme}" -parent alt -settings {

        # Global Color
        array set colors {
            -primary        "#00F700"
            -primaryVar     ""
            -secondary      ""
            -secondaryVar   ""
            -background     "#000000"
            -foreground     "#ffffff"

            -disabledfg     "#aaaaaa"
            -disabledbg     "#110000"
            -selectfg       "#ffffff"
            -selectbg       "#707070"
            -other          "#333333"
        }

        #Global Config

        ttk::style configure . \
            -background $colors(-background) \
            -foreground $colors(-foreground) \
            -troughcolor $colors(-background) \
            -focuscolor $colors(-selectbg) \
            -selectbackground $colors(-selectbg) \
            -selectforeground $colors(-selectfg) \
            -insertcolor $colors(-foreground) \
            -insertwidth 1 \
            -fieldbackground $colors(-selectbg) \
            -font {"Consolas" 10 bold} \
            -borderwidth 1 \
            -relief flat

        tk_setPalette background [ttk::style lookup . -background] \
            foreground [ttk::style lookup . -foreground] \
            highlightColor [ttk::style lookup . -focuscolor] \
            selectBackground [ttk::style lookup . -selectbackground] \
            selectForeground [ttk::style lookup . -selectforeground] \
            activeBackground [ttk::style lookup . -selectbackground] \
            activeForeground [ttk::style lookup . -selectforeground]

        ttk::style map . -foreground [list disabled $colors(-disabledfg)]

        option add *font [ttk::style lookup . -font]
        option add *Menu.selectcolor $colors(-foreground)

        ttk::style configure Sash -gripcount 0

        # ============================================================================

        # source all TCL file

        foreach f $fileTCL {
            source $f
        }
}

ttk::style theme use "${nameTheme}"
# source [file join [file dirname [info script]] asset-theme light.tcl]

# puts $nameTheme

# puts [file tail [file rootname [file dirname [info script]]]]
# puts [file rootname [file dirname [info script]]]
# puts [file dirname [info script]]
# puts [info script]

# proc set_theme {mode} {
#     global nameTheme
#     if {$mode == "dark"} {
#         puts [file join [file dirname [info script]] asset-theme dark.tcl]
#         ttk::style theme use "${nameTheme}-dark"
#     }

#     if {$mode == "light"} {
#         ttk::style theme use "${nameTheme}-light"
#     }
# }