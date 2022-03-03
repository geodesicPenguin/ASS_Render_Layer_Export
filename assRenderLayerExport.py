from contextlib import contextmanager
import maya.app.renderSetup.model.renderSetup as renderSetup

@contextlib.contextmanager
def maintained_render_layer():
    previous_rs = renderSetup.instance().getVisibleRenderLayer()
    try:
        yield
    finally:
        renderSetup.instance().switchToLayer(previous_rs)
        print("ALL VISIBLE LAYERS FINISHED EXPORTING")

# export all render layers to ASS files.

from pymel.core.other import arnoldExportAss

export_options = {'filename':'<path to render location>','startFrame':1,'endFrame':120} # supply your own arnoldExportAss options here         
with maintained_render_layer():
    render_setup = renderSetup.instance()
    render_layers = render_setup.getRenderLayers()

    for layer in renderSetup.instance().getRenderLayers():
        if layer.isRenderable():
            layer_name = layer.name()
            layer_obj = renderSetup.instance().getRenderLayer(layer_name)
            renderSetup.instance().switchToLayer(layer_obj)
            print("Run ASS Export for render layer "
                "'{}' with options: '{}'".format(layer.name(), export_options))
            arnoldExportAss(**export_options)
        else:
            print(f"{layer} not set, skipping!")