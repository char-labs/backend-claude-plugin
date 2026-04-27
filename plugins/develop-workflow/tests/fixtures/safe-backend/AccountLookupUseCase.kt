package fixtures.safe

class AccountLookupUseCase(
    private val accountRepository: AccountRepository,
    private val authorization: AccountAuthorization,
) {
    fun handle(query: AccountLookupQuery): AccountView {
        authorization.requireCanRead(query.actorId, query.accountId)
        val account = accountRepository.findById(query.accountId)
            ?: throw AccountNotFoundException(query.accountId)
        return AccountView(account.id, account.displayName)
    }
}

data class AccountLookupQuery(
    val actorId: Long,
    val accountId: Long,
)

data class AccountView(
    val id: Long,
    val displayName: String,
)

interface AccountRepository {
    fun findById(id: Long): Account?
}

interface AccountAuthorization {
    fun requireCanRead(actorId: Long, accountId: Long)
}

data class Account(
    val id: Long,
    val displayName: String,
)

class AccountNotFoundException(id: Long) : RuntimeException("account not found: $id")
