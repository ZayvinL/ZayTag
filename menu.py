import nuke
import CurrentPath
import ZayTagPath


ZayTagPath.run_show_funa
bar = nuke.menu('Nodes')
toolbar = bar.addMenu("Z")
#toolbar.addCommand('ZayTag', ZayTagPath.runshow)
toolbar.addCommand('ZayTag', ZayTagPath.run_show_funa)







