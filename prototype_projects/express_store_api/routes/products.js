const express = require("express");

const router = express.Router();

router.get("/products", (req, res) => {
  const category = req.query.category;
  const requestId = req.get("x-request-id");

  return res.status(200).json({
    items: [],
    category,
    requestId,
  });
});

router.get("/products/:productId", (req, res) => {
  const productId = req.params.productId;
  if (!productId) {
    return res.status(400).json({ message: "productId is required" });
  }

  return res.status(404).json({ error: "Product not found" });
});

router.post("/products", (req, res) => {
  const { name, price, stock } = req.body;
  if (!name) {
    return res.status(400).json({ message: "name is required" });
  }

  return res.status(201).json({
    id: "prod_1",
    name,
    price,
    stock,
  });
});

router.patch("/products/:productId", function (req, res) {
  const productId = req.params.productId;
  const price = req.body.price;

  return res.status(200).json({
    id: productId,
    price,
  });
});

module.exports = router;
