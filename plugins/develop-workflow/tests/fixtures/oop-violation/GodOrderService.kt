package fixtures.oop

import java.net.URI
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse

class GodOrderService(
    private val orderRepository: OrderRepository,
) {
    fun submit(userId: Long, orderId: Long, rawAddress: String): String {
        if (rawAddress.isBlank()) {
            throw IllegalArgumentException("bad address")
        }

        val order = orderRepository.find(orderId)
        if (order.userId != userId) {
            throw IllegalStateException("not owner")
        }

        order.status = "SUBMITTED"
        orderRepository.save(order)

        val client = HttpClient.newHttpClient()
        val request = HttpRequest.newBuilder(URI.create("https://shipper.example/orders/$orderId"))
            .POST(HttpRequest.BodyPublishers.ofString(rawAddress))
            .build()
        val response = client.send(request, HttpResponse.BodyHandlers.ofString())

        return "order=${order.id};status=${order.status};shipping=${response.body()}"
    }
}

data class Order(
    val id: Long,
    val userId: Long,
    var status: String,
)

interface OrderRepository {
    fun find(id: Long): Order
    fun save(order: Order)
}
