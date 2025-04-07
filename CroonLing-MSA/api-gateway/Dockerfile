# 1단계: Build (Gradle로 bootJar 빌드)
FROM gradle:8.4.0-jdk21 AS build
WORKDIR /app

COPY build.gradle settings.gradle ./
COPY src ./src

RUN gradle bootJar --no-daemon

# 2단계: Run (JAR 실행)
FROM eclipse-temurin:21-jdk-jammy
WORKDIR /app

COPY --from=build /app/build/libs/*.jar app.jar
EXPOSE 8000
ENTRYPOINT ["java", "-jar", "app.jar"]