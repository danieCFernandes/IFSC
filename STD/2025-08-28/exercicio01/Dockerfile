FROM gradle:8.14.3-jdk21-alpine AS build

WORKDIR /codigo-java

COPY . .

RUN gradle installDist

FROM eclipse-temurin:21-jre-alpine

WORKDIR /aplicacao

COPY --from=build /codigo-java/app/build/install/app /aplicacao

ENTRYPOINT [ "./bin/app" ]