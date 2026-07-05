# Citation Subsystem Architecture

This document describes the flow of retrieved sources and answer syntheses through the citation generation subsystem.

```
Retrieved Sources
        │
        ▼
 Source Tracking
        │
        ▼
Citation Building
        │
        ▼
Provenance Mapping
        │
        ▼
 Final Citations
```

## Flow Description

1. **Retrieved Sources**: Text chunks, entities, and relationships collected during retrieval phases.
2. **Source Tracking**: Items pass through the `SourceTracker` to generate `SourceReference` records, attaching lineage and type definitions.
3. **Citation Building**: The `CitationBuilder` parses synthesized answer text alongside track references, generating `Citation` entries mapping specific char spans to sources.
4. **Provenance Mapping**: The `ProvenanceMapper` constructs relational lineage links illustrating how graph objects and text segments trace back to raw documents.
5. **Final Citations**: The validated citations and provenance metadata are compiled into the `CitationPayload` returned to client systems.
