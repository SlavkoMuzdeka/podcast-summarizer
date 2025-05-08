"use client";

import ReactMarkdown from "react-markdown";

import { useMemo } from "react";
import { cn } from "@/lib/utils";

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

export function MarkdownRenderer({
  content,
  className,
}: MarkdownRendererProps) {
  const safeContent = useMemo(() => {
    if (!content) return "";
    return typeof content === "string" ? content : String(content);
  }, [content]);

  return (
    <div
      className={cn(
        "prose prose-slate dark:prose-invert max-w-none",
        className
      )}
    >
      <ReactMarkdown
        components={{
          h1: ({ node, ...props }) => (
            <h1
              className="text-2xl font-bold mb-4 text-slate-900 dark:text-white font-heading tracking-tight"
              {...props}
            />
          ),
          h2: ({ node, ...props }) => (
            <h2
              className="text-xl font-bold mb-3 text-slate-900 dark:text-white font-heading tracking-tight"
              {...props}
            />
          ),
          h3: ({ node, ...props }) => (
            <h3
              className="text-lg font-semibold mb-3 text-slate-900 dark:text-white font-heading tracking-tight"
              {...props}
            />
          ),
          p: ({ node, ...props }) => (
            <p
              className="mb-4 text-slate-700 dark:text-slate-300 leading-relaxed"
              {...props}
            />
          ),
          ul: ({ node, ...props }) => (
            <ul
              className="mb-4 pl-5 list-disc text-slate-700 dark:text-slate-300"
              {...props}
            />
          ),
          ol: ({ node, ...props }) => (
            <ol
              className="mb-4 pl-5 list-decimal text-slate-700 dark:text-slate-300"
              {...props}
            />
          ),
          li: ({ node, ...props }) => (
            <li
              className="mb-1 text-slate-700 dark:text-slate-300"
              {...props}
            />
          ),
          a: ({ node, ...props }) => (
            <a
              className="text-corporate-600 dark:text-corporate-400 hover:underline font-medium"
              {...props}
            />
          ),
          blockquote: ({ node, ...props }) => (
            <blockquote
              className="border-l-4 border-corporate-200 dark:border-corporate-800 pl-4 italic my-4 text-slate-600 dark:text-slate-400"
              {...props}
            />
          ),
          code: ({ node, ...props }) => (
            <code
              className="bg-slate-100 dark:bg-slate-800 px-1 py-0.5 rounded text-slate-900 dark:text-slate-100 font-mono text-sm"
              {...props}
            />
          ),
          pre: ({ node, ...props }) => (
            <pre
              className="bg-slate-100 dark:bg-slate-800 p-4 rounded-lg overflow-x-auto my-4 font-mono text-sm"
              {...props}
            />
          ),
        }}
      >
        {safeContent}
      </ReactMarkdown>
    </div>
  );
}
