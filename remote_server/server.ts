import express from "express";
import path from "node:path";
import fs from "node:fs/promises";
import * as assert from "node:assert";

const app = express();
const port = 80;

app.use(express.json())

app.post("/log-entry", async (req, res) => {
  const { fileName, entry } = req.body
  const logsDir = process.env.LOGS_DIR!

  assert.ok(logsDir)
  assert.ok(fileName)
  assert.ok(entry)

  await fs.mkdir(logsDir, { recursive: true })
  const file = path.join(logsDir, fileName)
  const fileExists = await fs.exists(file)
  if (!fileExists) {
    await fs.appendFile(file, 'Timestamp,Cpu usage,Mem usage,Disk usage\n', { encoding: 'utf-8' })
  }
  await fs.appendFile(file, `${entry}`, { encoding: 'utf-8' })

  res.send("Done");
});

app.listen(port, () => {
  console.log(`Listening on port ${port}...`);
});
