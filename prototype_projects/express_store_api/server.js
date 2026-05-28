const express = require("express");
const productRoutes = require("./routes/products");

const app = express();

app.use(express.json());
app.use("/api/v1", productRoutes);

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

module.exports = app;
