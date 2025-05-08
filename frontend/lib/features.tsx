import type { ReactNode } from "react";
import {
  Zap,
  Clock,
  BookOpen,
  FileText,
  Headphones,
  MessageSquare,
} from "lucide-react";

export interface Feature {
  title: string;
  description: string;
  icon: ReactNode;
  color: string;
}

export const features: Feature[] = [
  {
    title: "Multi-Source Support",
    description:
      "Process content from YouTube videos and podcast RSS feeds from various platforms.",
    icon: (
      <Headphones className="h-6 w-6 text-corporate-600 dark:text-corporate-400" />
    ),
    color: "corporate",
  },
  {
    title: "AI-Powered Summaries",
    description:
      "Convert lengthy podcast episodes into concise, readable summaries.",
    icon: (
      <Zap className="h-6 w-6 text-corporate-600 dark:text-corporate-400" />
    ),
    color: "corporate",
  },
  {
    title: "Key Points Extraction",
    description:
      "Automatically identify and highlight the most important takeaways from each episode.",
    icon: (
      <BookOpen className="h-6 w-6 text-corporate-600 dark:text-corporate-400" />
    ),
    color: "corporate",
  },
  {
    title: "Time-Saving Tool",
    description:
      "Get the essence of hour-long podcasts in just minutes of reading.",
    icon: (
      <Clock className="h-6 w-6 text-corporate-600 dark:text-corporate-400" />
    ),
    color: "corporate",
  },
  {
    title: "Content Analysis",
    description:
      "Identify speakers and their key contributions to the discussion.",
    icon: (
      <MessageSquare className="h-6 w-6 text-corporate-600 dark:text-corporate-400" />
    ),
    color: "corporate",
  },
  {
    title: "Easy Sharing",
    description:
      "Share summaries with colleagues or export them for later reference.",
    icon: (
      <FileText className="h-6 w-6 text-corporate-600 dark:text-corporate-400" />
    ),
    color: "corporate",
  },
];
