from .plot_setup import setup_plot


PLOT_PARAMS = {
    'lw': 1.
}


def plot_main_panel(plot, data=None, model_result=None, *args, **kwargs):
    if data is None:
        return

    ax = plot[1]

    wave = data[:, 0]
    flux = data[:, 1]

    ax.plot(wave, flux, **PLOT_PARAMS)

    if model_result is None:
        return ax

    ax.plot(wave, model_result.best_fit, **PLOT_PARAMS)


def plot_residual_panel(plot, data=None, model_result=None, *args, **kwargs):
    if data is None and model_result is None:
        return

    ax_res = plot[2]

    wave = data[:, 0]
    flux = data[:, 1]
    res = flux - model_result.best_fit

    ax_res.plot(wave, res, 'r-', **PLOT_PARAMS)
    ax_res.axhline(0., color='k', **PLOT_PARAMS)


def plot_spectrum(
    residuals=False, plot_type=None, out_filename=None, display=False,
    *args, **kwargs
):
    plot = setup_plot(residuals, plot_type)

    plot_main_panel(plot, *args, **kwargs)
    if residuals:
        plot_residual_panel(plot, *args, **kwargs)

    fig = plot[0]
    if out_filename is not None:
        fig.savefig(out_filename)

    if display:
        fig.show()

    return plot
