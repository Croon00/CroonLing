# 1단계
FROM gradle:8.4.0-jdk21 AS build
WORKDIR /app

COPY build.gradle.kts settings.gradle.kts ./
COPY src ./src

RUN gradle bootJar --no-daemon

# 2단계
FROM eclipse-temurin:21-jdk-jammy
WORKDIR /app

COPY --from=build /app/build/libs/*.jar app.jar
EXPOSE 8888
ENTRYPOINT ["java", "-jar", "app.jar"]
