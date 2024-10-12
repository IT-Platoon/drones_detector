# Frontend
FROM node:lts-alpine as build-stage

WORKDIR /app

COPY ./frontend/package*.json ./
RUN npm install

COPY ./frontend/ .
RUN npm run build

# Nginx
FROM nginx:1.19.2 as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/default.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]