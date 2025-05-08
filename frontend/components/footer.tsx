"use client";

import { motion } from "framer-motion";

export default function Footer() {
  return (
    <motion.footer
      className="border-t border-slate-200 dark:border-slate-800 pt-10 pb-16 text-center mt-32"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ delay: 0.3 }}
    >
      <p className="text-slate-500 dark:text-slate-500">
        © 2025 Podcast Summarizer. All rights reserved.
      </p>
    </motion.footer>
  );
}
