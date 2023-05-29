# FROM nginx:1.18-alpine

# # Copy source
# COPY /dist/angular10 /usr/share/nginx/html

# # Copy configuration file
# COPY ./nginx-custom.conf /etc/nginx/conf.d/default.conf

# # Copy environment vars and execute the server
# COPY ./start.sh /start.sh

# # Set permissions
# RUN chmod +x /start.sh

FROM node:14 as angular-builder
COPY package.json *lock* /build/
WORKDIR /build
RUN npm install --force
COPY *.json *.js /build/
COPY src /build/src
RUN npx ng build --prod

FROM nginx:1.18-alpine
COPY --from=angular-builder /build/dist/angular10 /usr/share/nginx/html
COPY ./nginx-custom.conf /default.template.conf
COPY --chown=777 start.sh /start.sh
CMD ["sh", "/start.sh"]