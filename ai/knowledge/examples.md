# 📚 Spring Boot Code Review - Good vs Bad Examples

## 1. NPE 風險處理

### ❌ Bad Example

```java
public String getUserName(Long userId) {
    User user = userRepository.findById(userId);
    return user.getName().toUpperCase(); // NPE 風險！
}

public int getTotalPrice(Order order) {
    return order.getItems().stream()
        .mapToInt(Item::getPrice)
        .sum(); // getItems() 可能為 null
}
```

### ✅ Good Example

```java
public String getUserName(Long userId) {
    User user = userRepository.findById(userId);
    if (user == null || user.getName() == null) {
        return "Unknown";
    }
    return user.getName().toUpperCase();
}

// 或使用 Optional
public String getUserName(Long userId) {
    return userRepository.findById(userId)
        .map(User::getName)
        .map(String::toUpperCase)
        .orElse("Unknown");
}

public int getTotalPrice(Order order) {
    if (order == null || order.getItems() == null) {
        return 0;
    }
    return order.getItems().stream()
        .mapToInt(Item::getPrice)
        .sum();
}
```

---

## 2. Optional 濫用 .get()

### ❌ Bad Example

```java
public User getUser(Long id) {
    Optional<User> user = userRepository.findById(id);
    return user.get(); // 沒檢查就 get() 會拋 NoSuchElementException
}
```

### ✅ Good Example

```java
public User getUser(Long id) {
    return userRepository.findById(id)
        .orElseThrow(() -> new UserNotFoundException("User not found: " + id));
}

// 或
public User getUser(Long id) {
    return userRepository.findById(id)
        .orElse(null);
}
```

---

## 3. equals 誤用 ==

### ❌ Bad Example

```java
public boolean isSameUser(String userName1, String userName2) {
    return userName1 == userName2; // ❌ 比較記憶體位址
}

public boolean isPriceEqual(BigDecimal price1, BigDecimal price2) {
    return price1 == price2; // ❌ 永遠 false
}

public boolean isAdmin(User user) {
    return user.getRole() == "ADMIN"; // ❌ String 用 ==
}
```

### ✅ Good Example

```java
public boolean isSameUser(String userName1, String userName2) {
    return Objects.equals(userName1, userName2); // ✅ 處理 null
}

public boolean isPriceEqual(BigDecimal price1, BigDecimal price2) {
    if (price1 == null || price2 == null) {
        return false;
    }
    return price1.compareTo(price2) == 0; // ✅ 使用 compareTo
}

public boolean isAdmin(User user) {
    return "ADMIN".equals(user.getRole()); // ✅ 常數在前避免 NPE
}
```

---

## 4. Magic Number

### ❌ Bad Example

```java
public boolean isVip(User user) {
    return user.getLevel() >= 5; // 5 是什麼意思？
}

public void processOrder(Order order) {
    if (order.getStatus() == 3) { // 3 是什麼狀態？
        // ...
    }
}
```

### ✅ Good Example

```java
public class UserLevel {
    public static final int VIP_THRESHOLD = 5;
}

public boolean isVip(User user) {
    return user.getLevel() >= UserLevel.VIP_THRESHOLD;
}

public enum OrderStatus {
    PENDING(1), PROCESSING(2), COMPLETED(3), CANCELLED(4);
    private final int code;
    // ...
}

public void processOrder(Order order) {
    if (order.getStatus() == OrderStatus.COMPLETED.getCode()) {
        // ...
    }
}
```

---

## 5. 三層架構違反

### ❌ Bad Example - Controller 有業務邏輯

```java
@RestController
public class OrderController {
    @Autowired
    private OrderRepository orderRepository;

    @PostMapping("/order")
    public Result createOrder(@RequestBody OrderRequest request) {
        // ❌ Controller 直接操作 DB
        Order order = new Order();
        order.setUserId(request.getUserId());
        order.setTotalPrice(request.getItems().stream()
            .mapToInt(Item::getPrice).sum()); // ❌ 業務邏輯
        orderRepository.save(order);
        return Result.success(order);
    }
}
```

