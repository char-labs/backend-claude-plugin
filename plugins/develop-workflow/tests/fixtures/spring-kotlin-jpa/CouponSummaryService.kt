package fixtures.jpa

import jakarta.persistence.Entity
import jakarta.persistence.FetchType
import jakarta.persistence.Id
import jakarta.persistence.ManyToOne
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Service

@Entity
class Coupon(
    @Id
    val id: Long,
    @ManyToOne(fetch = FetchType.LAZY)
    val issuer: Issuer,
)

@Entity
class Issuer(
    @Id
    val id: Long,
    val name: String,
)

interface CouponRepository : JpaRepository<Coupon, Long>

@Service
class CouponSummaryService(
    private val couponRepository: CouponRepository,
) {
    fun summaries(): List<String> =
        couponRepository.findAll().map { coupon ->
            "${coupon.id}:${coupon.issuer.name}"
        }
}
