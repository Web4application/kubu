FROM node:18-alpine AS build

WORKDIR /app

COPY ./kubu-hai-ui/package.json ./kubu-hai-ui/package-lock.json* /app/
RUN npm install

COPY ./kubu-hai-ui /app

RUN npm run build

# Production image
FROM nginx:stable-alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
