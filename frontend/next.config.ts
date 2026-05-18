import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",       // Produces /out — served by Nginx
  reactStrictMode: true,
  trailingSlash: true,    // Required for try_files to resolve routes
  ...(process.env.NODE_ENV === "development" ? {
    async rewrites() {
      return [
        {
          source: "/api/:path*",
          destination: "http://127.0.0.1:8000/api/:path*",
        },
      ];
    }
  } : {}),
};

export default nextConfig;

