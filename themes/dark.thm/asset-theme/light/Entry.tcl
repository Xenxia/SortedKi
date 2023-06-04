ttk::style element create Entry.field \
    image [list $I(box-basic) \
        {focus hover} $I(box-accent) \
        invalid $I(box-invalid) \
        disabled $I(box-basic) \
        focus $I(box-accent) \
        hover $I(box-hover) \
    ] -border 5 -padding {3} -sticky news