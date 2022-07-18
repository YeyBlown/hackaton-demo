FROM node:16-alpine

COPY package.json package.json
RUN apk add --no-cache libc6-compat
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .

#WORKDIR /client
#RUN ["next", "build"]
#CMD ["next", "start"]
CMD ["yarn", "run", "dev"]