
import xpol
# import gapflow
# import matplotlib.pyplot as plt
# import numpy as np

'''	printing single and mean values
'''
setcase={	8:[0.5, 180],
			9:[0.5, 180],
		    10:[0.5, 180],
		    11:[0.5, 180],
		    12:[0.5, 147],
		    13:[0.5, 180],
		    14:[0.5, 180]}

o='c{}_xpol_singlescan_{}_{}_{}.pdf'

# case=8

for case in range(9,15):
	
	elev,azim=setcase[case]

	field = 'ZA'

	rhis=xpol.get_data(case,'RHI',azim)
	oname=o.format(str(case).zfill(2), 'rhi', str(azim), field)
	xpol.plot_single(rhis, name=field, smode='rhi',case=case, saveas=oname)
	# xpol.plot_single(rhis.ix[:3,:], name=field, smode='rhi',case=case, saveas=oname)

	ppis=xpol.get_data(case,'PPI',elev)
	oname=o.format(str(case).zfill(2), 'ppi', str(elev), field)
	xpol.plot_single(ppis, name=field, smode='ppi', case=case, saveas=oname)


	field = 'VR'

	rhis=xpol.get_data(case,'RHI',azim)
	oname=o.format(str(case).zfill(2), 'rhi', str(azim), field)
	xpol.plot_single(rhis, name=field, smode='rhi', case=case, saveas=oname)

	ppis=xpol.get_data(case,'PPI',elev)
	oname=o.format(str(case).zfill(2), 'ppi', str(elev), field)
	xpol.plot_single(ppis,name=field, smode='ppi', case=case, saveas=oname)

