FROM webviz/base_image:latest
COPY . dash_app
COPY --chown=1000 . dash_app
