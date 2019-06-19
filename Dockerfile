FROM webvizstandardtest.azurecr.io/webviz_base7:latest
COPY . dash_app
COPY --chown=appuser . dash_app
