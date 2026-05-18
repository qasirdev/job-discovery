import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",       // Produces /out — served by Nginx
  reactStrictMode: true,
  trailingSlash: true,    // Required for try_files to resolve routes
};

export default nextConfig;
