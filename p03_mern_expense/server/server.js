// ===== M E R N  —  Express + Node.js REST API with MongoDB =====
import express from "express";
import mongoose from "mongoose";
import cors from "cors";
import "dotenv/config";

const app = express();
app.use(cors());
app.use(express.json());

// ---- M: MongoDB model ----
const Expense = mongoose.model(
  "Expense",
  new mongoose.Schema(
    {
      title: { type: String, required: true, trim: true },
      amount: { type: Number, required: true, min: 1 },
      category: { type: String, enum: ["Food", "Travel", "Shopping", "Bills", "Education", "Fun"], default: "Food" },
      date: { type: Date, default: Date.now },
    },
    { timestamps: true }
  )
);

// ---- E: Express REST routes ----
app.get("/api/expenses", async (req, res) => {
  res.json(await Expense.find().sort({ date: -1 }));
});

app.post("/api/expenses", async (req, res) => {
  try {
    res.status(201).json(await Expense.create(req.body));
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.delete("/api/expenses/:id", async (req, res) => {
  await Expense.findByIdAndDelete(req.params.id);
  res.json({ ok: true });
});

// Summary using MongoDB aggregation (category-wise total)
app.get("/api/summary", async (req, res) => {
  const byCategory = await Expense.aggregate([
    { $group: { _id: "$category", total: { $sum: "$amount" }, count: { $sum: 1 } } },
    { $sort: { total: -1 } },
  ]);
  res.json(byCategory);
});

app.get("/", (req, res) => res.send("SpendSmart API is running 🚀"));

// ---- N: Node server ----
const PORT = process.env.PORT || 5000;
mongoose
  .connect(process.env.MONGO_URI || "mongodb://127.0.0.1:27017/spendsmart")
  .then(() => {
    console.log("✅ MongoDB connected");
    app.listen(PORT, () => console.log(`🚀 API on http://localhost:${PORT}`));
  })
  .catch((e) => console.error("❌ MongoDB error:", e.message));
