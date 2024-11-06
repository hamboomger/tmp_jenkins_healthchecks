import express from "express";
import path from "node:path";
import fs from "node:fs";

const app = express();
const port = 8080;

app.use(express.json())

app.post("/log-entry", (req, res) => {
  const LOGS_DIR = path.join('some', 'path')
  const { fileName, entry } = req.body

  res.send("Hello World!");
});

app.listen(port, () => {
  console.log(`Listening on port ${port}...`);
});
