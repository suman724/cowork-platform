/**
 * Event envelope builder for the cowork platform.
 *
 * Creates standard event envelopes with auto-generated eventId and timestamp.
 */

import { randomUUID } from "node:crypto";

export interface EventEnvelopeData {
  eventId: string;
  eventType: string;
  timestamp: string;
  tenantId: string;
  userId: string;
  sessionId: string;
  component: string;
  payload: Record<string, unknown>;
  taskId?: string;
  stepId?: string;
  workspaceId?: string;
}

export function buildEvent(params: {
  eventType: string;
  tenantId: string;
  userId: string;
  sessionId: string;
  component: string;
  payload: Record<string, unknown>;
  taskId?: string;
  stepId?: string;
  workspaceId?: string;
}): EventEnvelopeData {
  return {
    eventId: randomUUID(),
    timestamp: new Date().toISOString(),
    eventType: params.eventType,
    tenantId: params.tenantId,
    userId: params.userId,
    sessionId: params.sessionId,
    component: params.component,
    payload: params.payload,
    ...(params.taskId !== undefined && { taskId: params.taskId }),
    ...(params.stepId !== undefined && { stepId: params.stepId }),
    ...(params.workspaceId !== undefined && {
      workspaceId: params.workspaceId,
    }),
  };
}
