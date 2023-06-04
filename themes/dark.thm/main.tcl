
# Set name theme
set nameTheme [file tail [file rootname [file dirname [info script]]]]

# load file dark.tcl (./rootDir/asset-theme/dark.tcl)
source [file join [file dirname [info script]] asset-theme dark.tcl]
ttk::style theme use "${nameTheme}-dark"
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