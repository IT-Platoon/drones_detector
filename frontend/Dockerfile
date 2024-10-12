FROM node:lts-alpine

ENV NODE_ENV="development"

RUN npm install -g http-server

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]