### ✅ Good Example - 三層分離

```java
@RestController
public class OrderController {
    @Autowired
    private OrderService orderService;

    @PostMapping("/order")
    public Result<OrderDTO> createOrder(@Valid @RequestBody OrderRequest request) {
        OrderDTO order = orderService.createOrder(request);
        return Result.success(order);
    }
}

@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;

    @Transactional
    public OrderDTO createOrder(OrderRequest request) {
        // ✅ 業務邏輯在 Service
        int totalPrice = calculateTotalPrice(request.getItems());
        Order order = new Order();
        order.setUserId(request.getUserId());
        order.setTotalPrice(totalPrice);
        order.setStatus(OrderStatus.PENDING);

        Order saved = orderRepository.save(order);
        return OrderDTO.from(saved);
    }

    private int calculateTotalPrice(List<OrderItem> items) {
        return items.stream()
            .mapToInt(OrderItem::getPrice)
            .sum();
    }
}
```

---

## 6. 方法過長 & SRP 違反

### ❌ Bad Example

```java
public void processOrder(Order order) {
    // 驗證訂單
    if (order.getItems() == null || order.getItems().isEmpty()) {
        throw new IllegalArgumentException("Items cannot be empty");
    }

    // 計算價格
    int totalPrice = 0;
    for (OrderItem item : order.getItems()) {
        totalPrice += item.getPrice() * item.getQuantity();
    }

    // 檢查庫存
    for (OrderItem item : order.getItems()) {
        Product product = productRepository.findById(item.getProductId());
        if (product.getStock() < item.getQuantity()) {
            throw new OutOfStockException("Product out of stock");
        }
    }

    // 扣庫存
    for (OrderItem item : order.getItems()) {
        Product product = productRepository.findById(item.getProductId());
        product.setStock(product.getStock() - item.getQuantity());
        productRepository.save(product);
    }

    // 建立訂單
    order.setTotalPrice(totalPrice);
    order.setStatus(OrderStatus.PENDING);
    orderRepository.save(order);

    // 發送通知
    String message = "Your order " + order.getId() + " is created";
    notificationService.send(order.getUserId(), message);
}
```

### ✅ Good Example - 拆分方法

```java
@Transactional
public void processOrder(Order order) {
    validateOrder(order);
    checkStock(order.getItems());
    deductStock(order.getItems());

    int totalPrice = calculateTotalPrice(order.getItems());
    order.setTotalPrice(totalPrice);
    order.setStatus(OrderStatus.PENDING);

    Order saved = orderRepository.save(order);
    sendOrderNotification(saved);
}

private void validateOrder(Order order) {
    if (order.getItems() == null || order.getItems().isEmpty()) {
        throw new IllegalArgumentException("Items cannot be empty");
    }
}

private int calculateTotalPrice(List<OrderItem> items) {
    return items.stream()
        .mapToInt(item -> item.getPrice() * item.getQuantity())
        .sum();
}

private void checkStock(List<OrderItem> items) {
    for (OrderItem item : items) {
        Product product = productRepository.findById(item.getProductId())
            .orElseThrow(() -> new ProductNotFoundException(item.getProductId()));
        if (product.getStock() < item.getQuantity()) {
            throw new OutOfStockException("Product out of stock: " + product.getName());
        }
    }
}

private void deductStock(List<OrderItem> items) {
    for (OrderItem item : items) {
        productRepository.decreaseStock(item.getProductId(), item.getQuantity());
    }
}

private void sendOrderNotification(Order order) {
    String message = String.format("Your order %s is created", order.getId());
    notificationService.send(order.getUserId(), message);
}
```

---

## 7. 巢狀 if 過深

### ❌ Bad Example

