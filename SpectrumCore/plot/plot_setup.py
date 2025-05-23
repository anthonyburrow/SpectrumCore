import matplotlib.pyplot as plt
import matplotlib as mpl


def set_plot_properties():
    # Figure
    mpl.rcParams['figure.figsize'] = (6.4, 4.8)
    mpl.rcParams['figure.dpi'] = 135
    mpl.rcParams['figure.autolayout'] = False

    # Axes and Ticks
    tick_fontsize = 12
    tick_major_length = 5
    tick_minor_length = 2.5
    label_fontsize = 13

    mpl.rcParams['axes.labelsize'] = label_fontsize

    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['xtick.major.top'] = True
    mpl.rcParams['xtick.minor.top'] = True
    mpl.rcParams['xtick.labelsize'] = tick_fontsize
    mpl.rcParams['xtick.major.size'] = tick_major_length
    mpl.rcParams['xtick.minor.size'] = tick_minor_length

    mpl.rcParams['ytick.direction'] = 'in'
    mpl.rcParams['ytick.right'] = True
    mpl.rcParams['ytick.major.right'] = True
    mpl.rcParams['ytick.minor.right'] = True
    mpl.rcParams['ytick.labelsize'] = tick_fontsize
    mpl.rcParams['ytick.major.size'] = tick_major_length
    mpl.rcParams['ytick.minor.size'] = tick_minor_length

    # Lines
    mpl.rcParams['lines.linewidth'] = 1
    mpl.rcParams['lines.markersize'] = 3.5
    mpl.rcParams['lines.markeredgewidth'] = 1

    # Legend
    mpl.rcParams['legend.frameon'] = False
    mpl.rcParams['legend.fontsize'] = label_fontsize - 1

    # Fonts
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['mathtext.fontset'] = 'dejavuserif'


# Setup functions
def basic_spectrum():
    set_plot_properties()

    fig, ax = plt.subplots()

    ax.grid(which='both', axis='x')

    return fig, ax


def residual_spectrum():
    set_plot_properties()

    fig = plt.figure()

    ax = fig.add_axes([0.15, 0.3, 0.8, 0.6])
    ax_res = fig.add_axes([0.15, 0.15, 0.8, 0.15])
    ax_res.sharex(ax)

    ax.grid(which='both', axis='x')

    ax_res.grid(which='both', axis='x')

    return fig, ax, ax_res


# Axis labels
def spectrum_labels(plot, plot_type=None):
    fig, ax = plot

    ax.set_ylabel('Flux')
    if plot_type is None or plot_type == 'optical':
        ax.set_xlabel('Wavelength [A]')
    elif plot_type == 'nir':
        ax.set_xlabel(r'Wavelength [$\mu$m]')


def residual_labels(plot, plot_type=None):
    fig, ax, ax_res = plot

    ax.set_ylabel('Flux')

    if plot_type is None or plot_type == 'optical':
        ax_res.set_xlabel('Wavelength [A]')
    elif plot_type == 'nir':
        ax_res.set_xlabel(r'Wavelength [$\mu$m]')
    ax_res.set_ylabel('Residual')


# Axis scale
def spectrum_scale(plot, plot_type=None):
    fig, ax = plot

    ax.set_yscale('log')
    if plot_type == 'nir':
        ax.set_xscale('log')


def residual_scale(plot, plot_type=None):
    fig, ax, ax_res = plot

    ax.set_yscale('log')
    if plot_type == 'nir':
        ax.set_xscale('log')
        ax_res.set_xscale('log')


# Main function
def setup_plot(residuals=False, plot_type=None):
    if residuals:
        plot = residual_spectrum()

        residual_labels(plot, plot_type)
        residual_scale(plot, plot_type)
    else:
        plot = basic_spectrum()

        spectrum_labels(plot, plot_type)
        spectrum_scale(plot, plot_type)

    return plot
