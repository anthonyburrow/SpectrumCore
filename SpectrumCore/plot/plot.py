from .plot_setup import setup_plot


PLOT_PARAMS = {
    'lw': 1.
}


def plot_main_panel(plot, data, plot_type=None, model_result=None,
                    *args, **kwargs):
    ax = plot[1]

    if plot_type == 'nir':
        wave = data[:, 0] * 1.e-4
    else:
        wave = data[:, 0]
    flux = data[:, 1]

    ax.plot(wave, flux, **PLOT_PARAMS)

    if model_result is None:
        return ax

    ax.plot(wave, model_result.best_fit, **PLOT_PARAMS)


def plot_residual_panel(plot, data, plot_type=None, model_result=None,
                        *args, **kwargs):
    if data is None and model_result is None:
        return

    ax_res = plot[2]

    if plot_type == 'nir':
        wave = data[:, 0] * 1.e-4
    else:
        wave = data[:, 0]
    flux = data[:, 1]
    res = flux - model_result.best_fit

    ax_res.plot(wave, res, 'r-', **PLOT_PARAMS)
    ax_res.axhline(0., color='k', **PLOT_PARAMS)


def plot_spectrum(data, residuals=False, plot_type=None, out_filename=None,
                  display=False, *args, **kwargs):
    if plot_type is None and data[-1:, 0] > 9500.:
        plot_type = 'nir'

    plot = setup_plot(residuals, plot_type)

    plot_main_panel(plot, data, plot_type=plot_type, *args, **kwargs)
    if residuals:
        plot_residual_panel(plot, data, plot_type=plot_type, *args, **kwargs)

    fig = plot[0]
    if out_filename is not None:
        fig.savefig(out_filename, bbox_inches='tight')

    if display:
        fig.show()

    return plot
