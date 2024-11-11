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
  const filePath = path.join(logsDir, fileName)
  const fileExists = await fs.exists(filePath)
  if (!fileExists) {
    await fs.writeFile(filePath, '[]', { encoding: 'utf-8' })
  }

  const jsonFile = JSON.parse(await fs.readFile(filePath, { encoding: 'utf-8' })) as any[]
  jsonFile.push(entry)

  await fs.writeFile(filePath, JSON.stringify(jsonFile, null, 4), { encoding: 'utf-8' })

  res.send("Done");
});

app.listen(port, () => {
  console.log(`Listening on port ${port}...`);
});
