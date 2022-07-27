
proc findFiles { basedir pattern } {

    # Fix the directory name, this ensures the directory name is in the
    # native format for the platform and contains a final directory seperator
    set basedir [string trimright [file join [file normalize $basedir] { }]]
    set fileList {}

    # Look in the current directory for matching files, -type {f r}
    # means ony readable normal files are looked at, -nocomplain stops
    # an error being thrown if the returned list is empty
    foreach fileName [glob -nocomplain -type {f r} -path $basedir $pattern] {
        lappend fileList $fileName
    }

    # Now look for any sub direcories in the current directory
    foreach dirName [glob -nocomplain -type {d  r} -path $basedir *] {
        # Recusively call the routine on the sub directory and append any
        # new files to the results
        set subDirList [findFiles $dirName $pattern]
        if { [llength $subDirList] > 0 } {
            foreach subDirFile $subDirList {
                lappend fileList $subDirFile
            }
        }
    }
    return $fileList
}

proc load_images {imgdir} {
    foreach file [glob -directory $imgdir *.png] {

        set img [file tail [file rootname $file]]
        set Iarray($img) [image create photo -file $file -format png]
    }
    return [array get Iarray]
}

# load Image
array set I [load_images [file join [file dirname [info script]] dark/img]]

#load TCL file
set fileTCL [findFiles [file join [file dirname [info script]] dark] *.tcl]

ttk::style theme create "${nameTheme}-dark" -parent alt -settings {

        # Global Color
        array set colors {
            -fg             "#ffffff"
            -bg             "#000000"
            -disabledfg     "#aaaaaa"
            -disabledbg     "#110000"
            -selectfg       "#ffffff"
            -selectbg       "#707070"
            -other          "#333333"
            -accent         "#00FF00"
        }

        #Global Config

        ttk::style configure . \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -troughcolor $colors(-bg) \
            -focuscolor $colors(-selectbg) \
            -selectbackground $colors(-selectbg) \
            -selectforeground $colors(-selectfg) \
            -insertcolor $colors(-fg) \
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
        option add *Menu.selectcolor $colors(-fg)

        ttk::style configure Sash -gripcount 0

        # ============================================================================

        # source all TCL file

        foreach f $fileTCL {
            source $f
        }

}