# REAL-TIME ARCHITECTURE

This platform utilizes modern real-time architecture components for event-driven pipelines.

## Technologies
- **SSE (Server-Sent Events)**: For unidirectional status updates from server to client.
- **WebSockets**: For bi-directional interactive sessions.
- **Event-Driven Pipelines**: Using Redis Pub/Sub or Temporal for background processing.

## Real-Time Update Surfaces
The frontend dashboard consumes real-time data for the following surfaces:
- **AI Scoring**: Immediate feedback when a job's relevance score is updated.
- **Job Ingestion**: Live feed of incoming jobs being scraped.
- **Notifications**: System alerts and actionable notifications.
- **Cover Letter Status**: Streaming generation of AI cover letters.
- **Workflow Status**: Agent pipeline progress (e.g., scraping, embedding, ranking).
