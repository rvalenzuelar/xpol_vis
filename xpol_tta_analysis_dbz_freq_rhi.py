import Windprof2 as wp
import xpol
import numpy as np
import matplotlib.pyplot as plt
import os


def make_rhi_list():

    homedir = os.path.expanduser('~')
    setcase = {8: [0.5, 180, 10, 100],
               9: [0.5, 180, 13, 100],
               10: [0.5, 180, 30, 100],
               11: [0.5, 180, 20, 100],
               12: [0.5,   6, 15, 100],
               13: [0.5, 180, 25, 100],
               14: [0.5, 180, 30, 100]}

    rhi_list = []
    for case in range(8, 15):
        elevation, azimuth, _, maxv = setcase[case]
        rhi_list.append(xpol.get_data(case, 'RHI', azimuth, homedir=homedir))

    return rhi_list


def process_rhi(rhi_list):

    homedir = os.path.expanduser('~')
    tta_vr = []
    tta_z = []
    tta_thres = []
    notta_vr = []
    notta_z = []
    notta_thres = []

    for rhis, case in zip(rhi_list, np.arange(len(rhi_list))+8):

        tta_times = wp.get_tta_times(case=str(case), homedir=homedir)
        print(tta_times)

        tta_idxs = np.asarray([], dtype=int)
        for time in tta_times:
            idx = np.where((rhis.index.day == time.day) &
                           (rhis.index.hour == time.hour))[0]
            if idx.size > 0:
                tta_idxs = np.append(tta_idxs, idx)

        notta_idxs = np.delete(np.arange(len(rhis.index)), tta_idxs)
        rhis_tta = rhis.iloc[tta_idxs]
        rhis_notta = rhis.iloc[notta_idxs]

        if rhis_tta.size > 0:
            print('TTA')
            dbz_freq, thres, csum = xpol.get_dbz_freq(rhis_tta['ZA'],
                                                      percentile=50)
            tta_z.append(dbz_freq)
            tta_thres.append(thres)
            rhi_tta_mean, good = xpol.get_mean(rhis_tta['VR'], name='VR')
            tta_vr.append(rhi_tta_mean)

        if rhis_notta.size > 0:
            print('NO TTA')
            dbz_freq, thres, csum = xpol.get_dbz_freq(rhis_notta['ZA'],
                                                      percentile=50)
            notta_z.append(dbz_freq)
            notta_thres.append(thres)
            rhi_notta_mean, good = xpol.get_mean(rhis_notta['VR'], name='VR')
            notta_vr.append(rhi_notta_mean)

    return {'tta_vr': tta_vr, 'tta_z': tta_z, 'tta_thres': tta_thres,
            'notta_vr': notta_vr, 'notta_z': notta_z,
            'notta_thres': notta_thres}


def make_plot_tta(ppi_dict):

    tta_vr = ppi_dict['tta_vr']
    tta_z = ppi_dict['tta_z']
    data = tta_vr+tta_z

    axes = get_axes_gridspec4x2()

    for n, ax in enumerate(axes):
        d = xpol.convert_to_common_grid(data[n])
        if n <= 3:
            xpol.plot(d, ax=ax, name='VR',
                      smode='rhi', colorbar=False,
                      add_yticklabs=True)
        else:
            xpol.plot(d, ax=ax, name='freq',
                      smode='rhi', colorbar=False, vmax=100)

        if n not in [3, 7]:
            ax.set_xticklabels([])

        if n > 0:
            ax.set_yticklabels([])


def make_plot_notta(ppi_dict, select):

    notta_vr = [ppi_dict['notta_vr'][n] for n in select]
    notta_z = [ppi_dict['notta_z'][n] for n in select]
    data = notta_vr+notta_z

    axes = get_axes_gridspec3x2()

    for n, ax in enumerate(axes):
        d = xpol.convert_to_common_grid(data[n])
        if n < 3:
            xpol.plot(d, ax=ax, name='VR',
                      smode='rhi', colorbar=False,
                      add_yticklabs=True)
        else:
            xpol.plot(d, ax=ax, name='freq',
                      smode='rhi', colorbar=False, vmax=100)

        if n not in [2, 5]:
            ax.set_xticklabels([])

        if n > 0:
            ax.set_yticklabels([])


def get_axes_gridspec4x2():

    import matplotlib.gridspec as gridspec

    f = plt.figure(figsize=(8.5, 11))
    gs0 = gridspec.GridSpec(1, 2,
                            top=0.95, bottom=0.1,
                            left=0.05, right=0.98,
                            wspace=0.05)

    gs00 = gridspec.GridSpecFromSubplotSpec(4, 1,
                                            subplot_spec=gs0[0],
                                            wspace=0, hspace=0)
    ax0 = plt.Subplot(f, gs00[0])
    f.add_subplot(ax0)
    ax1 = plt.Subplot(f, gs00[1])
    f.add_subplot(ax1)
    ax2 = plt.Subplot(f, gs00[2])
    f.add_subplot(ax2)
    ax3 = plt.Subplot(f, gs00[3])
    f.add_subplot(ax3)

    gs01 = gridspec.GridSpecFromSubplotSpec(4, 1,
                                            subplot_spec=gs0[1],
                                            wspace=0, hspace=0)
    ax4 = plt.Subplot(f, gs01[0])
    f.add_subplot(ax4)
    ax5 = plt.Subplot(f, gs01[1])
    f.add_subplot(ax5)
    ax6 = plt.Subplot(f, gs01[2])
    f.add_subplot(ax6)
    ax7 = plt.Subplot(f, gs01[3])
    f.add_subplot(ax7)

    return np.array([ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7])


def get_axes_gridspec3x2():

    import matplotlib.gridspec as gridspec

    f = plt.figure(figsize=(8.5, 11))
    gs0 = gridspec.GridSpec(1, 2,
                            top=0.9, bottom=0.35,
                            left=0.1, right=0.9,
                            wspace=0.05)

    gs00 = gridspec.GridSpecFromSubplotSpec(3, 1,
                                            subplot_spec=gs0[0],
                                            wspace=0, hspace=0)
    ax0 = plt.Subplot(f, gs00[0])
    f.add_subplot(ax0)
    ax1 = plt.Subplot(f, gs00[1])
    f.add_subplot(ax1)
    ax2 = plt.Subplot(f, gs00[2])
    f.add_subplot(ax2)

    gs01 = gridspec.GridSpecFromSubplotSpec(3, 1,
                                            subplot_spec=gs0[1],
                                            wspace=0, hspace=0)
    ax3 = plt.Subplot(f, gs01[0])
    f.add_subplot(ax3)
    ax4 = plt.Subplot(f, gs01[1])
    f.add_subplot(ax4)
    ax5 = plt.Subplot(f, gs01[2])
    f.add_subplot(ax5)

    return np.array([ax0, ax1, ax2, ax3, ax4, ax5])


def get_axes_grid(nrows_ncols):

    from mpl_toolkits.axes_grid1 import ImageGrid

    fig = plt.figure(figsize=(8.5, 11))
    axes = ImageGrid(fig, 111,
                     nrows_ncols=nrows_ncols,
                     axes_pad=0,
                     add_all=True,
                     share_all=False,
                     label_mode="L",
                     cbar_location="top",
                     cbar_mode="single",
                     cbar_size='2%',
                     aspect=True)

    return axes


def get_axes_subplots(nrows_ncols):

    nrows, ncols = nrows_ncols
    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(8.5, 11),
                             sharex=True,
                             sharey=True)
    axes = axes.flatten()

    return axes
