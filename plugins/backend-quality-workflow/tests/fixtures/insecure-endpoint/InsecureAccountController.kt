package fixtures.insecure

import org.slf4j.LoggerFactory
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestHeader
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@RestController
class InsecureAccountController(
    private val jdbcTemplate: JdbcTemplate,
) {
    private val log = LoggerFactory.getLogger(javaClass)

    @GetMapping("/accounts")
    fun findAccount(
        @RequestParam accountId: String,
        @RequestHeader("Authorization") authorization: String,
    ): Map<String, Any?> {
        log.info("account lookup token={} accountId={}", authorization, accountId)

        return jdbcTemplate.queryForMap(
            "select id, owner_id, balance from accounts where id = '$accountId'",
        )
    }
}
