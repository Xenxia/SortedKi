import tkinter
r=tkinter.Tcl()
# r.eval('source ./sortedtree.thm/main.tcl')
# r.evalfile("./sortedtree.thm/main.tcl")
r.tk.call("source", "./sortedtree.thm/main.tcl")
# result = r.tk.call("set_theme", "test")

# print(result)