import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter, NullFormatter


PLOT_DPI = 135


# Setup functions
def basic_spectrum():
    fig, ax = plt.subplots(dpi=PLOT_DPI)

    ax.grid(which='both', axis='x')

    ax.tick_params(axis='both', which='both', direction='in',
                   top=True, right=True)

    return fig, ax


def residual_spectrum():
    fig = plt.figure(dpi=PLOT_DPI)

    ax = fig.add_axes([0.15, 0.3, 0.8, 0.6])
    ax_res = fig.add_axes([0.15, 0.15, 0.8, 0.15])

    # Main axis
    ax.grid(which='both', axis='x')

    ax.tick_params(axis='both', which='both', direction='in',
                   top=True, right=True)

    # Residual axis
    ax_res.grid(which='both', axis='x')

    ax_res.tick_params(axis='both', which='both', direction='in',
                       top=True, right=True)

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
