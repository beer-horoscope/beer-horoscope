FROM nginx:latest

USER root

#RUN apk add --no-cache nginx-mod-http-perl
#RUN mkdir -p /var/cache/nginx
#RUN chown -R nginx:nginx /var/cache/nginx

# support running as arbitrary user which belogs to the root group
RUN chmod g+rwx /var/cache/nginx /var/run /var/log/nginx
EXPOSE 8081

COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf
COPY dist /usr/share/nginx/html

USER nginx

CMD ["/bin/sh", "-c", "exec nginx -g 'daemon off;';"]
WORKDIR /usr/share/nginx/html