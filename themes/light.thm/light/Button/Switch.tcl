# Switch
set name "Switch."

ttk::style element create ${name}indicator image \
    [list $I(off-basic) \
        {selected disabled} $I(on-basic) \
        disabled $I(off-basic) \
        {pressed selected} $I(on-accent) \
        {active selected} $I(on-accent) \
        selected $I(on-accent) \
        {pressed !selected} $I(off-basic) \
        active $I(off-basic) \
    ] -width 46 -sticky w

ttk::style layout ${name}TCheckbutton {
    ${name}button -children {
        ${name}padding -children {
            ${name}indicator -side left
            ${name}label -side right -expand true
        }
    }
}