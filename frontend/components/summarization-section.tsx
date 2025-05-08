"use client";

import { motion } from "framer-motion";
import { PodcastSummarizer } from "@/components/podcast-summarizer";

export function SummarizationSection() {
  return (
    <motion.div
      id="summarizer"
      className="scroll-mt-24"
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7, delay: 0.5 }}
    >
      <PodcastSummarizer />
    </motion.div>
  );
}
