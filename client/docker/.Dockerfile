FROM node:12-alpine

COPY package.json package.json
RUN apk add --no-cache libc6-compat
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
#RUN npm install next react react-dom
COPY . .

#WORKDIR /client
ENV HTTPS=true
ENV DISABLE_ESLINT_PLUGIN=true
#RUN ["next", "build"]
#CMD ["next", "start"]
#ENV PORT=443
#ENV HOST=0.0.0.0
RUN ["yarn", "build"]
CMD ["yarn", "start"]