```java
public void updateUser(User user) {
    if (user != null) {
        if (user.getName() != null) {
            if (user.getName().length() > 0) {
                if (user.getAge() >= 18) {
                    if (user.getEmail() != null) {
                        userRepository.save(user);
                    } else {
                        throw new ValidationException("Email required");
                    }
                } else {
                    throw new ValidationException("Must be 18+");
                }
            } else {
                throw new ValidationException("Name cannot be empty");
            }
        } else {
            throw new ValidationException("Name required");
        }
    } else {
        throw new ValidationException("User cannot be null");
    }
}
```

### ✅ Good Example - Early Return

```java
public void updateUser(User user) {
    if (user == null) {
        throw new ValidationException("User cannot be null");
    }
    if (user.getName() == null) {
        throw new ValidationException("Name required");
    }
    if (user.getName().isEmpty()) {
        throw new ValidationException("Name cannot be empty");
    }
    if (user.getAge() < 18) {
        throw new ValidationException("Must be 18+");
    }
    if (user.getEmail() == null) {
        throw new ValidationException("Email required");
    }

    userRepository.save(user);
}
```

---

## 8. N+1 Query 問題

### ❌ Bad Example

```java
public List<OrderDTO> getOrders() {
    List<Order> orders = orderRepository.findAll();

    return orders.stream()
        .map(order -> {
            // ❌ 每個 order 都查一次 DB（N+1 query）
            User user = userRepository.findById(order.getUserId()).get();
            OrderDTO dto = new OrderDTO();
            dto.setOrderId(order.getId());
            dto.setUserName(user.getName());
            return dto;
        })
        .collect(Collectors.toList());
}
```

### ✅ Good Example - 批次查詢

```java
public List<OrderDTO> getOrders() {
    List<Order> orders = orderRepository.findAll();

    // ✅ 一次查詢所有 user
    Set<Long> userIds = orders.stream()
        .map(Order::getUserId)
        .collect(Collectors.toSet());

    Map<Long, User> userMap = userRepository.findByIdIn(userIds).stream()
        .collect(Collectors.toMap(User::getId, user -> user));

    return orders.stream()
        .map(order -> {
            User user = userMap.get(order.getUserId());
            OrderDTO dto = new OrderDTO();
            dto.setOrderId(order.getId());
            dto.setUserName(user != null ? user.getName() : "Unknown");
            return dto;
        })
        .collect(Collectors.toList());
}

// 或使用 JOIN
@Query("SELECT o FROM Order o JOIN FETCH o.user")
List<Order> findAllWithUser();
```

---

## 9. 無 limit 查詢

### ❌ Bad Example

```java
public List<User> getAllUsers() {
    return userRepository.findAll(); // ❌ 可能回傳百萬筆
}

public List<Order> searchOrders(String keyword) {
    return orderRepository.findByKeyword(keyword); // ❌ 沒分頁
}
```

### ✅ Good Example

```java
public Page<User> getAllUsers(int page, int size) {
    Pageable pageable = PageRequest.of(page, size);
    return userRepository.findAll(pageable); // ✅ 分頁查詢
}

public List<Order> searchOrders(String keyword) {
    PageRequest pageRequest = PageRequest.of(0, 100); // ✅ 最多 100 筆
    return orderRepository.findByKeyword(keyword, pageRequest).getContent();
}
```

---

## 10. 命名不清楚

### ❌ Bad Example

```java
public void process(User u) {
    String s = u.getName();
    int a = u.getAge();
    boolean b = check(a);
    if (b) {
        save(u);
    }
}

public boolean check(int x) {
    return x >= 18;
}
```

### ✅ Good Example

```java
public void processUserRegistration(User user) {
    String userName = user.getName();
    int userAge = user.getAge();
    boolean isAdult = isAdultAge(userAge);

    if (isAdult) {
        saveUser(user);
    }
}

public boolean isAdultAge(int age) {
    return age >= ADULT_AGE_THRESHOLD;
}

// Boolean 命名範例
private boolean isActive;
private boolean hasPermission;
private boolean canEdit;
private boolean shouldRetry;
```
