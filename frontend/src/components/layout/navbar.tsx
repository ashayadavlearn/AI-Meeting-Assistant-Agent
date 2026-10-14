"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { Bot, Activity, FileText } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { API_BASE_URL, API_DOCS_URL } from "@/lib/api-config";

interface HealthCheckData {
  status: string;
  version: string;
  environment: string;
  uptime_seconds: number;
}

export function Navbar() {
  const { data: health, isError, isLoading } = useQuery<HealthCheckData>({
    queryKey: ["backend-health"],
    queryFn: async () => {
      const res = await fetch(`${API_BASE_URL}/health`);
      if (!res.ok) throw new Error("Backend offline");
      return res.json();
    },
    refetchInterval: 10000,
    retry: false,
  });

  return (
    <header className="sticky top-0 z-50 w-full border-b border-zinc-800/80 bg-zinc-950/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 shadow-md shadow-indigo-500/25">
            <Bot className="h-5 w-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-base font-bold tracking-tight text-white">Meeting Assistant</span>
              <Badge variant="indigo" className="text-[10px] uppercase font-mono tracking-wider">
                v0.1.0
              </Badge>
            </div>
            <p className="text-xs text-zinc-400">Enterprise AI MoM & Action Agent</p>
          </div>
        </div>

        {/* Center Nav Items */}
        <nav className="hidden md:flex items-center gap-1">
          <Link href="/" className="px-3 py-1.5 text-sm font-medium text-white hover:text-indigo-400 transition-colors rounded-md bg-zinc-900/60 border border-zinc-800/80">
            Overview
          </Link>
          <span className="px-3 py-1.5 text-sm font-medium text-zinc-400 hover:text-zinc-200 transition-colors cursor-not-allowed">
            Meetings (Phase 4)
          </span>
          <span className="px-3 py-1.5 text-sm font-medium text-zinc-400 hover:text-zinc-200 transition-colors cursor-not-allowed">
            Tasks (Phase 9)
          </span>
          <span className="px-3 py-1.5 text-sm font-medium text-zinc-400 hover:text-zinc-200 transition-colors cursor-not-allowed">
            Chat (Phase 8)
          </span>
        </nav>

        {/* Right Status & Actions */}
        <div className="flex items-center gap-3">
          {/* Backend Status Indicator */}
          <div className="hidden sm:flex items-center gap-2 rounded-full bg-zinc-900/80 border border-zinc-800 px-3 py-1">
            <Activity className="h-3.5 w-3.5 text-zinc-400" />
            <span className="text-xs text-zinc-400">API:</span>
            {isLoading ? (
              <span className="text-xs text-zinc-400 animate-pulse">Checking...</span>
            ) : isError || !health ? (
              <div className="flex items-center gap-1.5">
                <span className="relative flex h-2 w-2">
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500" />
                </span>
                <span className="text-xs font-medium text-rose-400">Offline</span>
              </div>
            ) : (
              <div className="flex items-center gap-1.5">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
                </span>
                <span className="text-xs font-medium text-emerald-400">Live ({health.environment})</span>
              </div>
            )}
          </div>

          {/* Swagger link */}
          <a
            href={API_DOCS_URL}
            target="_blank"
            rel="noopener noreferrer"
          >
            <Button variant="outline" size="sm" className="hidden sm:inline-flex">
              <FileText className="h-3.5 w-3.5 text-indigo-400" />
              Swagger Docs
            </Button>
          </a>
        </div>
      </div>
    </header>
  );
}
