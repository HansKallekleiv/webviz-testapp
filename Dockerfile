FROM webviz/base_image:latest
COPY . dash_app
COPY --chown=appuser . dash_app
