/**
 * Shared API contracts and types matching FastAPI Pydantic models.
 */

export interface ErrorDetail {
  code: string;
  message: string;
  details?: Record<string, unknown> | Array<unknown> | string | null;
}

export interface ErrorResponse {
  error: ErrorDetail;
}

export interface HealthResponse {
  status: string;
  version: string;
  environment: string;
  uptime_seconds: number;
  timestamp: string;
}

export interface PaginationParams {
  page?: number;
  page_size?: number;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  pagination: PaginationMeta;
}

export type TaskStatus = "TODO" | "IN_PROGRESS" | "DONE";
export type MeetingSourceType = "AUDIO" | "TRANSCRIPT" | "NOTES";
export type MeetingStatus = "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED";
