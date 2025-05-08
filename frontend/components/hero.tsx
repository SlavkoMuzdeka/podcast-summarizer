"use client";

import { motion } from "framer-motion";
import { Sparkles, ArrowRight } from "lucide-react";
import { fadeIn, staggerContainer } from "@/lib/utils";

export function Hero() {
  return (
    <motion.div
      className="flex flex-col items-center text-center mb-16 md:mb-24"
      initial="hidden"
      animate="visible"
      variants={staggerContainer}
    >
      <motion.div
        className="inline-flex items-center px-3 py-1 mb-6 text-xs font-medium rounded-full bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700"
        variants={fadeIn}
        custom={0}
      >
        <Sparkles className="h-3 w-3 mr-2 text-corporate-500" />
        AI-Powered Tool
      </motion.div>

      <motion.h1
        className="text-4xl md:text-6xl font-bold tracking-tight text-slate-900 dark:text-white mb-6 max-w-4xl font-heading"
        variants={fadeIn}
        custom={1}
      >
        Transform{" "}
        <span className="text-corporate-600 dark:text-corporate-500 relative">
          podcasts
          <span className="absolute bottom-1 left-0 w-full h-1 bg-corporate-200 dark:bg-corporate-800 rounded-full"></span>
        </span>{" "}
        into actionable insights
      </motion.h1>

      <motion.p
        className="text-lg md:text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto mb-8"
        variants={fadeIn}
        custom={2}
      >
        Our AI-powered platform converts lengthy podcast episodes into concise,
        accurate summaries for busy professionals.
      </motion.p>

      <motion.div
        className="flex flex-col sm:flex-row gap-4 mt-2"
        variants={fadeIn}
        custom={3}
      >
        <motion.a
          href="#summarizer"
          className="inline-flex items-center justify-center px-6 py-3 rounded-lg bg-corporate-600 hover:bg-corporate-700 text-white font-medium transition-colors duration-200 shadow-lg hover:shadow-xl hover:shadow-corporate-200 dark:hover:shadow-none"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Start Summarizing
          <ArrowRight className="ml-2 h-4 w-4" />
        </motion.a>
        <motion.a
          href="#features"
          className="inline-flex items-center justify-center px-6 py-3 rounded-lg bg-white hover:bg-slate-50 text-slate-800 font-medium border border-slate-200 hover:border-slate-300 transition-colors duration-200 shadow-sm dark:bg-slate-800 dark:hover:bg-slate-700 dark:text-slate-200 dark:border-slate-700 dark:hover:border-slate-600"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Explore Features
        </motion.a>
      </motion.div>
    </motion.div>
  );
}
