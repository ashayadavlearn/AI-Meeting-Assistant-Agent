"use client";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  Server,
  Database,
  Cpu,
  Layers,
  Sparkles,
  CheckCircle,
  Clock,
  Terminal,
  ShieldCheck,
  RefreshCw,
  ExternalLink,
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { API_BASE_URL, API_DOCS_URL } from "@/lib/api-config";

interface HealthData {
  status: string;
  version: string;
  environment: string;
  uptime_seconds: number;
  timestamp: string;
}

export default function HomePage() {
  const [testResult, setTestResult] = useState<string | null>(null);
  const [testing, setTesting] = useState(false);

  const { data: health } = useQuery<HealthData>({
    queryKey: ["health-full"],
    queryFn: async () => {
      const res = await fetch(`${API_BASE_URL}/health`);
      if (!res.ok) throw new Error("API not reachable");
      return res.json();
    },
    refetchInterval: 15000,
    retry: 1,
  });

  const runApiTest = async () => {
    setTesting(true);
    setTestResult(null);
    try {
      const start = performance.now();
      const res = await fetch(`${API_BASE_URL}/health`);
      const elapsed = (performance.now() - start).toFixed(2);
      const reqId = res.headers.get("x-request-id") || "N/A";
      const data = await res.json();
      setTestResult(
        JSON.stringify(
          {
            status: res.status,
            latency: `${elapsed}ms`,
            x_request_id: reqId,
            body: data,
          },
          null,
          2
        )
      );
    } catch (err: unknown) {
      setTestResult(
        JSON.stringify(
          {
            error: "Failed to connect to backend",
            hint: `Make sure the backend is running on ${API_BASE_URL}`,
            details: String(err),
          },
          null,
          2
        )
      );
    } finally {
      setTesting(false);
    }
  };

  const phases = [
    { num: 1, title: "Design & Architecture", desc: "Requirements, ER diagram, pipeline specs, API design", status: "completed" },
    { num: 2, title: "Project Initialization", desc: "FastAPI app factory, DI, Next.js 15, logging, error envelopes", status: "active" },
    { num: 3, title: "Auth, Database & Models", desc: "SQLAlchemy 2.0, Alembic, JWT tokens, audit logs, repos", status: "pending" },
    { num: 4, title: "Meeting & Transcript APIs", desc: "Multipart upload, StorageBackend, validation, job runner", status: "pending" },
    { num: 5, title: "Gemini 2.5 Flash Pipeline", desc: "LangGraph nodes, structured MoM, tasks, risks & emails", status: "pending" },
    { num: 6, title: "Faster-Whisper STT", desc: "Speech-to-text adapter, audio chunking, progress updates", status: "pending" },
    { num: 7, title: "FAISS & Semantic Search", desc: "SentenceTransformers, per-user FAISS index, search API", status: "pending" },
    { num: 8, title: "Chat With Meetings (RAG)", desc: "LangChain retrieval, source citation, structured queries", status: "pending" },
    { num: 9, title: "Task Manager & Dashboard", desc: "Task CRUD, status transitions, deadlines, calendar stats", status: "pending" },
    { num: 10, title: "Rich Frontend Experience", desc: "Notion/Fireflies UI, Kanban board, audio player, chat UI", status: "pending" },
    { num: 11, title: "Testing & Hardening", desc: "Coverage, request tracing, rate limiting, security review", status: "pending" },
    { num: 12, title: "Deployment & Demo Pitch", desc: "Docker, Railway, Neon, Vercel, demo scripts & presentation", status: "pending" },
  ];

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8 space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 rounded-full border border-indigo-500/30 bg-indigo-500/10 px-3 py-1 text-xs font-semibold text-indigo-400">
          <Sparkles className="h-3.5 w-3.5" />
          AI/ML Hackathon Prototype &bull; Phase 2 Active
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl text-white">
          Intelligent Meeting Assistant Agent
        </h1>
        <p className="text-base sm:text-lg text-zinc-400">
          Transform meeting audio, transcripts, and notes into structured executive summaries,
          Minutes of Meeting (MoM), actionable tasks with owners and deadlines, and cited semantic chat.
        </p>
      </div>

      {/* Live System Diagnostics */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card className="border-indigo-500/20 bg-gradient-to-b from-indigo-950/20 to-zinc-900/60">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-zinc-300">FastAPI Backend</CardTitle>
            <Server className="h-4 w-4 text-indigo-400" />
          </CardHeader>
          <CardContent className="space-y-1">
            <div className="text-2xl font-bold text-white">
              {health?.status === "ok" ? "200 OK" : "Connecting..."}
            </div>
            <p className="text-xs text-zinc-400">
              {health ? `v${health.version} (${health.environment})` : `Polling ${API_BASE_URL}`}
            </p>
          </CardContent>
        </Card>

        <Card className="border-purple-500/20 bg-gradient-to-b from-purple-950/20 to-zinc-900/60">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-zinc-300">Next.js Frontend</CardTitle>
            <Layers className="h-4 w-4 text-purple-400" />
          </CardHeader>
          <CardContent className="space-y-1">
            <div className="text-2xl font-bold text-white">Next.js 15</div>
            <p className="text-xs text-zinc-400">React 19 + TypeScript Strict + Tailwind v4</p>
          </CardContent>
        </Card>

        <Card className="border-emerald-500/20 bg-gradient-to-b from-emerald-950/20 to-zinc-900/60">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-zinc-300">AI Intelligence Core</CardTitle>
            <Cpu className="h-4 w-4 text-emerald-400" />
          </CardHeader>
          <CardContent className="space-y-1">
            <div className="text-2xl font-bold text-white">Gemini 2.5</div>
            <p className="text-xs text-zinc-400">LangGraph + Whisper + FAISS Vector</p>
          </CardContent>
        </Card>

        <Card className="border-amber-500/20 bg-gradient-to-b from-amber-950/20 to-zinc-900/60">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-zinc-300">Persistence Store</CardTitle>
            <Database className="h-4 w-4 text-amber-400" />
          </CardHeader>
          <CardContent className="space-y-1">
            <div className="text-2xl font-bold text-white">PostgreSQL</div>
            <p className="text-xs text-zinc-400">SQLAlchemy 2.0 Async + Alembic</p>
          </CardContent>
        </Card>
      </div>

      {/* Interactive Diagnostics & Testing Console */}
      <Card className="border-zinc-800 bg-zinc-900/70">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-lg text-white flex items-center gap-2">
                <Terminal className="h-5 w-5 text-indigo-400" />
                Live API Diagnostic Console
              </CardTitle>
              <CardDescription>
                Verify backend request context tracing, X-Request-ID propagation, and uniform error formatting.
              </CardDescription>
            </div>
            <Button
              onClick={runApiTest}
              disabled={testing}
              variant="default"
              size="sm"
              className="gap-2"
            >
              <RefreshCw className={`h-4 w-4 ${testing ? "animate-spin" : ""}`} />
              Probe API Health
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {testResult ? (
            <div className="rounded-lg bg-zinc-950 border border-zinc-800 p-4 font-mono text-xs text-emerald-400 overflow-x-auto">
              <pre>{testResult}</pre>
            </div>
          ) : (
            <div className="rounded-lg bg-zinc-950/60 border border-zinc-800/60 p-6 text-center text-zinc-500 text-sm">
              Click &quot;Probe API Health&quot; to execute an async round-trip diagnostic against the backend.
            </div>
          )}

          <div className="flex flex-wrap items-center gap-4 pt-2 text-xs text-zinc-400">
            <span className="flex items-center gap-1.5">
              <ShieldCheck className="h-4 w-4 text-emerald-400" />
              Uniform Error Envelopes Active
            </span>
            <span className="flex items-center gap-1.5">
              <Clock className="h-4 w-4 text-indigo-400" />
              X-Request-ID Latency Header Tracing Active
            </span>
            <a
              href={API_DOCS_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="ml-auto inline-flex items-center gap-1 text-indigo-400 hover:text-indigo-300"
            >
              Open Interactive Swagger UI <ExternalLink className="h-3 w-3" />
            </a>
          </div>
        </CardContent>
      </Card>

      {/* Engineering Roadmap Tracker */}
      <div className="space-y-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">Engineering Phased Roadmap</h2>
          <p className="text-sm text-zinc-400">Strict single-phase delivery progression with tests and typed APIs.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {phases.map((p) => (
            <div
              key={p.num}
              className={`rounded-xl border p-4 transition-all duration-200 ${
                p.status === "completed"
                  ? "border-emerald-500/30 bg-emerald-950/10"
                  : p.status === "active"
                  ? "border-indigo-500/50 bg-indigo-950/20 shadow-lg shadow-indigo-500/10"
                  : "border-zinc-800/80 bg-zinc-900/40 opacity-70"
              }`}
            >
              <div className="flex items-center justify-between pb-2">
                <span className="text-xs font-mono font-bold text-zinc-400">PHASE {p.num}</span>
                {p.status === "completed" ? (
                  <Badge variant="success" className="gap-1">
                    <CheckCircle className="h-3 w-3" /> Done
                  </Badge>
                ) : p.status === "active" ? (
                  <Badge variant="indigo" className="gap-1">
                    <RefreshCw className="h-3 w-3 animate-spin" /> In Progress
                  </Badge>
                ) : (
                  <Badge variant="outline" className="text-zinc-500">Upcoming</Badge>
                )}
              </div>
              <h3 className="text-sm font-semibold text-white">{p.title}</h3>
              <p className="mt-1 text-xs text-zinc-400">{p.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
