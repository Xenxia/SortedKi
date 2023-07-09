# Switch
set name "Switch."

ttk::style element create ${name}indicator image \
    [list $I(off) \
        {selected disabled} $I(on) \
        disabled $I(off) \
        {pressed selected} $I(on) \
        {active selected} $I(on) \
        selected $I(on) \
        {pressed !selected} $I(off) \
        active $I(off) \
    ] -width 46 -sticky w

ttk::style layout Switch.TCheckbutton {
    Switch.button -children {
        Switch.padding -children {
            Switch.indicator -side left
            Switch.label -side right -expand true
        }
    }
}