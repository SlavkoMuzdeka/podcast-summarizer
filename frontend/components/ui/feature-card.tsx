import React from "react";
import { motion } from "framer-motion";
import { featureCardVariants } from "../../lib/animations";

interface FeatureCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  color: string;
  index: number;
}

export function FeatureCard({
  title,
  description,
  icon,
  color,
  index,
}: FeatureCardProps) {
  return (
    <motion.div
      className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md border border-slate-100 dark:border-slate-700 relative overflow-hidden"
      variants={featureCardVariants}
      whileHover="hover"
      custom={index}
    >
      <div
        className={`absolute top-0 right-0 w-24 h-24 bg-${color}-100 dark:bg-${color}-900/20 rounded-bl-full -mr-8 -mt-8 opacity-50`}
      />
      <div
        className={`w-12 h-12 bg-${color}-50 dark:bg-${color}-900/30 rounded-lg flex items-center justify-center mb-4 relative z-10`}
      >
        {icon}
      </div>
      <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2 relative z-10">
        {title}
      </h3>
      <p className="text-slate-600 dark:text-slate-400 relative z-10">
        {description}
      </p>
    </motion.div>
  );
}
