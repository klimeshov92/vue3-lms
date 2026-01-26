# Стадия сборки Vue
#FROM node:20-alpine AS build

# Увеличиваем память Node
#ENV NODE_OPTIONS="--max-old-space-size=768"

# Рабочая директория
#WORKDIR /app

# Копируем package.json для кеша npm
#COPY package*.json ./

# Устанавливаем зависимости
#RUN npm install

# Копируем исходный код
#COPY . .

# Собираем production build (dist/)
#RUN npm run build


# Финальный образ — только nginx
FROM nginx:alpine

# Кладём ТОЛЬКО собранную статику
#COPY --from=build /app/dist /usr/share/nginx/html

# Копируем уже собранную статику
COPY dist /usr/share/nginx/html
