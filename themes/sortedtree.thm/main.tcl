

set nameTheme [file tail [file rootname [file dirname [info script]]]]
source [file join [file dirname [info script]] asset-theme dark.tcl]

proc set_theme {mode} {
    global nameTheme
    if {$mode == "dark"} {
        ttk::style theme use "${nameTheme}-dark"

    }
}