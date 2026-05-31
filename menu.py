import nuke
import CurrentPath
import SearchPanelB


SearchPanelB.run_show_funa
bar = nuke.menu('Nodes')
toolbar = bar.addMenu("Z")
toolbar.addCommand('pipline/Plate Search file', SearchPanelB.runshow)







