# 1단계: Build
FROM gradle:8.4.0-jdk21 AS build
WORKDIR /app

COPY . .
RUN chmod +x ./gradlew
RUN ./gradlew bootJar --no-daemon

# 2단계: Run
FROM eclipse-temurin:21-jdk-jammy
WORKDIR /app

COPY --from=build /app/build/libs/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
