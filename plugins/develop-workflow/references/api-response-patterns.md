# API 응답 Envelope 패턴

Spring/Kotlin REST API에서 `ApiResponse`, `ErrorResponse`, `ResponseBodyAdvice`, `RestControllerAdvice` 기반 공통 응답을 설계하거나 리뷰할 때 사용한다.

## 위치와 책임

- `support/response/ApiResponse.kt`: public response envelope data class.
- `support/error/ErrorResponse.kt`: 외부에 노출 가능한 error payload.
- `presentation/advice/ApiResponseAdvice.kt`: 정상 controller return value를 success envelope으로 감싼다.
- `presentation/advice/ApiExceptionAdvice.kt`: framework/domain/auth 예외를 fail envelope으로 변환한다.
- Controller는 transport DTO를 반환한다. `ApiResponse` 직접 반환은 이미 감싸진 응답이나 특별한 예외 상황에서만 허용한다.

## 기본 Envelope

```kotlin
data class ApiResponse<Data>(
    val success: Boolean,
    val status: Int,
    val data: Data? = null,
    val timestamp: LocalDateTime,
) {
    companion object {
        fun <Data> success(
            status: Int,
            data: Data,
        ): ApiResponse<Data> = ApiResponse(true, status, data, LocalDateTime.now())

        fun fail(
            status: Int,
            errorResponse: ErrorResponse,
        ): ApiResponse<ErrorResponse> = ApiResponse(false, status, errorResponse, LocalDateTime.now())
    }
}
```

```kotlin
data class ErrorResponse(
    val errorClassName: String,
    val message: String,
) {
    companion object {
        fun of(
            errorClassName: String,
            message: String,
        ) = ErrorResponse(errorClassName, message)
    }
}
```

## ResponseBodyAdvice 기준

- `@RestControllerAdvice(basePackages = ["{base-package}"])`로 API package 범위를 명시한다.
- 2xx 응답만 `ApiResponse.success(status, body)`로 감싼다.
- 다음 body는 그대로 둔다: `ApiResponse<*>`, `ErrorResponse`, `String`, null body.
- actuator, prometheus, health, file/streaming endpoint는 exclude list 또는 별도 조건으로 제외한다.
- `HttpStatus.resolve(status)`가 null이면 wrapper를 만들지 않는다.
- `String` response는 converter mismatch가 잦으므로 직접 wrapping하지 않는다.

## Exception Advice 기준

- `ResponseEntityExceptionHandler`를 상속하면 framework validation/method error를 override한다.
- `MethodArgumentNotValidException`, `ConstraintViolationException`, `MethodArgumentTypeMismatchException`, method not supported, domain error, authentication error, catch-all exception을 분리한다.
- domain error는 프로젝트의 `ErrorType` 같은 안정된 code/status/message를 사용한다.
- catch-all `Exception`/`RuntimeException`은 내부 log에는 원인을 남기되 외부 message는 `INTERNAL_SERVER_ERROR` 같은 안전한 문구로 제한한다.
- `ex.message!!` 같은 강제 unwrap은 피하고 fallback message를 둔다.
- 모든 실패 응답은 `ResponseEntity.status(status).body(ApiResponse.fail(status, errorResponse))` 형태로 status와 body status를 맞춘다.

## Controller 반환 규칙

- Controller는 `TokenResponse`, `MapCategoryAllResponse` 같은 plain response DTO를 반환한다.
- 생성 성공처럼 status만 바뀌면 `@ResponseStatus(HttpStatus.CREATED)`를 우선한다.
- header, redirect, streaming, file download, empty body처럼 HTTP detail이 핵심일 때만 `ResponseEntity`를 사용한다.
- Controller에서 `ApiResponse.success`를 반복 호출하지 않는다. wrapper 책임은 advice가 가진다.

## 문서와 테스트

- RestDocs/OpenAPI에는 envelope 필드 `success`, `status`, `data`, `timestamp`가 드러나야 한다.
- error response docs에는 `data.errorClassName`, `data.message` 또는 프로젝트가 정한 error payload 필드를 문서화한다.
- standalone MockMvc docs test는 advice가 등록되는지 확인한다. advice 없이 controller만 setup하면 실제 runtime envelope과 문서가 달라질 수 있다.
- advice branch가 바뀌면 already wrapped body, success wrapping, error mapping, excluded endpoint를 집중 테스트한다.
- 단순 data class 추가만 있고 business branch가 없으면 compile/static validation을 우선하고 테스트를 억지로 만들지 않는다.
