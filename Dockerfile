FROM node:22.16-bookworm-slim AS dependencies
WORKDIR /app
COPY package.json ./
RUN npm install --ignore-scripts --no-audit --no-fund

FROM dependencies AS build
WORKDIR /app
COPY . .
ARG DATABASE_URL=postgresql://mvqueen:build-only@127.0.0.1:5432/mvqueen_build
ENV DATABASE_URL=$DATABASE_URL
ENV MVQ_DATABASE_PROFILE=production
RUN npm run prisma:generate:production
RUN npm run build

FROM node:22.16-bookworm-slim AS runtime
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000

COPY --from=dependencies /app/node_modules ./node_modules
COPY --from=build /app/build ./build
COPY --from=build /app/app ./app
COPY --from=build /app/scripts ./scripts
COPY --from=build /app/prisma ./prisma
COPY --from=build /app/tsconfig.json ./tsconfig.json
COPY --from=build /app/package.json ./package.json

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:'+(process.env.PORT||3000)+'/healthz').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

CMD ["sh", "-c", "npm run db:migrate:production && npm run start"]
