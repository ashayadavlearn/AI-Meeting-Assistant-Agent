/**
 * Shared application constants across frontend and backend.
 */

export const API_VERSION = "0.1.0";
export const API_V1_PREFIX = "/api/v1";

export const SUPPORTED_AUDIO_EXTENSIONS = [".mp3", ".wav", ".m4a"] as const;
export const SUPPORTED_TRANSCRIPT_EXTENSIONS = [".txt", ".md", ".vtt", ".srt", ".docx"] as const;

export const MAX_FILE_SIZE_BYTES = 104_857_600; // 100MB
