"use client";

import Footer from "@/components/footer";

import { Hero } from "@/components/hero";
import { ThemeToggle } from "@/components/theme-toggle";
import { FeaturesSection } from "@/components/features-section";
import { SummarizationSection } from "@/components/summarization-section";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-white dark:from-gray-950 dark:to-slate-900 overflow-hidden">
      {/* Theme Toggle */}
      <ThemeToggle />

      {/* Main section */}
      <div className="relative pt-20 pb-2 md:pt-32">
        <div className="container mx-auto px-6 max-w-screen-xl">
          <Hero />
          <SummarizationSection />
          <FeaturesSection />
          <Footer />
        </div>
      </div>
    </main>
  );
}
