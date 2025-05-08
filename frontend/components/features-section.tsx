"use client";

import { motion } from "framer-motion";
import { features } from "@/lib/features";
import { fadeIn, staggerContainer, featureCardVariants } from "@/lib/utils";

export function FeaturesSection() {
  return (
    <motion.div
      id="features"
      className="mt-32 scroll-mt-24"
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-100px" }}
      variants={staggerContainer}
    >
      <motion.div className="text-center mb-16" variants={fadeIn} custom={0}>
        <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4 font-heading">
          Key Features
        </h2>
        <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
          Our platform makes podcast content more accessible with these powerful
          features
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {features.map((feature, index) => (
          <motion.div
            key={index}
            className={`bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md border border-slate-100 dark:border-slate-700 relative overflow-hidden`}
            variants={featureCardVariants}
            whileHover="hover"
            custom={index}
          >
            <div
              className={`absolute top-0 right-0 w-24 h-24 bg-corporate-100 dark:bg-corporate-900/20 rounded-bl-full -mr-8 -mt-8 opacity-50`}
            ></div>
            <div
              className={`w-12 h-12 bg-corporate-50 dark:bg-corporate-900/30 rounded-lg flex items-center justify-center mb-4 relative z-10`}
            >
              {feature.icon}
            </div>
            <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2 relative z-10 font-heading">
              {feature.title}
            </h3>
            <p className="text-slate-600 dark:text-slate-400 relative z-10">
              {feature.description}
            </p>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
