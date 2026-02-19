import type { NextConfig } from "next";
import path from "path";
import fs from "fs";

// Load environment variables from parent directory (.env)
const parentEnvPath = path.resolve(__dirname, "..", ".env");

if (fs.existsSync(parentEnvPath)) {
  const envContent = fs.readFileSync(parentEnvPath, "utf-8");
  envContent.split("\n").forEach((line) => {
    const [key, ...value] = line.split("=");
    if (key && value.length > 0) {
      const skipped = line.trim().startsWith("#");
      if (!skipped) {
        const val = value.join("=").trim();
        const cleanKey = key.trim();
        // Load NEXT_PUBLIC_ variables so they are available to the browser
        if (cleanKey.startsWith("NEXT_PUBLIC_")) {
          process.env[cleanKey] = val;
        }
      }
    }
  });
}

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;
