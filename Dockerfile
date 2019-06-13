FROM webviz/base_image

COPY . dash_app
RUN chmod -R 660 dash_app