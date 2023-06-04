# Checkbutton
ttk::style configure TCheckbutton -padding 4

ttk::style element create Checkbutton.indicator image \
    [list $I(box-basic) \
        {alternate disabled} $I(check-tri-basic) \
        {selected disabled} $I(check-basic) \
        disabled $I(box-basic) \
        {pressed alternate} $I(check-tri-hover) \
        {active alternate} $I(check-tri-hover) \
        alternate $I(check-tri-accent) \
        {pressed selected} $I(check-hover) \
        {active selected} $I(check-hover) \
        selected $I(check-accent) \
        {pressed !selected} $I(rect-hover) \
        active $I(box-hover) \
    ] -width 26 -sticky w