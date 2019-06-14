FROM webviz/base_image

COPY . dash_app
RUN chmod -R 660 dash_app
ENV LISTEN_PORT=80
EXPOSE 80