import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import svgr from "vite-plugin-svgr";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss(), react(), svgr()],
  optimizeDeps: {
    include: ["react", "react-dom", "@tanstack/react-query"],
  },
});
