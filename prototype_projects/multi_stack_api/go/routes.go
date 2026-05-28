package main

func registerRoutes(router Router) {
    router.GET("/go-users", listUsers)
    router.POST("/go-users", createUser)
    router.DELETE("/go-users/:id", deleteUser)
}
